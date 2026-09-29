import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pdfplumber

from models import db, User, Analysis
from skills_data import extract_skills, compare_skills

# ---------------- APP CONFIG ----------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "prod-secret-key-change-in-env-98234")

# SQLite database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure both uploads and instance folders exist
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.instance_path, exist_ok=True)

# Initialize database
db.init_app(app)

# ---------------- LOGIN MANAGER CONFIG ----------------
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


def auto_migrate_db():
    """Ensures database tables and email column exist."""
    with app.app_context():
        try:
            db.create_all()
            import sqlite3
            # Check both instance folder and root folder
            db_paths = [
                os.path.join(app.instance_path, "database.db"),
                os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance", "database.db"),
                os.path.join(os.path.abspath(os.path.dirname(__file__)), "database.db"),
                "instance/database.db",
                "database.db"
            ]
            for path in set(db_paths):
                if os.path.exists(path):
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("PRAGMA table_info(user)")
                    columns = [info[1] for info in cursor.fetchall()]
                    if columns and "email" not in columns:
                        cursor.execute("ALTER TABLE user ADD COLUMN email VARCHAR(150)")
                        cursor.execute("UPDATE user SET email = username || '@example.com' WHERE email IS NULL OR email = ''")
                        conn.commit()
                    conn.close()
        except Exception as e:
            print("Migration notice:", e)


# Run migration
auto_migrate_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not email or "@" not in email:
            flash("Please provide a valid email address.", "danger")
            return redirect(url_for("register"))

        if not password or len(password) < 4:
            flash("Password must be at least 4 characters long.", "danger")
            return redirect(url_for("register"))

        if not username:
            username = email.split("@")[0]

        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("An account with this email already exists. Please log in.", "danger")
                return redirect(url_for("login"))

            # Hash password securely
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, username=username, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            # Automatically log in the user after registration
            login_user(new_user)
            flash(f"Welcome to ResumeAI, {new_user.username or new_user.email}!", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred during registration: {e}", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_or_user = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email_or_user or not password:
            flash("Please enter both your email/username and password.", "danger")
            return redirect(url_for("login"))

        try:
            # Allow login by email or username
            user = User.query.filter(
                (User.email == email_or_user) | (User.username == email_or_user)
            ).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash(f"Welcome back, {user.username or user.email}!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid email/username or password.", "danger")
        except Exception as e:
            flash("Unable to sign in. Please verify your credentials or reset your password.", "danger")

    return render_template("login.html")


# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not email or "@" not in email:
            flash("Please enter a valid registered email address.", "danger")
            return redirect(url_for("forgot_password"))

        try:
            user = User.query.filter_by(email=email).first()

            if not user:
                flash("No account found with this email address.", "danger")
                return redirect(url_for("forgot_password"))

            if not new_password or len(new_password) < 4:
                flash("Password must be at least 4 characters long.", "danger")
                return redirect(url_for("forgot_password"))

            if new_password != confirm_password:
                flash("New password and confirm password do not match.", "danger")
                return redirect(url_for("forgot_password"))

            # Update password hash
            user.password = generate_password_hash(new_password)
            db.session.commit()

            flash("Your password has been successfully reset! You can now log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error resetting password: {e}", "danger")
            return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    analyses = Analysis.query.filter_by(user_id=current_user.id)\
        .order_by(Analysis.created_at.desc()).all()
    return render_template("dashboard.html", analyses=analyses)


# ---------------- UPLOAD & ANALYZE RESUME ----------------
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")
        resume_file = request.files.get("resume")

        if not resume_file or resume_file.filename == "":
            flash("Please select a PDF resume file to upload.", "danger")
            return redirect(url_for("upload_resume"))

        filename = secure_filename(resume_file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        resume_file.save(filepath)

        # Extract text from PDF
        resume_text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        resume_text += page_text + "\n"
        except Exception as e:
            flash(f"Error reading PDF file: {e}", "danger")
            return redirect(url_for("upload_resume"))

        # Skill extraction and comparison
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        matched, missing, percentage = compare_skills(resume_skills, job_skills)

        # Save analysis result to database
        new_analysis = Analysis(
            user_id=current_user.id,
            resume_filename=filename,
            job_title=job_title,
            matched_skills=",".join(matched),
            missing_skills=",".join(missing),
            match_percentage=percentage,
        )
        db.session.add(new_analysis)
        db.session.commit()

        flash("Resume analysis completed successfully!", "success")
        return redirect(url_for("result", analysis_id=new_analysis.id))

    return render_template("upload_resume.html")


# ---------------- RESULT PAGE ----------------
@app.route("/result/<int:analysis_id>")
@login_required
def result(analysis_id):
    analysis = db.session.get(Analysis, analysis_id)

    if not analysis or analysis.user_id != current_user.id:
        flash("Analysis result not found or access denied.", "danger")
        return redirect(url_for("dashboard"))

    matched = analysis.matched_skills.split(",") if analysis.matched_skills else []
    missing = analysis.missing_skills.split(",") if analysis.missing_skills else []

    return render_template("result.html", analysis=analysis, matched=matched, missing=missing)


# ---------------- DELETE ANALYSIS ----------------
@app.route("/delete/<int:analysis_id>", methods=["POST"])
@login_required
def delete_analysis(analysis_id):
    analysis = db.session.get(Analysis, analysis_id)

    if not analysis or analysis.user_id != current_user.id:
        flash("Analysis not found or permission denied.", "danger")
        return redirect(url_for("dashboard"))

    # Delete PDF file from uploads folder if it exists
    if analysis.resume_filename:
        try:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], analysis.resume_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass

    db.session.delete(analysis)
    db.session.commit()

    flash(f"Analysis report for '{analysis.job_title}' was successfully deleted.", "success")
    return redirect(url_for("dashboard"))


# ---------------- USER PROFILE ----------------
@app.route("/profile")
@login_required
def profile():
    analyses = Analysis.query.filter_by(user_id=current_user.id)\
        .order_by(Analysis.created_at.desc()).all()

    total_count = len(analyses)
    avg_score = 0
    best_score = 0

    if total_count > 0:
        scores = [a.match_percentage for a in analyses if a.match_percentage is not None]
        if scores:
            avg_score = round(sum(scores) / len(scores), 1)
            best_score = max(scores)

    return render_template(
        "profile.html",
        analyses=analyses,
        total_count=total_count,
        avg_score=avg_score,
        best_score=best_score
    )


# ---------------- ERROR HANDLERS ----------------
@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Internal Server Error: {e}")
    flash("A temporary server error occurred. Please try again.", "danger")
    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found_error(e):
    flash("The requested page was not found.", "warning")
    return redirect(url_for("home"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)




