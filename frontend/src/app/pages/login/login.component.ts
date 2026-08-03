import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <div style="max-width: 400px; margin: 80px auto; font-family: sans-serif; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
      <h2>{{ isRegister ? 'Create Account' : 'Welcome Back' }}</h2>

      <form (ngSubmit)="handleSubmit()">
        <div *ngIf="isRegister" style="margin-bottom: 12px;">
          <label style="display: block; margin-bottom: 4px;">Full Name</label>
          <input type="text" [(ngModel)]="fullName" name="fullName" required style="width: 100%; padding: 8px; box-sizing: border-box;">
        </div>

        <div style="margin-bottom: 12px;">
          <label style="display: block; margin-bottom: 4px;">Email</label>
          <input type="email" [(ngModel)]="email" name="email" required style="width: 100%; padding: 8px; box-sizing: border-box;">
        </div>

        <div style="margin-bottom: 16px;">
          <label style="display: block; margin-bottom: 4px;">Password</label>
          <input type="password" [(ngModel)]="password" name="password" required style="width: 100%; padding: 8px; box-sizing: border-box;">
        </div>

        <button type="submit" style="width: 100%; padding: 10px; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer;">
          {{ isRegister ? 'Register' : 'Sign In' }}
        </button>
      </form>

      <p *ngIf="errorMessage" style="color: #dc2626; margin-top: 12px;">{{ errorMessage }}</p>

      <p style="margin-top: 16px; font-size: 14px; text-align: center;">
        <a (click)="isRegister = !isRegister" style="color: #2563eb; cursor: pointer; text-decoration: underline;">
          {{ isRegister ? 'Already have an account? Sign In' : "Don't have an account? Register" }}
        </a>
      </p>
    </div>
  `
})
export class LoginComponent{
  auth = inject(AuthService);
  router = inject(Router);

  isRegister = false;
  email = '';
  password = '';
  fullName = '';
  errorMessage = '';

  handleSubmit() {
    this.errorMessage = '';
    if (this.isRegister) {
      this.auth.register({ email: this.email, password: this.password, full_name: this.fullName }).subscribe({
        next: () => {
          this.isRegister = false;
          alert('Registration successful! Please sign in.');
        },
        error: (err) => this.errorMessage = err.error?.detail || 'Registration failed'
      });
    } else {
      this.auth.login({ username: this.email, password: this.password }).subscribe({
        next: () => this.router.navigate(['/dashboard']),
        error: (err) => this.errorMessage = err.error?.detail || 'Invalid email or password'
      });
    }
  }
}