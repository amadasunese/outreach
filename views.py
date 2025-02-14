# from flask import render_template, request, redirect, url_for, jsonify, flash
# from app import app
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from models import School, Student, Attendance, Lesson, Assessment, Facilitator, User
from extensions import db, login_manager
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from flask import jsonify
from auth import admin_required



auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/register', methods=['GET', 'POST'])
# @login_required
# @admin_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        is_admin = form.is_admin.data

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Registration successful! {"Admin privileges granted." if is_admin else "User registered successfully."}', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/users')
@admin_required
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@auth.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        
        # Convert 'on' to True and empty to False
        user.is_admin = request.form.get('is_admin') == 'on'
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('auth.users'))
    
    return render_template('edit_user.html', user=user)



@auth.route('/delete_user/<int:user_id>')
@admin_required
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()


# Dashboard (Protected Route)
@auth.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.username}! <br> <a href='{url_for('auth.logout')}'>Logout</a>"





@auth.route('/schools')
@login_required
def schools():
    all_schools = School.query.all()
    return render_template('schools.html', schools=all_schools)

@auth.route('/add_school', methods=['GET', 'POST'])
@login_required
@admin_required
def add_school():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        if name and address and phone:
            new_school = School(name=name, address=address, phone=phone)
            db.session.add(new_school)
            db.session.commit()
            flash("School added successfully!", "success")
        else:
            flash("All fields are required!", "error")
        
        return redirect(url_for('auth.schools'))

    return render_template('add_school.html')

@auth.route('/facilitators')
def facilitators():
    all_facilitators = Facilitator.query.all()
    all_schools = School.query.all()
    return render_template('facilitators.html', facilitators=all_facilitators, schools=all_schools)

@auth.route('/add_facilitator', methods=['GET', 'POST'])
@login_required
@admin_required
def add_facilitator():
    schools = School.query.all()
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        school_id = request.form.get('school_id')

        if name and phone and school_id:
            new_facilitator = Facilitator(name=name, phone=phone, school_id=int(school_id))
            db.session.add(new_facilitator)
            db.session.commit()
            flash("Facilitator added successfully!", "success")
        else:
            flash("All fields are required!", "error")

        return redirect(url_for('auth.facilitators'))

    return render_template('add_facilitator.html', schools=schools)

# @auth.route('/students')
# def students():
#     all_students = Student.query.all()

#     for student in all_students:
#         if student.program_type == 'SCHOOL_OUTREACH' and student.student_class:
#             classes.add(student.student_class)
#         elif student.program_type == 'CENTER_MEETING' and student.center_year:
#             classes.add(f"Year {student.center_year}")
    
#     print(classes)

#     for student in all_students:
#         print(student)  # Debugging

#     all_schools = School.query.all()
#     return render_template('students.html', students=all_students, schools=all_schools)

# @auth.route('/students')
# def students():
#     all_students = Student.query.all()
#     classes = set()  # Initialize an empty set

#     for student in all_students:
#         if student.program_type == 'SCHOOL_OUTREACH' and student.student_class:
#             classes.add(student.student_class)
#         elif student.program_type == 'CENTER_MEETING' and student.center_year:
#             classes.add(f"Year {student.center_year}")

#     print("Classes found:", classes)  # Debugging output
#     for student in all_students:
#         print(f"ID: {student.id}, Program Type: {student.program_type}, Class: {student.student_class}, Center Year: {student.center_year}")

#     all_schools = School.query.all()
#     return render_template('students.html', students=all_students, schools=all_schools)

@auth.route('/students')
def students():
    all_students = Student.query.all()

    for student in all_students:
        print(f"ID: {student.id}, Name: {student.name}, Program Type: {student.program_type}, Class: {student.student_class}, Center Year: {student.center_year}")

    all_schools = School.query.all()
    return render_template('students.html', students=all_students, schools=all_schools)


# @auth.route('/add_student', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def add_student():
#     schools = School.query.all()
#     if request.method == 'POST':
#         name = request.form.get('name')
#         age = request.form.get('age')
#         school_id = request.form.get('school_id')

#         if name and age and school_id:
#             new_student = Student(name=name, age=int(age), school_id=int(school_id))
#             db.session.add(new_student)
#             db.session.commit()
#             flash("Student added successfully!", "success")
#         else:
#             flash("All fields are required!", "error")

#         return redirect(url_for('auth.students'))

#     return render_template('add_student.html', schools=schools)




