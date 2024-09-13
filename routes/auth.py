from flask import render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User
from models import db
from datetime import datetime, timedelta
from utils.decorators import jwt_token_required
from . import auth_routes

@auth_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # If user already exists, re-render the signup page with an error message
        if user:
            return render_template('signup.html', error="User already exists"), 401
        
        # Hash the password and create a new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful signup
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.username)
            return jsonify({"access_token": access_token, "message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    return render_template('login.html')

@auth_routes.route('/logout')
@jwt_token_required
def logout():
    # Set the cookie expiration to a past date to invalidate it
    response = redirect(url_for('auth.login'))
    response.set_cookie('auth', '', expires=datetime(1970, 1, 1))  # Expire the auth cookie
    
    return response