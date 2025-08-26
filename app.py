from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/student_mgmt'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

# Allowed courses
ALLOWED_COURSES = ['CS','AI','AIML','DS','BS','CE','CI','EC','Civil','Mech']

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usn = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# View all students
@app.route('/index')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].strip()
        usn = request.form['usn'].strip()
        course = request.form['course']
        semester = request.form['semester']

        # SERVER-SIDE VALIDATION
        if not re.fullmatch(r"[A-Za-z. ]+", name):
            flash("Name can only contain letters, spaces, and dots.", "error")
            return redirect(url_for('add_student'))

        if course not in ALLOWED_COURSES:
            flash("Invalid course selected.", "error")
            return redirect(url_for('add_student'))

        try:
            semester = int(semester)
            if semester < 1 or semester > 8:
                flash("Semester must be between 1 and 8.", "error")
                return redirect(url_for('add_student'))
        except ValueError:
            flash("Invalid semester.", "error")
            return redirect(url_for('add_student'))

        new_student = Student(name=name, usn=usn, course=course, semester=semester)
        db.session.add(new_student)
        db.session.commit()
        flash("Student added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add.html')

# Edit student
@app.route('/edit/<int:student_id>', methods=['GET','POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        name = request.form['name'].strip()
        usn = request.form['usn'].strip()
        course = request.form['course']
        semester = request.form['semester']

        # SERVER-SIDE VALIDATION
        if not re.fullmatch(r"[A-Za-z. ]+", name):
            flash("Name can only contain letters, spaces, and dots.", "error")
            return redirect(url_for('edit_student', student_id=student.id))

        if course not in ALLOWED_COURSES:
            flash("Invalid course selected.", "error")
            return redirect(url_for('edit_student', student_id=student.id))

        try:
            semester = int(semester)
            if semester < 1 or semester > 8:
                flash("Semester must be between 1 and 8.", "error")
                return redirect(url_for('edit_student', student_id=student.id))
        except ValueError:
            flash("Invalid semester.", "error")
            return redirect(url_for('edit_student', student_id=student.id))

        student.name = name
        student.usn = usn
        student.course = course
        student.semester = semester
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

# Delete student
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True)
