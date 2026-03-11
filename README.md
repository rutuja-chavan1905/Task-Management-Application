<div align="center">

# ✅ Smart Task & Productivity Manager

**A full-stack task management web application built with Flask, React, and MySQL**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)

<br/>

> A secure, feature-rich productivity application where users can register, log in, and manage their daily tasks with priorities, due dates, and real-time notifications.

<br/>

![Dashboard Preview](https://via.placeholder.com/800x400/4f46e5/ffffff?text=Smart+Task+Manager+—+Dashboard)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🌟 Overview

**Smart Task & Productivity Manager** is a full-stack web application that demonstrates real-world software development practices including:

- **REST API design** with Python Flask
- **JWT-based authentication** with bcrypt password hashing
- **Relational database** design with MySQL foreign keys
- **Server-side pagination** using SQL `LIMIT` and `OFFSET`
- **Modern React frontend** with Context API, hooks, and component architecture
- **Real-time notifications** using Toastify
- **Data export** to CSV and JSON formats

Each user has a private, isolated workspace — their tasks are never visible to other users.

---

## ✨ Features

### 🔐 Authentication System
| Feature | Description |
|---|---|
| User Registration | Create an account with name, email, and password |
| Secure Login | Passwords hashed with **bcrypt** — never stored in plain text |
| JWT Tokens | Stateless authentication — token valid for **24 hours** |
| **Lockout System** | Form locks for **30 seconds** after **3 failed login attempts** with a live countdown timer |
| Session Persistence | Stay logged in across page refreshes via localStorage |

### ✅ Task Management (Full CRUD)
| Feature | Description |
|---|---|
| Create Tasks | Add title, description, priority, and due date |
| View Tasks | Paginated table showing 10 tasks per page |
| Edit Tasks | Update any field inline with a pre-filled form |
| Delete Tasks | Permanently remove with a confirmation prompt |
| Toggle Status | One-click checkbox to mark Pending ↔ Completed |
| Priority Levels | **Low** / **Medium** / **High** with colour-coded badges |

### 📅 Due Date Warnings
| Warning | Trigger |
|---|---|
| 🔴 **⚠ Overdue** | Task's due date has already passed |
| 🟡 **🔔 Today** | Task is due today |
| 🔵 **📅 Tomorrow** | Task is due the next day |

Overdue rows are highlighted in red; due-today rows in yellow.

### 📊 Dashboard & Analytics
- **3 stat cards** — Total, Completed, and Pending task counts
- **SVG Donut Chart** — Visual breakdown of Completed vs Pending (built with pure SVG, no chart library)
- **Priority Bar Chart** — Horizontal bars showing High / Medium / Low task counts
- **Progress Bar** — Animated completion percentage

### 📤 Export Options
- **⬇ Export CSV** — Downloads all tasks as a `.csv` spreadsheet
- **⬇ Export JSON** — Downloads all tasks as a formatted `.json` file
- Exports always fetch the **complete task list**, bypassing pagination

### 🔔 Toast Notifications
All user actions trigger a **Toastify** notification instead of disruptive alert boxes:
- ✅ Task created / updated / deleted
- ✏️ Task status toggled
- ⚠️ Overdue tasks detected on load
- 📥 File exported successfully
- 🔒 Login lockout triggered / unlocked

### 📄 Pagination
- Tasks displayed **10 per page**
- Smart page number controls with `…` ellipsis for large page counts
- **Prev / Next** buttons + numbered page buttons
- Page info: *"Page 2 of 5 · 48 tasks"*
- Filter tabs (All / Pending / Completed) reset to page 1

---

## 🛠 Tech Stack

### Backend
| Package | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Core language |
| Flask | 3.0.0 | REST API framework |
| Flask-CORS | 4.0.0 | Cross-origin request handling |
| Flask-Bcrypt | 1.0.1 | Password hashing |
| PyJWT | 2.8.0 | JWT token creation and verification |
| mysql-connector-python | 8.2.0 | MySQL database driver |

### Frontend
| Package | Version | Purpose |
|---|---|---|
| React | 18.2.0 | UI component library |
| Vite | 5.0.0 | Build tool and dev server |
| React Router DOM | 6.20.1 | Client-side routing |
| Axios | 1.6.2 | HTTP client with interceptors |
| React Toastify | 10.0.4 | Toast notification system |

### Database
| Tool | Version | Purpose |
|---|---|---|
| MySQL | 8.0+ | Relational data storage |

---

## 📁 Project Structure

```
smart-task-manager/
│
├── 📄 database.sql                    # MySQL table creation queries
├── 📄 README.md                       # This file
│
├── 📂 backend/                        # Python Flask REST API
│   ├── 🐍 app.py                      # Application entry point
│   ├── 🐍 config.py                   # Database & JWT configuration
│   ├── 🐍 database.py                 # MySQL connection factory
│   ├── 🐍 models.py                   # All SQL query functions
│   ├── 📄 requirements.txt            # Python dependencies
│   └── 📂 routes/
│       ├── 🐍 __init__.py
│       ├── 🐍 auth_routes.py          # /register  /login  /profile
│       └── 🐍 task_routes.py          # /tasks  /dashboard  (CRUD + pagination)
│
└── 📂 frontend/                       # React + Vite application
    ├── 📄 index.html
    ├── 📄 package.json
    ├── 📄 vite.config.js
    └── 📂 src/
        ├── ⚛️  App.jsx                 # Routes + ToastContainer
        ├── 🎨 index.css               # Global stylesheet
        ├── ⚛️  main.jsx               # React entry point
        │
        ├── 📂 components/
        │   ├── ⚛️  AuthContext.jsx    # Global auth state (Context API)
        │   └── ⚛️  Navbar.jsx         # Navigation bar
        │
        ├── 📂 pages/
        │   ├── ⚛️  LoginPage.jsx      # Sign in + 3-attempt lockout
        │   ├── ⚛️  RegisterPage.jsx   # Create account
        │   ├── ⚛️  DashboardPage.jsx  # Stats + SVG charts
        │   └── ⚛️  TasksPage.jsx      # Full CRUD + pagination + export
        │
        └── 📂 services/
            └── 📄 api.js              # All Axios HTTP calls (centralised)
```

---

## 🗄 Database Schema

### `users` table

```sql
CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    email      VARCHAR(150)  NOT NULL UNIQUE,
    password   VARCHAR(255)  NOT NULL,            -- bcrypt hash
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP
);
```

### `tasks` table

```sql
CREATE TABLE tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(200)  NOT NULL,
    description TEXT,
    priority    ENUM('Low', 'Medium', 'High')    DEFAULT 'Medium',
    status      ENUM('Pending', 'Completed')     DEFAULT 'Pending',
    due_date    DATE,
    created_at  DATETIME      DEFAULT CURRENT_TIMESTAMP,
    user_id     INT           NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

> **Note:** `ON DELETE CASCADE` means deleting a user account automatically removes all their tasks.

---

## 📡 API Reference

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|:---:|---|---|:---:|
| `POST` | `/register` | Create a new user account | ❌ |
| `POST` | `/login` | Login and receive JWT token | ❌ |
| `GET` | `/profile` | Get current user's profile | ✅ |

**Register — Request Body**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "mypassword123"
}
```

**Login — Response**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiJ9...",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" }
}
```

---

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|:---:|---|---|:---:|
| `GET` | `/dashboard` | Get task stats (total / completed / pending) | ✅ |
| `GET` | `/tasks` | Get paginated tasks | ✅ |
| `GET` | `/tasks?all=true` | Get ALL tasks (for export) | ✅ |
| `POST` | `/tasks` | Create a new task | ✅ |
| `GET` | `/tasks/<id>` | Get a single task | ✅ |
| `PUT` | `/tasks/<id>` | Update a task | ✅ |
| `DELETE` | `/tasks/<id>` | Delete a task | ✅ |
| `PATCH` | `/tasks/<id>/toggle` | Toggle Pending ↔ Completed | ✅ |

**Pagination Query Parameters**

```
GET /tasks?page=2&per_page=10&status=Pending
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | `1` | Page number (1-based) |
| `per_page` | integer | `10` | Items per page (max 100) |
| `status` | string | *(all)* | Filter: `Pending` or `Completed` |
| `all` | string | — | Set to `true` to bypass pagination |

