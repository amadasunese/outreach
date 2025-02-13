from extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum


class ProgramType(Enum):
    SCHOOL_OUTREACH = "School Outreach"
    CENTER_MEETING = "Center Meeting"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    facilitators = db.relationship('Facilitator', backref='school', lazy=True)
    students = db.relationship('Student', backref='school', lazy=True)


class Facilitator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)  # Optional for center facilitators
    center_assigned = db.Column(db.Boolean, default=False)  # True if assigned to center girls


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(10))
    age = db.Column(db.Integer)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=True)  # Nullable for center students
    program_type = db.Column(db.Enum(ProgramType), nullable=False)
    
    # School outreach students have classes (e.g., JSS1, JSS2, etc.)
    student_class = db.Column(db.String(50), nullable=True)

    # Center girls have structured Year 1, Year 2, Year 3 (then graduation)
    center_year = db.Column(db.Integer, nullable=True)

    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    father_name = db.Column(db.String(100))
    father_occupation = db.Column(db.String(100))
    father_phone = db.Column(db.String(20))
    mother_name = db.Column(db.String(100))
    mother_occupation = db.Column(db.String(100))
    mother_phone = db.Column(db.String(20))
    introduced_by = db.Column(db.String(100))
    consent = db.Column(db.Boolean, default=False)

    # Relationships
    assessments = db.relationship('Assessment', backref='student', lazy=True)
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    present = db.Column(db.Boolean, nullable=False)


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    program_type = db.Column(db.Enum(ProgramType), nullable=False)


class AssessmentType(Enum):
    GENERAL = "General Assessment"
    CENTER_PROMOTION = "Center Promotion Assessment"


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    obtainable_score = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)
    assessment_type = db.Column(db.Enum(AssessmentType), nullable=False)
