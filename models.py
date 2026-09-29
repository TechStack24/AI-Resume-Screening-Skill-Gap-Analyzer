from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy database object
db = SQLAlchemy()


# ---------------- USER MODEL ----------------
# Stores user credentials (email, username, hashed password)
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)  # Hashed password string

    # One-to-Many relationship with Analysis records
    analyses = db.relationship("Analysis", backref="user", lazy=True)


# ---------------- ANALYSIS MODEL ----------------
# Stores candidate resume screening results
class Analysis(db.Model):
    __tablename__ = "analysis"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    resume_filename = db.Column(db.String(300))
    job_title = db.Column(db.String(200))

    matched_skills = db.Column(db.Text)   # Comma-separated string: "python,sql,flask"
    missing_skills = db.Column(db.Text)   # Comma-separated string: "docker,aws"
    match_percentage = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

