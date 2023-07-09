from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Route for the home page


@app.route('/')
def index():
    return render_template('index.html')

# Route for the registration form submission


@app.route('/register', methods=['POST'])
def register():

    # Validate the registration form data
    if not User.validate_register(request.form):
        return redirect('/')

    # Prepare the user data to be saved
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    # Save the user data to the database
    id = User.save(data)

    # Store the user's ID in the session
    session['user_id'] = id

    # Redirect to the dashboard
    return redirect('/dashboard')

# Route for the login form submission


@app.route('/login', methods=['POST'])
def login():
    # Retrieve the user by email
    user = User.get_by_email(request.form)

    # Check if the user exists
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')

    # Check if the entered password is valid
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    # Store the user's ID in the session
    session['user_id'] = user.id

    # Redirect to the dashboard
    return redirect('/dashboard')

# Route for the dashboard


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect('/logout')

    # Retrieve the user's data
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)

    # Render the dashboard template with the user's data
    return render_template("dashboard.html", user=user)

# Route for logging out


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the home page
    return redirect('/')