**Paginated Response**
```json
{
  "tasks": [...],
  "total": 48,
  "page": 2,
  "per_page": 10,
  "total_pages": 5
}
```

**Create Task — Request Body**
```json
{
  "title": "Finish the report",
  "description": "Complete sections 3 and 4",
  "priority": "High",
  "due_date": "2025-02-15"
}
```

> **Authentication:** All protected endpoints require the header:
> ```
> Authorization: Bearer <your-jwt-token>
> ```

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed on your machine:

- [Python 3.8+](https://python.org/downloads/) — `python --version`
- [Node.js 18+](https://nodejs.org/) — `node --version`
- [MySQL 8.0+](https://dev.mysql.com/downloads/) — `mysql --version`
- pip (bundled with Python)
- npm (bundled with Node.js)

---

## ⚙️ Environment Configuration

Before running the app, update **`backend/config.py`** with your MySQL credentials:

```python
class Config:
    MYSQL_HOST     = "localhost"
    MYSQL_USER     = "root"           # ← your MySQL username
    MYSQL_PASSWORD = "yourpassword"   # ← your MySQL password
    MYSQL_DB       = "smart_task_db"

    SECRET_KEY         = "change_this_in_production"
    JWT_EXPIRY_SECONDS = 86400        # 24 hours
```

> ⚠️ **Security note:** Change `SECRET_KEY` to a long random string before deploying. Never commit real credentials to version control.

---

## ▶️ Running the Application

You need **three things running** simultaneously: MySQL, the Flask backend, and the React frontend.

### Step 1 — Set up the Database

```bash
# Option A — MySQL command line
mysql -u root -p < database.sql

# Option B — MySQL Workbench
# Open database.sql and click Execute (⚡)
```

This creates the `smart_task_db` database and both tables (`users`, `tasks`).

---

### Step 2 — Start the Backend

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Flask
python app.py
```

✅ **Backend running at:** `http://localhost:5000`

Verify by opening `http://localhost:5000` — you should see:
```json
{ "message": "Smart Task Manager API is running!" }
```

---

### Step 3 — Start the Frontend

Open a **new terminal window**:

```bash
# Navigate to the frontend folder
cd frontend

# Install Node packages
npm install

# Start the dev server
npm run dev
```

✅ **Frontend running at:** `http://localhost:3000`

---

### Step 4 — Open the App

Navigate to **[http://localhost:3000](http://localhost:3000)** in your browser.

1. Click **"Create one"** to register a new account
2. Log in with your credentials
3. Explore the **Dashboard** → charts and stats
4. Go to **My Tasks** → add, edit, delete, and complete tasks
5. Test **Export CSV** and **Export JSON** buttons
6. Test the **lockout**: enter the wrong password 3 times on the login page

---

## ⚡ How It Works

### Authentication Flow

```
User enters credentials
        │
        ▼
POST /login  →  Flask finds user by email
        │
        ▼
bcrypt.check_password_hash(stored_hash, entered_password)
        │
    ┌───┴───┐
  Wrong    Correct
    │         │
    ▼         ▼
 401 Error  Create JWT token
            { user_id: 1, exp: +24h }
            signed with SECRET_KEY
                │
                ▼
            Return token to React
                │
                ▼
            localStorage.setItem('token', ...)
                │
                ▼
            Every future request includes:
            Authorization: Bearer <token>
```

### Pagination Flow

```
User clicks "Next" (page 2)
        │
        ▼
GET /tasks?page=2&per_page=10
        │
        ▼
Flask:  offset = (2 - 1) × 10 = 10
        │
        ▼
SQL:    SELECT * FROM tasks
        WHERE user_id = 1
        ORDER BY created_at DESC
        LIMIT 10 OFFSET 10
        │
        ▼
Response: { tasks: [...10 rows], total: 48, page: 2, total_pages: 5 }
        │
        ▼
React updates table + pagination bar
```

### Login Lockout System

```
Attempt 1 fails → attempts = 1 → "2 attempts remaining"
Attempt 2 fails → attempts = 2 → "1 attempt remaining" + yellow warning
Attempt 3 fails → attempts = 3 → LOCKED
                                  lockTimer = 30 seconds
                                  setInterval counts down every 1s
                                  Inputs disabled, button shows "Locked 27s"
Timer hits 0    → clearInterval()
                  lockedOut = false, attempts = 0
                  Toast: "🔓 Account unlocked"
```

---

## 📸 Screenshots

| Page | Description |
|---|---|
| **Login** | Clean sign-in form with lockout banner after 3 failures |
| **Register** | Account creation with real-time toast feedback |
| **Dashboard** | Stats cards, SVG donut chart, priority bar chart, progress bar |
| **My Tasks** | Paginated table with due date warnings, edit/delete, export buttons |

---

## 🔧 Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError` | Python packages not installed | Run `pip install -r requirements.txt` |
| `Access denied for user 'root'` | Wrong MySQL password | Update `MYSQL_PASSWORD` in `config.py` |
| `Unknown database 'smart_task_db'` | Database not created | Run `database.sql` first (Step 1) |
| `CORS error` in browser | Flask not running | Start Flask: `python app.py` |
| `npm: command not found` | Node.js not installed | Install from [nodejs.org](https://nodejs.org) |
| Port `5000` already in use | Another process using it | Change port in `app.py` and `api.js` |
| Tasks not showing | Token expired | Log out and log in again |
| `pip: command not found` | Python path issue | Use `python -m pip install ...` |

---

## 📦 Available Scripts

### Backend

```bash
python app.py                  # Start development server
pip install -r requirements.txt  # Install dependencies
```

### Frontend

```bash
npm run dev      # Start Vite development server (port 3000)
npm run build    # Build for production
npm run preview  # Preview production build locally
```

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│              React 18 + Vite                        │
│         http://localhost:3000                       │
│                                                     │
│  LoginPage  RegisterPage  DashboardPage  TasksPage  │
│       └────────────────┬────────────────┘           │
│                    api.js (Axios)                   │
└────────────────────────┼────────────────────────────┘
                         │  HTTP / JSON
                         ▼
┌─────────────────────────────────────────────────────┐
│                 Flask REST API                      │
│              http://localhost:5000                  │
│                                                     │
│   auth_routes.py          task_routes.py            │
│   /register /login        /tasks /dashboard         │
│        └──────────────────────┘                     │
│                    models.py                        │
│               (SQL query functions)                 │
└────────────────────────┬────────────────────────────┘
                         │  SQL queries
                         ▼
┌─────────────────────────────────────────────────────┐
│                 MySQL 8 Database                    │
│              localhost:3306                         │
│                                                     │
│   ┌──────────┐        ┌──────────────────────┐     │
│   │  users   │──────► │       tasks          │     │
│   │──────────│  1:N   │──────────────────────│     │
│   │ id       │        │ id                   │     │
│   │ name     │        │ title                │     │
│   │ email    │        │ priority             │     │
│   │ password │        │ status               │     │
│   │ created  │        │ due_date             │     │
│   └──────────┘        │ user_id (FK)         │     │
│                       └──────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

---

## 📄 License

This project is built for educational purposes as a college full-stack development project.

---

<div align="center">

**Built with ❤️ using Flask · React · MySQL**

*Smart Task & Productivity Manager — College Full-Stack Project*

</div>
