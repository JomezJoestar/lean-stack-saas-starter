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
```

Ensure `.env` contains your database and JWT secrets:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=saas_db
DATABASE_URL=postgresql://postgres:postgres@db:5432/saas_db
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Build and Run Services

Start all containers in detached or attached mode using Docker Compose:

```bash
docker compose up --build
```

Access the running applications:
- **Frontend App:** `http://localhost:4200`
- **Backend API Docs:** `http://localhost:8000/docs`
- **PostgreSQL Database:** `localhost:5432`

---

## Testing Webhooks Locally

To forward Stripe checkout events directly to your containerized backend:

1. **Start listening to Stripe events:**
   ```bash
   stripe listen --events checkout.session.completed --forward-to localhost:8000/billing/webhook
   ```

2. **Trigger a mock checkout completed event:**
   ```bash
   stripe trigger checkout.session.completed
   ```

3. **Verify backend log output:**
   Check the `backend-1` terminal log stream to confirm the `is_premium` status updated in PostgreSQL:
   ```text
   🎉 SUCCESS: Activated lifetime pass in DB for stripe@example.com!
   ```

---

## Database Management

Connect directly to the PostgreSQL database container shell:

```bash
docker compose exec db psql -U postgres -d saas_db
```

Query or manually update user roles:
```sql
SELECT id, email, is_premium FROM "user";
UPDATE "user" SET is_premium = true WHERE email = 'stripe@example.com';
```

---

## Project Structure

```text
lean-stack-saas-starter/
├── backend/
│   ├── app/
│   │   ├── routers/       # Auth and Billing API endpoints
│   │   ├── models.py      # SQLModel database schemas
│   │   ├── database.py    # Database connection setup
│   │   └── main.py        # FastAPI entrypoint
│   └── Dockerfile
├── frontend/
│   ├── src/               # Angular 19 components & services
│   └── Dockerfile
├── docker-compose.yml     # Multi-container orchestration
├── .env.example           # Environment template
└── README.md              # Documentation
```