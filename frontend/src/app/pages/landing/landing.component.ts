import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1e293b; line-height: 1.6;">
      
      <!-- Navigation -->
      <nav style="display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; padding: 20px;">
        <div style="font-weight: 700; font-size: 20px; color: #2563eb;">⚡ LeanSaaS</div>
        <div>
          <a routerLink="/login" style="margin-right: 16px; text-decoration: none; color: #475569; font-weight: 500;">Sign In</a>
          <a routerLink="/login" style="padding: 8px 16px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: 500;">Get Started</a>
        </div>
      </nav>

      <!-- Hero Section -->
      <header style="text-align: center; max-width: 800px; margin: 60px auto 40px; padding: 0 20px;">
        <h1 style="font-size: 48px; font-weight: 800; letter-spacing: -1px; margin-bottom: 16px;">
          Launch Your Micro-SaaS in Hours, Not Weeks
        </h1>
        <p style="font-size: 18px; color: #64748b; margin-bottom: 32px;">
          Production-ready full-stack boilerplate built with FastAPI, Angular, Docker Compose, and Stripe Checkout.
        </p>
        <div style="display: flex; gap: 12px; justify-content: center;">
          <a routerLink="/login" style="padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">Start Building Now</a>
          <a href="#pricing" style="padding: 12px 24px; background: #f1f5f9; color: #334155; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 16px;">View Pricing</a>
        </div>
      </header>

      <!-- Features Grid -->
      <section style="max-width: 1000px; margin: 80px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
        <div style="padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc;">
          <h3 style="margin-top: 0;">⚡ FastAPI Backend</h3>
          <p style="color: #64748b; margin: 0;">Async endpoints, JWT security, SQLModel ORM, and automated OpenAPI documentation out of the box.</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc;">
          <h3 style="margin-top: 0;">🅰️ Angular Frontend</h3>
          <p style="color: #64748b; margin: 0;">Standalone components, HTTP interceptors, reactive state management, and modern Angular routing.</p>
        </div>
        <div style="padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px; background: #f8fafc;">
          <h3 style="margin-top: 0;">💳 Stripe Webhooks</h3>
          <p style="color: #64748b; margin: 0;">Secure payment collection and webhook handling for automatic database subscription fulfillment.</p>
        </div>
      </section>

      <!-- Pricing Section -->
      <section id="pricing" style="max-width: 800px; margin: 80px auto; padding: 0 20px; text-align: center;">
        <h2 style="font-size: 32px; font-weight: 700;">Simple Pricing</h2>
        <p style="color: #64748b; margin-bottom: 40px;">Choose the tier that fits your needs.</p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
          <!-- Free Tier -->
          <div style="padding: 32px; border: 1px solid #e2e8f0; border-radius: 12px; text-align: left;">
            <h3>Starter</h3>
            <p style="font-size: 36px; font-weight: 800; margin: 16px 0;">$0 <span style="font-size: 14px; font-weight: 400; color: #64748b;">/ forever</span></p>
            <ul style="padding-left: 20px; color: #475569; margin-bottom: 24px;">
              <li style="margin-bottom: 8px;">Basic API access</li>
              <li style="margin-bottom: 8px;">Public dashboard</li>
              <li>Community support</li>
            </ul>
            <a routerLink="/login" style="display: block; text-align: center; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; text-decoration: none; color: #334155; font-weight: 600;">Sign Up Free</a>
          </div>

          <!-- Pro Tier -->
          <div style="padding: 32px; border: 2px solid #2563eb; border-radius: 12px; text-align: left; position: relative; background: #f8fafc;">
            <span style="position: absolute; top: -12px; right: 20px; background: #2563eb; color: white; padding: 2px 10px; font-size: 12px; font-weight: 700; border-radius: 12px;">POPULAR</span>
            <h3>Pro Pass</h3>
            <p style="font-size: 36px; font-weight: 800; margin: 16px 0;">$10 <span style="font-size: 14px; font-weight: 400; color: #64748b;">/ month</span></p>
            <ul style="padding-left: 20px; color: #475569; margin-bottom: 24px;">
              <li style="margin-bottom: 8px;">Access to gated <code>/pro-feature</code> endpoints</li>
              <li style="margin-bottom: 8px;">Priority webhook processing</li>
              <li style="margin-bottom: 8px;">Full source code access</li>
              <li>Premium badge & support</li>
            </ul>
            <a routerLink="/login" style="display: block; text-align: center; padding: 10px; background: #2563eb; color: white; border-radius: 6px; text-decoration: none; font-weight: 600;">Upgrade to Pro</a>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer style="text-align: center; padding: 40px 20px; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 14px;">
        © 2026 LeanSaaS Starter Kit. Ready to deploy anywhere.
      </footer>

    </div>
  `
})
export class LandingComponent {}