import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="max-width: 800px; margin: 40px auto; font-family: sans-serif; padding: 24px;">
      <div style="display: flex; justify-space-between; align-items: center; margin-bottom: 24px;">
        <h1>User Dashboard</h1>
        <button (click)="logout()" style="padding: 8px 16px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer;">Logout</button>
      </div>

      <div *ngIf="auth.currentUser$ | async as user; else loading" style="background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 24px;">
        <h3>Welcome, {{ user.full_name || user.email }}!</h3>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p>
          <strong>Status:</strong> 
          <span [style.color]="user.is_premium ? '#16a34a' : '#dc2626'" style="font-weight: bold;">
            {{ user.is_premium ? 'PRO SUBSCRIBER ⚡' : 'FREE USER' }}
          </span>
        </p>
      </div>

      <ng-template #loading><p>Loading user details...</p></ng-template>

      <div style="border-top: 1px solid #e2e8f0; padding-top: 20px;">
        <h3>Test Gated Pro Endpoint</h3>
        <button (click)="testProFeature()" style="padding: 10px 20px; background: #059669; color: white; border: none; border-radius: 4px; cursor: pointer;">
          Fetch /auth/pro-feature
        </button>

        <div *ngIf="proResponse" style="margin-top: 16px; padding: 12px; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 4px; color: #065f46;">
          <strong>API Response:</strong> {{ proResponse }}
        </div>
        <div *ngIf="proError" style="margin-top: 16px; padding: 12px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 4px; color: #991b1b;">
          <strong>Access Denied:</strong> {{ proError }}
        </div>
      </div>
    </div>
  `
})
export class DashboardComponent {
  auth = inject(AuthService);
  http = inject(HttpClient);
  router = inject(Router);

  proResponse = '';
  proError = '';

  testProFeature() {
    this.proResponse = '';
    this.proError = '';
    this.http.get<{ message: string }>('http://localhost:8000/auth/pro-feature').subscribe({
      next: (res) => this.proResponse = JSON.stringify(res),
      error: (err) => this.proError = err.error?.detail || 'You need an active subscription to access this feature!'
    });
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}