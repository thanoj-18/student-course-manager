from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"

## Configure SQL Alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

## Database Modelss -------------------------------------------


class Student(db.Model):

    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_description = db.Column(db.String(200))


class Enrollments(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)
    estudent_id = db.Column(
        db.Integer, db.ForeignKey("student.student_id"), nullable=False
    )
    ecourse_id = db.Column(
        db.Integer, db.ForeignKey("course.course_id"), nullable=False
    )

    ## Relationships
    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")


@app.route("/")
def home():

    students = Student.query.all()

    return render_template("index.html", students=students), 200


@app.route("/student/create", methods=["GET", "POST"])
def add_student():
    if request.method == "GET":
        return render_template("create_student.html"), 200

    roll = request.form["roll"]
    f_name = request.form["f_name"]
    l_name = request.form["l_name"]

    st = Student.query.filter_by(roll_number=roll).first()

    if st:
        return render_template("student_exists.html", roll_number=roll), 200

    student = Student(roll_number=roll, first_name=f_name, last_name=l_name)

    db.session.add(student)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/student/<int:student_id>")
def view_student(student_id):

    student = Student.query.get(student_id)

    if student is None:
        return "Student not found", 404

    enrollments = (
        db.session.query(Enrollments, Course)
        .join(Course, Enrollments.ecourse_id == Course.course_id)
        .filter(Enrollments.estudent_id == student_id)
        .all()
    )

    return render_template(
        "student_detail.html", student=student, enrollments=enrollments
    ), 200


@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
    student = Student.query.get(student_id)
    enrolled_course_ids = db.session.query(Enrollments.ecourse_id).filter_by(estudent_id=student_id)
    courses = Course.query.filter(~Course.course_id.in_(enrolled_course_ids)).all()

    if request.method == "GET":
        return render_template("update_student.html", student=student, courses=courses), 200

    f_name = request.form["f_name"]
    l_name = request.form["l_name"]
    course_id = request.form.get("course")

    student.first_name = f_name
    student.last_name = l_name

    if course_id:
        existing = Enrollments.query.filter_by(
            estudent_id=student_id, ecourse_id=course_id
        ).first()

        if not existing:
            enrollment = Enrollments(estudent_id=student_id, ecourse_id=course_id)
            db.session.add(enrollment)

    db.session.commit()
    return redirect(url_for("home"))


@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student:
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for("home"))


##### Courses


@app.route("/courses")
def view_courses():

    courses = Course.query.all()

    return render_template("courses.html", courses=courses), 200


@app.route("/course/create", methods=["GET", "POST"])
def add_course():
    if request.method == "GET":
        return render_template("create_course.html"), 200

    course_code = request.form["code"]
    course_name = request.form["c_name"]
    course_desc = request.form["desc"]

    c = Course.query.filter_by(course_code=course_code).first()

    if c:
        return render_template("course_exists.html", course_code=course_code), 200

    course = Course(
        course_code=course_code, course_name=course_name, course_description=course_desc
    )

    db.session.add(course)
    db.session.commit()

    return redirect(url_for("view_courses"))


@app.route("/course/<int:course_id>/update", methods=["GET", "POST"])
def update_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()

    if request.method == "GET":
        return render_template("update_course.html", course=course), 200

    course.course_name = request.form["c_name"]
    course.course_description = request.form["desc"]

    db.session.commit()

    return redirect(url_for("view_courses"))


@app.route("/course/<int:course_id>/delete")
def delete_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()

    if course:
        Enrollments.query.filter_by(ecourse_id=course_id).delete()
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/course/<int:course_id>")
def view_course(course_id):
    course = Course.query.filter_by(course_id=course_id).first()

    if course is None:
        return "Course not found", 404

    enrollments = (
        db.session.query(Enrollments, Student)
        .join(Student, Enrollments.estudent_id == Student.student_id)
        .filter(Enrollments.ecourse_id == course_id)
        .all()
    )

    return render_template(
        "course_detail.html", course=course, enrollments=enrollments
    ), 200


## Withdraw -----


@app.route("/student/<int:student_id>/withdraw/<int:course_id>")
def withdraw_course(student_id, course_id):
    enrollment = Enrollments.query.filter_by(
        estudent_id=student_id, ecourse_id=course_id
    ).first()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()

    return redirect(url_for("view_student", student_id=student_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
