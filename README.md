# LeanSaaS Starter Kit 🚀

A modern, high-performance full-stack boilerplate built with **FastAPI**, **SQLModel**, **Angular 19 (Zoneless)**, and **Stripe Lifetime Billing**.

## Features

- **Backend:** FastAPI with SQLModel (SQLite/PostgreSQL ready)
- **Frontend:** Angular 19 featuring signal-based state and Zoneless change detection
- **Authentication:** JWT Auth (Login, Register, Protected Routes)
- **Billing:** Stripe Webhook integration pre-configured for One-Time / Lifetime Pass models
- **DevOps:** Docker Compose setup for single-command local development

---

## Quick Start Guide

### 1. Prerequisites

Ensure you have the following installed on your machine:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Stripe CLI](https://stripe.com/docs/stripe-cli) (for local webhook testing)

### 2. Environment Configuration

Clone the example environment file:

```bash
cp .env.example .env