@auth.route('/add_student', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    schools = School.query.all()
    form_errors = []

    if request.method == 'POST':
        name = request.form.get('name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        program_type = request.form.get('program_type')
        school_id = request.form.get('school_id')
        student_class = request.form.get('student_class')
        center_year = request.form.get('center_year')
        address = request.form.get('address')
        phone = request.form.get('phone')
        father_name = request.form.get('father_name')
        father_occupation = request.form.get('father_occupation')
        father_phone = request.form.get('father_phone')
        mother_name = request.form.get('mother_name')
        mother_occupation = request.form.get('mother_occupation')
        mother_phone = request.form.get('mother_phone')
        introduced_by = request.form.get('introduced_by')
        consent = request.form.get('consent')  # Get consent value

        # Validation
        if not name:
            form_errors.append("Name is required.")
        if not age:
            form_errors.append("Age is required.")

        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be greater than 0.")
        except ValueError:
            form_errors.append("Invalid age.")

        if not program_type:
            form_errors.append("Program Type is required.")

        if program_type == 'SCHOOL_OUTREACH' and not school_id:
            form_errors.append("School is required for School Outreach students.")
        elif program_type == 'CENTER_MEETING' and not center_year:
            form_errors.append("Center Year is required for Center students.")

        # Convert school_id and center_year to integers if they exist
        try:
            school_id = int(school_id) if school_id else None
            center_year = int(center_year) if center_year else None
        except ValueError:
            form_errors.append("Invalid School or Center Year")

        consent = True if consent == 'on' else False  # Convert checkbox value to boolean

        if not form_errors:
            try:
                if program_type == 'SCHOOL_OUTREACH':
                    new_student = Student(name=name, sex=sex, age=age, school_id=school_id, program_type=program_type, student_class=student_class, address=address, phone=phone, father_name=father_name, father_occupation=father_occupation, father_phone=father_phone, mother_name=mother_name, mother_occupation=mother_occupation, mother_phone=mother_phone, introduced_by=introduced_by, consent=consent)
                elif program_type == 'CENTER_MEETING':
                    new_student = Student(name=name, sex=sex, age=age, center_year=center_year, program_type=program_type, address=address, phone=phone, father_name=father_name, father_occupation=father_occupation, father_phone=father_phone, mother_name=mother_name, mother_occupation=mother_occupation, mother_phone=mother_phone, introduced_by=introduced_by, consent=consent)

                db.session.add(new_student)
                db.session.commit()
                flash("Student added successfully!", "success")
                return redirect(url_for('auth.students'))
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {str(e)}", "error")
        else:
            for error in form_errors:
                flash(error, "error")

    return render_template('add_student.html', schools=schools)


# Center girls
@auth.route('/center_girls')
def center_girls():
    all_students = Student.query.filter_by(program_type='CENTER_MEETING').all()
    return render_template('center_girls.html', students=all_students)



@auth.route('/edit_center_girls')
def edit_center_girls():
    students = Student.query.filter_by(program_type='CENTER_MEETING').all()
    return render_template('edit_center_girls.html', students=students)

@auth.route('/edit_center_girl/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_center_girl(id):
    student = Student.query.get_or_404(id)
    form_errors = []

    if request.method == 'POST':
        student.center_year = request.form.get('center_year')
        student.address = request.form.get('address')
        student.phone = request.form.get('phone')
        student.father_name = request.form.get('father_name')
        student.father_occupation = request.form.get('father_occupation')
        student.father_phone = request.form.get('father_phone')
        student.mother_name = request.form.get('mother_name')
        student.mother_occupation = request.form.get('mother_occupation')
        student.mother_phone = request.form.get('mother_phone')
        student.introduced_by = request.form.get('introduced_by')
        student.consent = True if request.form.get('consent') == 'on' else False  # Convert checkbox value to boolean

    try:
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('auth.center_girls'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")

@auth.route(f'/delete_center_girl/<int:id>')
def delete_center_girl(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('auth.center_girls'))
    

# Outreach Girls
@auth.route('/outreach_girls')
def outreach_girls():
    all_students = Student.query.filter_by(program_type='SCHOOL_OUTREACH').all()
    return render_template('outreach_girls.html', outreach_students=all_students)



@auth.route('/edit_outrach')
def edit_outreach_girls():
    students = Student.query.filter_by(program_type='SCHOOL_OUTREACH').all()
    return render_template('edit_outreach_girls.html', students=students)

@auth.route('/edit_outreach_girl/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_outreach_girl(id):
    student = Student.query.get_or_404(id)
    form_errors = []

    if request.method == 'POST':
        student.center_year = request.form.get('outreach-school')
        student.address = request.form.get('address')
        student.phone = request.form.get('phone')
        student.father_name = request.form.get('father_name')
        student.father_occupation = request.form.get('father_occupation')
        student.father_phone = request.form.get('father_phone')
        student.mother_name = request.form.get('mother_name')
        student.mother_occupation = request.form.get('mother_occupation')
        student.mother_phone = request.form.get('mother_phone')
        student.introduced_by = request.form.get('introduced_by')
        student.consent = True if request.form.get('consent') == 'on' else False  # Convert checkbox value to boolean

    try:
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('auth.outreach_girls'))
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")

@auth.route(f'/delete_outreach_girl/<int:id>')
def delete_outreach_girl(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('auth.outreach_girls'))









@auth.route('/lessons')
def lessons():
    lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=lessons)

# @auth.route('/add_lesson', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def add_lesson():
#     if request.method == 'POST':
#         # ... get data from the form
#         data = request.form.to_dict()
#         last_lesson = Lesson.query.order_by(Lesson.id.desc()).first()
#         if last_lesson:
#             week_number = str(last_lesson.week + 1)
#         else:
#             week_number = 1
#         week_mapping = {
#             1: "One",
#             2: "Two",
#             3: "Three",
#             # Add more mappings as needed
#         }
#         data['week'] = week_mapping.get(week_number, str(week_number))
#         lesson = Lesson(**data)
#         db.session.add(lesson)
#         db.session.commit()
#         return redirect(url_for('auth.lessons'))
#     return render_template('add_lesson.html')

from models import ProgramType
@auth.route('/add_lesson', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lesson():
    if request.method == 'POST':
        data = request.form.to_dict()

        # Get last lesson week number
        last_lesson = Lesson.query.order_by(Lesson.id.desc()).first()
        print(last_lesson)
        week_number = last_lesson.week + 1 if last_lesson else 1  # Keep as integer

        # Week number mapping
        week_mapping = {
            1: "One",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            # Add more mappings if needed
        }

        data['week'] = week_mapping.get(week_number, str(week_number))

        # Ensure program_type is a valid enum
        program_type = data.get("program_type")
        if program_type not in ["SCHOOL_OUTREACH", "CENTER_MEETING"]:
            flash("Invalid program type!", "error")
            return redirect(url_for('auth.add_lesson'))

        data['program_type'] = ProgramType[program_type]  # Convert string to Enum

        lesson = Lesson(**data)
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('auth.lessons'))

    return render_template('add_lesson.html')


@auth.route('/edit_lesson/<int:lesson_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    if request.method == 'POST':
        #... update lesson details
        #... then redirect to lessons page
        pass

    return render_template('edit_lesson.html', lesson=lesson)

@auth.route('/attendance')
def attendances():
    attendances = Attendance.query.all()
    students = Student.query.all()
    return render_template('attendance.html', attendances=attendances, students=students)

@auth.route('/add_attendance', methods=['GET', 'POST'])
@login_required
@admin_required
def add_attendance():
    students = Student.query.all()
    if request.method == 'POST':
        # ... get data from the form
        attendance = Attendance(**data)
        db.session.add(attendance)
        db.session.commit()
        return redirect(url_for('auth.attendances'))
    return render_template('add_attendance.html', students=students)

@auth.route('/mark_attendance', methods=['POST'])
@login_required
@admin_required
def mark_attendance():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_attendance = Attendance(**data)
    db.session.add(new_attendance)
    db.session.commit()
    return jsonify({"message": "Attendance recorded!"})

@auth.route('/assessments')
def assessments():
    assessments = Assessment.query.all()
    students = Student.query.all()
    return render_template('assessments.html', assessments=assessments, students=students)

@auth.route('/add_assessment', methods=['GET', 'POST'])
@login_required
@admin_required
def add_assessment():
    students = Student.query.all()
    if request.method == 'POST':
        # get data from the form
        data = request.form.to_dict()
        data['student_id'] = int(data['student_id'])
        data['obtainable_score'] = int(data['obtainable_score'])
        data['score'] = int(data['score'])

        
        assessment = Assessment(**data)
        db.session.add(assessment)
        db.session.commit()
        return redirect(url_for('auth.assessments'))
    return render_template('add_assessment.html', students=students)

@auth.route('/record_assessment', methods=['POST'])
@login_required
@admin_required
def record_assessment():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_assessment = Assessment(**data)
    db.session.add(new_assessment)
    db.session.commit()
    return jsonify({"message": "Assessment recorded!"})

@auth.route('/check_graduation/<int:student_id>', methods=['GET'])
def check_graduation(student_id):
    total_lessons = db.session.query(Lesson).count()
    attended_lessons = db.session.query(Attendance).filter_by(student_id=student_id, present=True).count()
    student_assessments = db.session.query(Assessment).filter_by(student_id=student_id).all()
    
    avg_score = (
        sum(a.score for a in student_assessments) / sum(a.obtainable_score for a in student_assessments) * 100
        if student_assessments else 0
    )
    
    attendance_percentage = (attended_lessons / total_lessons) * 100 if total_lessons else 0
    qualifies = attendance_percentage >= 70 and avg_score >= 70
    
    return jsonify({
        "student_id": student_id,
        "attendance_percentage": attendance_percentage,
        "average_score": avg_score,
        "qualified": qualifies
    })

    return render_template('graduation.html', student_id=student_id)

@auth.route('/graduation', methods=['GET', 'POST'])
def graduation():
    students = Student.query.all()
    return render_template('graduation.html', students=students)


@auth.route("/")
def graduation_eligibility():
    students = Student.query.all()  # Fetch all students
    return render_template("graduation.html", students=students)


@auth.route("/get_student_data/<int:student_id>")
def get_student_data(student_id):
    student_attendance = Attendance.query.filter_by(student_id=student_id).first()
    student_assessment = Assessment.query.filter_by(student_id=student_id).first()

    return jsonify({
        "attendance": student_attendance.percentage if student_attendance else 0,
        "assessment": student_assessment.score if student_assessment else 0
    })
