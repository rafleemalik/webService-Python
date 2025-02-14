from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a unique and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

# User authentication logic
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate the user
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Login successful
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login successful!", "success")
            return redirect(url_for('student'))
        else:
            # Login failed
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session
    flash("Logged out successfully.", "info")
    return redirect(url_for('index'))  # Redirect to the login page

# Students route
@app.route('/students')
def student():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    # Fetch students from the database
    students = Student.query.all()
    return render_template('student.html', students=students)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Add student route
@app.route('/add', methods=['POST'])
def add_student():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    new_student = Student(name=name, age=age, grade=grade)
    db.session.add(new_student)
    db.session.commit()
    flash("Student added successfully!", "success")
    return redirect(url_for('student'))

# Delete student route
@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully!", "success")
    return redirect(url_for('student'))

# Edit student route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.grade = request.form['grade']
        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('student'))
    
    return render_template('edit.html', student=student)

# Create user route
@app.route('/users/create', methods=['GET', 'POST'])
def create_user_form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('create_user.html', error="Both fields are required!")

        if User.query.filter_by(username=username).first():
            return render_template('create_user.html', error="User already exists!")

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("User created successfully!", "success")
        return redirect(url_for('index'))

    return render_template('create_user.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default admin user if not already present
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('admin123')  # Default password
            db.session.add(admin_user)
            db.session.commit()
    app.run(host='0.0.0.0', port=8000, debug=True)
