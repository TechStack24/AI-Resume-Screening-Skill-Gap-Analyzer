# 📄 ResumeAI — AI Resume Screening & Skill Gap Analyzer

> An intelligent web application for resume screening, ATS match calculation, skill extraction, and skill gap analysis.

---

## 🌟 Features

### 🤖 AI Resume Screening

* Upload candidate resumes in PDF format.
* Automatically extract resume text using `pdfplumber`.
* Identify technical and soft skills from resumes.
* Compare candidate skills with job requirements.

### 📊 ATS Match & Skill Gap Analysis

* Calculate candidate ATS match percentage.
* Display matched and missing skills.
* Categorize candidates based on their match score.
* Provide recommendations based on skill gaps.

### 📈 Analytics Dashboard

* Total resume screenings.
* Average match percentage.
* Best candidate score.
* Search and filter previous analyses.
* View and delete analysis reports.

### 🔐 Authentication

* User registration and login.
* Secure password hashing using Werkzeug.
* Session-based authentication with Flask-Login.
* Forgot password functionality.

### 👤 User Profile

* View user information.
* Track screening statistics.
* View recent activity.
* Manage account credentials.

### 🖨️ Reports

* View detailed resume analysis reports.
* Print reports.
* Export reports as PDF using browser print functionality.

---

## 🛠️ Technology Stack

| Category          | Technology               |
| ----------------- | ------------------------ |
| Backend           | Python, Flask            |
| Frontend          | HTML5, CSS3, Bootstrap 5 |
| Database          | SQLite                   |
| ORM               | Flask-SQLAlchemy         |
| Authentication    | Flask-Login              |
| Password Security | Werkzeug                 |
| PDF Processing    | pdfplumber               |
| Production Server | Gunicorn                 |
| Deployment        | Vercel                   |
| Version Control   | Git & GitHub             |

---

## 📂 Project Structure

```text
resume_screener/
│
├── app.py
├── models.py
├── skills_data.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── dashboard.html
│   ├── upload_resume.html
│   ├── result.html
│   └── profile.html
│
├── uploads/
│
└── instance/
    └── database.db
```

---

## 🗄️ Database

The application uses **SQLite** with **Flask-SQLAlchemy**.

### User

Stores registered user information such as:

* User ID
* Email
* Username
* Hashed Password

### Analysis

Stores resume screening information such as:

* Resume filename
* Job title
* Matched skills
* Missing skills
* Match percentage
* Analysis date

---

## 🔒 Security

The application includes:

* Secure password hashing with Werkzeug.
* Flask-Login authentication.
* Secure filename handling for uploaded PDFs.
* User-specific analysis access.
* SQLAlchemy ORM for database operations.

> Never commit sensitive information such as passwords, API keys, or secret environment variables to GitHub.

---

## 🌐 Live Application

🚀 **[Open ResumeAI](https://ai-resume-screening-skill-gap-analy.vercel.app)**

💻 **GitHub:**
https://github.com/ariz440/Resume-Scanner

---

## 🎯 Project Goal

ResumeAI aims to simplify the recruitment and resume screening process by helping users quickly understand:

* How well a resume matches a job description.
* Which required skills are already present.
* Which skills are missing.
* How strong the candidate's overall profile is.

---

## 👨‍💻 Author

**Ariz Mondal**

Built with ❤️ using Python, Flask, Bootstrap, SQLite and modern web technologies.

---

## 📄 License

This project is licensed under the **MIT License**.
