# AI Resume Screening & Skill Gap Analyzer

A modern SaaS web application built with Flask and Bootstrap 5 for intelligent resume screening, ATS match calculation, and skill gap identification.

---

## 🌟 Key Features
- **User Authentication**: Secure user registration and login system (`Flask-Login`, password hashing).
- **PDF Parsing**: Automated text and entity extraction from candidate PDF resumes (`pdfplumber`).
- **Skill Extraction & Matching**: Real-time keyword extraction against job requirements.
- **Visual Analytics**: Interactive match percentage ring, matched/missing skill badges, and AI recommendations.
- **Analytics Dashboard**: KPI statistics (Total Screenings, Average Match %, Best Score) and search/filter.
- **Analysis History Management**: Real-time search, report inspection, and report deletion.
- **User Profile Details**: Dedicated profile overview with user screening metrics and activity.

---

## 🚀 Quickstart Guide

### 1. Check Python Installation
Make sure Python 3.9+ is installed:
```bash
python --version
```

### 2. Navigate to Project Directory
```bash
cd resume_screener
```

### 3. Setup Virtual Environment (Recommended)
```bash
python -m venv venv
```
Activate the environment:
- **Windows**: `venv\Scripts\activate`
- **macOS / Linux**: `source venv/bin/activate`

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📖 How to Use
1. **Register**: Create an account with your username and password.
2. **Sign In**: Log into your personal dashboard.
3. **Screen a Resume**:
   - Enter the target Job Title.
   - Paste the Job Description or pick a quick preset (*Python Dev*, *Frontend*, *Data Science*, *DevOps*).
   - Drag & drop the candidate's PDF resume.
4. **View Assessment**: Inspect the match score, matched skills, missing skill gaps, and AI recommendations.
5. **Manage History**: Search past analyses, print reports, or delete outdated screenings.

---

## 🛠️ Tech Stack
- **Backend**: Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Database**: SQLite
- **PDF Extraction**: pdfplumber
- **Frontend**: HTML5, Bootstrap 5.3, Custom SaaS CSS, Bootstrap Icons

