from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests
from .models import User
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
import os

auth = Blueprint('auth', __name__)

def get_api_key():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    return api_key

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={get_api_key()}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data

def get_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={get_api_key()}&q={city}&days=7"
    response = requests.get(url)
    data = response.json()
    return data

def show_weather(city):
    weather_data = get_weather(city)
    weather_forecast = get_forecast(city)
    if 'error' in weather_data or 'error' in weather_forecast:
        error = weather_data['error']['message']
    else:
        error = None
    return weather_data, weather_forecast, error, city


@auth.route('/nouser', methods = ['GET', 'POST'])
def nologpage():
    
    cityName = request.form.get('name')
    
    get_weather(cityName)
    
    
    
    return render_template("nologpage.html", city_name = cityName, user = None)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)