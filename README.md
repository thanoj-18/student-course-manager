# Student Course Manager

A simple Flask web application for managing students, courses, and enrollments.

## Features

- **Students**: Create, read, update, delete students with roll numbers
- **Courses**: Create, read, update, delete courses with codes and descriptions
- **Enrollments**: Enroll students in courses, withdraw from courses
- **Views**: List all students/courses, view details with enrolled items

## Tech Stack

- **Backend**: Flask + Flask-SQLAlchemy
- **Database**: SQLite (file-based)
- **Frontend**: Server-rendered Jinja2 templates with minimal CSS

## Project Structure

```
student-course-manager/
├── app.py                 # Main Flask application
├── static/
│   └── style.css          # Styling
├── templates/
│   ├── index.html         # Student list homepage
│   ├── create_student.html
│   ├── create_course.html
│   ├── student_detail.html
│   ├── course_detail.html
│   ├── update_student.html
│   ├── update_course.html
│   ├── student_exists.html
│   ├── course_exists.html
│   └── error.html
└── instance/
    └── database.sqlite3   # SQLite database (auto-created)
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone or navigate to the project
cd student-course-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy

# Run the application
python app.py
```

The app will be available at `http://localhost:5000`

## Routes

| Route                                  | Method   | Description                        |
| -------------------------------------- | -------- | ---------------------------------- |
| `/`                                  | GET      | Home - list all students           |
| `/student/create`                    | GET/POST | Add new student                    |
| `/student/<id>`                      | GET      | View student + enrolled courses    |
| `/student/<id>/update`               | GET/POST | Update student + enroll in courses |
| `/student/<id>/delete`               | GET      | Delete student                     |
| `/courses`                           | GET      | List all courses                   |
| `/course/create`                     | GET/POST | Add new course                     |
| `/course/<id>`                       | GET      | View course + enrolled students    |
| `/course/<id>/update`                | GET/POST | Update course                      |
| `/course/<id>/delete`                | GET      | Delete course                      |
| `/student/<id>/withdraw/<course_id>` | GET      | Withdraw student from course       |

## Database Models

- **Student**: `student_id`, `roll_number` (unique), `first_name`, `last_name`
- **Course**: `course_id`, `course_code` (unique), `course_name`, `course_description`
- **Enrollments**: `enrollment_id`, `estudent_id` (FK), `ecourse_id` (FK)

## Planned Improvements

### 🔐 Authentication & Authorization

- [ ] User registration & login (Flask-Login or JWT)
- [ ] Role-based access (Admin, Student, Instructor)
- [ ] Protected routes & session management
- [ ] Password hashing (bcrypt)

### ✅ Validation & Error Handling

- [ ] Server-side validation (WTForms or Marshmallow)
  - Roll number format validation
  - Course code format validation
  - Required field enforcement
  - Duplicate detection with user-friendly messages
- [ ] Client-side validation (HTML5 + JavaScript)
- [ ] Global error handlers (404, 500, validation errors)
- [ ] Flash messages for success/error feedback

### 🎨 UI/UX Enhancements

- [ ] Responsive design for mobile
- [ ] Confirmation modals for delete actions
- [ ] Search & filter on list pages
- [ ] Pagination for large datasets
