from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.getAPIdata import *
from . import db
import json

from .models import Places

views = Blueprint('views', __name__)

lastPlace = [None]

def render_nolog_page(city=None, actual_temp=None, weather=None, weather_image=None):
    """Render the nologpage template."""
    return render_template("nologpage.html", city_name=city, actual_temp=actual_temp, weather=weather, weather_image=weather_image, user=None)


def handle_post_request():
    """Handle POST request."""
    mesto = request.form.get('getMesto')
    if not mesto:
        flash('No city', category='error')
        return render_nolog_page()

    weather_data, _, _, _, city = show_weather(mesto)
    current_weather = weather_data['current']
    text = current_weather['condition']['text']
    icon_url = current_weather['condition']['icon']
    actual_temp = current_weather['temp_c']
    
    return render_nolog_page(city, actual_temp, text, icon_url)

def handle_get_request():
    """Handle GET request."""
    location = current_location()
    mesto = location[1]['location']['name']
    weather_data, _, _, _, city = show_weather(mesto)
    current_weather = weather_data['current']
    text = current_weather['condition']['text']
    icon_url = current_weather['condition']['icon']
    actual_temp = current_weather['temp_c']
    
    return render_nolog_page(city, actual_temp, text, icon_url)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        mesto = request.form.get('getMesto') #Gets the note from the HTML
        add = request.form.get('note')
        
        if isinstance(mesto,str) and add is None:
            if mesto == '':
                flash('No place selected!', category='error') 
            else:
                weather_data, _, weather_history, _, city = show_weather(mesto)
            
                text = weather_data['current']['condition']['text']
                iconUrl = weather_data['current']['condition']['icon']
                actualTemp = weather_data['current']['temp_c']

                lastPlace[0] = city

                return render_template("home.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, history = weather_history ,user=current_user)
    
        if mesto is None and add is None:
            
            if lastPlace[0] is None:
                flash('No place selected!', category='error') 
            else:
                _, forecast, _, _, _ = show_weather(mesto)
                
                date = forecast['forecast']['forecastday'][0]['date']
                text = forecast['forecast']['forecastday'][0]['day']['condition']['text']
                avgTemp = forecast['forecast']['forecastday'][0]['day']['avgtemp_c']
                
                resultStr = date + " in " + lastPlace[0] + " will be average temp: " + str(avgTemp) + "°C" + " and " +text

                new_note = Places(data=resultStr, user_id=current_user.id)  #providing the schema for the note 
                db.session.add(new_note) #adding the note to the database 
                db.session.commit()
                flash('Place added!', category='success')
                lastPlace[0] = None
                
            return render_template("home.html", user=current_user)
    else:
        location = current_location()
        
        mesto = location[1]['location']['name']
        
        weather_data, _ , _, _, city = show_weather(mesto)
        
        text = weather_data['current']['condition']['text']
        iconUrl = weather_data['current']['condition']['icon']
        actualTemp = weather_data['current']['temp_c']
        
        return render_template("home.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=current_user)

@views.route('/app', methods=['GET', 'POST'])
def noUserApp():
    print("here")

    location = current_location()
        
    mesto = location[1]['location']['name']

    weather_data, _ , _, _, city = show_weather(mesto)

    text = weather_data['current']['condition']['text']
    iconUrl = weather_data['current']['condition']['icon']
    actualTemp = weather_data['current']['temp_c']

    return render_template("nologpage.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=None)

@views.route('/nologin', methods=['GET', 'POST'])

def appNoUser():
    user = None
    if request.method == 'POST':
        return handle_post_request(user)
    elif request.method == 'GET':
        return handle_get_request(user)
    else:
        return render_template("base.html", user = None)
    
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Places.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})