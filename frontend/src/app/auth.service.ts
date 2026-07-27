// frontend/src/app/auth.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';

export interface User {
  id: number;
  email: string;
  full_name?: string;
  is_premium: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000';

  currentUser$ = new BehaviorSubject<User | null>(null);

  constructor() {
    if (this.getToken()) {
      this.fetchCurrentUser().subscribe();
    }
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  login(credentials: { username: string; password: string }) {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return this.http.post<{ access_token: string }>(`${this.apiUrl}/auth/login`, formData).pipe(
      tap(res => {
        localStorage.setItem('access_token', res.access_token);
        this.fetchCurrentUser().subscribe();
      })
    );
  }

  register(userData: { email: string; password: string; full_name?: string }) {
    return this.http.post(`${this.apiUrl}/auth/register`, userData);
  }

  fetchCurrentUser() {
    return this.http.get<User>(`${this.apiUrl}/auth/me`).pipe(
      tap(user => this.currentUser$.next(user))
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    this.currentUser$.next(null);
  }
}