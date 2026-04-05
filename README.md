# U3Vault

> **A comprehensive employee management and vault system** — built with FastAPI, Streamlit, and PostgreSQL, featuring JWT authentication, role-based access control, and powerful HR tools.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

U3Vault is a full-stack HR and employee management platform designed for organizations that need a secure, centralized vault for employee data. It provides a clean **Streamlit** frontend for both admins and employees, backed by a robust **FastAPI** REST API and a **PostgreSQL** database.

Whether you're managing employee records, tracking attendance, handling leave requests, or storing contract documents, U3Vault has you covered — all protected by industry-standard JWT authentication and bcrypt password hashing.

---

## Key Features

### 🔐 Security
- **JWT Token Authentication** — Stateless, expiring tokens (60-minute default) issued via `python-jose` with HS256 algorithm
- **Bcrypt Password Hashing** — Passwords are hashed using `passlib` with bcrypt; plain-text passwords are never stored
- **Strong Password Policy** — Enforced password requirements: minimum 10 characters, at least one uppercase letter, one lowercase letter, and one digit
- **Token Verification Endpoints** — Dedicated endpoints to validate active tokens and re-authenticate users before sensitive actions

### 👥 Role-Based Access Control
Three distinct roles with scoped permissions:
| Role | Capabilities |
|------|-------------|
| **Admin** | Full access — manage company settings, create/delete employees |
| **Manager** | Manage employees, approve/reject leave requests, view attendance analytics |
| **Employee** | View own profile, update own info, submit leave requests, view own attendance |

### 🏢 Employee Management
- Full **CRUD operations** for employee records
- Rich employee profiles: name, job title, department, role, supervisor, gender, date of birth, address, and employment details
- Support for multiple **contract types** (Employee, Temporary, Intern) and **employment types** (Full-time, Part-time)
- Employee **status tracking**: Active, On Leave, Inactive, Resigned
- Profile **photo upload** and **contract PDF** storage

### 📅 Leave Request System
- Employees can submit leave requests directly from the interface
- Managers can view, approve, or reject requests via a dedicated management endpoint
- Status tracking for all leave requests

### 📊 Attendance Tracking
- Log daily attendance for all employees
- Date-conflict detection to prevent duplicate entries
- Filter attendance records by date range
- **Analytics & Reports**: global and per-employee attendance analytics
- **Visual Charts**: trend plots and pie charts (returned as PNG images)
- PDF report generation for attendance data

### 📄 Document Management
- Store and retrieve employee **contract PDFs**
- Shared volume ensures both backend and frontend can access uploaded files seamlessly

### ✅ Data Validation
- **Phone number validation** with international country code support (`pydantic-extra-types` + `phonenumbers`)
- **Email validation** via Pydantic's `EmailStr`
- **Enum-enforced fields** for gender, status, contract type, employment type, and role
- Full request body validation through Pydantic models on every endpoint

### 🏗️ Company Management
- Register your company with a unique **auto-generated slug** (used as a tenant identifier for employee login)
- Company slug lookup and password update support
- Multi-tenant ready architecture

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Python 3.12 |
| **Frontend** | Streamlit |
| **Database** | PostgreSQL 15 |
| **ORM** | SQLAlchemy |
| **Authentication** | python-jose (JWT / HS256) |
| **Password Hashing** | passlib (bcrypt) |
| **Validation** | Pydantic v2, pydantic-extra-types, phonenumbers |
| **Analytics** | Pandas, Matplotlib, Seaborn |
| **PDF Generation** | fpdf |
| **Containerization** | Docker, Docker Compose |

---

## Project Structure

```
U3Vault/
├── docker-compose.yml          # Orchestrates backend, frontend, and PostgreSQL
│
├── backend/
│   ├── api/
│   │   └── api.py              # FastAPI app entry point, router registration, lifespan
│   ├── auth/                   # Authentication module (JWT login, token & password verification)
│   ├── create_company/         # Company registration & management
│   ├── employees/              # Employee CRUD, contract retrieval, profile updates
│   ├── attendance/             # Attendance logging, analytics, charts, PDF reports
│   ├── leave_req/              # Leave request submission and management
│   ├── shared/
│   │   └── func.py             # Shared helpers: JWT decode (`lazy`), password policy check
│   ├── db/                     # Database connection setup (SQLAlchemy engine)
│   ├── .env                    # Environment variables (DB credentials, JWT config)
│   ├── dockerfile
│   └── reqs.txt                # Python dependencies
│
└── frontend/
    ├── index.py                # Main Streamlit application
    ├── model.py                # Frontend data models
    ├── .env                    # Frontend environment variables
    ├── dockerfile
    └── reqs.txt                # Frontend Python dependencies
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Go](https://go.dev/dl/) *(required for auxiliary tooling and scripts)*

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Universal-Unlimited-Unity/U3Vault.git
   cd U3Vault
   ```

2. **Configure environment variables**

   Review and update the backend environment file before starting:

   ```bash
   # backend/.env
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="your_secure_password"
   POSTGRES_DB="vault"
   TOKEN_EXP_MIN="60"
   TOKEN_KEY="your_secret_key"
   ALGO="HS256"
   ```

   > ⚠️ Change `TOKEN_KEY` and `POSTGRES_PASSWORD` to strong, unique values before deploying.

3. **Start all services**

   ```bash
   docker-compose up --build
   ```

   Docker Compose will spin up three containers:
   - `db` — PostgreSQL 15 database
   - `backend` — FastAPI application
   - `frontend` — Streamlit web interface

4. **Access the application**

   | Service | URL |
   |---------|-----|
   | **Frontend (Streamlit)** | http://localhost:8501 |
   | **Backend API** | http://localhost:8000 |
   | **API Docs (Swagger)** | http://localhost:8000/docs |
   | **API Docs (ReDoc)** | http://localhost:8000/redoc |

### Database Initialization

The database tables are created automatically on first startup via SQLAlchemy. No manual migration steps are required.

### Development Mode (Live Reload)

The `docker-compose.yml` includes a `develop.watch` configuration for live sync:

```bash
docker-compose watch
```

This will sync file changes from your local machine into the containers and rebuild automatically when `reqs.txt` changes.

---

## Configuration

All configuration is managed via the `backend/.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | *(set your own)* |
| `POSTGRES_DB` | Database name | `vault` |
| `TOKEN_EXP_MIN` | JWT token expiration in minutes | `60` |
| `TOKEN_KEY` | Secret key for signing JWT tokens | *(set your own)* |
| `ALGO` | JWT signing algorithm | `HS256` |

---

## API Endpoints

All endpoints require an `Authorization: Bearer <token>` header unless otherwise noted.

### Authentication — `/auth`
| Method | Path | Description | Auth Required |
|--------|------|-------------|:---:|
| `POST` | `/auth/login` | Login (Admin or Employee/Manager) and receive a JWT token | ❌ |
| `POST` | `/auth/verify` | Verify a user's current password | ✅ |
| `POST` | `/auth/verify/token` | Check if the current token is still valid | ✅ |
| `POST` | `/auth/verify/admin` | Verify the Admin's password before sensitive actions | ✅ |

### Company — `/company`
| Method | Path | Description | Auth Required |
|--------|------|-------------|:---:|
| `POST` | `/company` | Register a new company | ❌ |
| `GET` | `/company` | Get current company name | ✅ |
| `GET` | `/company/slug` | Get company login slug | ✅ |
| `GET` | `/company/{name}` | Generate a slug from a company name | ❌ |
| `PATCH` | `/company` | Update company password | ✅ |

### Employees — `/employees`
| Method | Path | Description | Auth Required |
|--------|------|-------------|:---:|
| `POST` | `/employees` | Add a new employee (Admin/Manager only) | ✅ |
| `GET` | `/employees` | List employees for selection (Admin/Manager) | ✅ |
| `GET` | `/employees/dataframe` | List all employees with full details (Admin/Manager) | ✅ |
| `GET` | `/employees/{id}` | Get a single employee's profile | ✅ |
| `PATCH` | `/employees` | Employee updates their own profile | ✅ |
| `DELETE` | `/employees/{id}` | Delete an employee (Admin only) | ✅ |
| `GET` | `/employees/contracts/{id}` | Retrieve an employee's contract PDF | ✅ |

### Attendance — `/attendance`
| Method | Path | Description | Auth Required |
|--------|------|-------------|:---:|
| `GET` | `/attendance/` | Get employee attendance dictionary | ❌ |
| `POST` | `/attendance/` | Insert attendance records | ❌ |
| `GET` | `/attendance/date` | Check if a date already has attendance records | ❌ |
| `GET` | `/attendance/records` | Get all attendance records (optional date range) | ❌ |
| `GET` | `/attendance/records/{id}` | Get attendance records for one employee | ✅ |
| `GET` | `/attendance/analytics` | Global attendance analytics | ❌ |
| `GET` | `/attendance/analytics/{id}` | Per-employee analytics | ❌ |
| `GET` | `/attendance/analytics/plots` | Trend plot image (Admin/Manager) | ✅ |
| `GET` | `/attendance/analytics/piechart` | Global pie chart (Admin/Manager) | ✅ |
| `GET` | `/attendance/analytics/piechart/{id}` | Per-employee pie chart | ✅ |
| `GET` | `/attendance/analytics/reports` | Generate PDF attendance report | ❌ |

### Leave Requests — `/requests`
| Method | Path | Description | Auth Required |
|--------|------|-------------|:---:|
| `POST` | `/requests` | Submit a leave request (Employee only) | ✅ |
| `GET` | `/requests` | Get own leave requests by status (Employee) | ✅ |
| `GET` | `/requests/AdMan` | Get all leave requests (Admin/Manager) | ✅ |
| `PATCH` | `/requests/AdMan` | Approve or reject a leave request (Admin/Manager) | ✅ |

---

## Screenshots

> 📸 *Screenshots coming soon — add your application screenshots here!*

<!-- 
  Replace the placeholders below with actual screenshots of your application.
  Recommended sections to capture:
  - Login screen
  - Admin dashboard
  - Employee list view
  - Employee profile page
  - Attendance tracking page
  - Leave request management
  - Analytics / charts
-->

### Login
![Login Screen](docs/screenshots/login.png)

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)

### Employee Management
![Employee Management](docs/screenshots/employee-management.png)

### Attendance Analytics
![Attendance Analytics](docs/screenshots/attendance-analytics.png)

### Leave Request Management
![Leave Requests](docs/screenshots/leave-requests.png)

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Commit** your changes: `git commit -m "Add my feature"`
4. **Push** to your branch: `git push origin feature/my-feature`
5. **Open** a Pull Request

Please make sure your code follows the existing style and that any new API endpoints are properly validated and protected.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ by the Universal Unlimited Unity team</sub>
</div>
