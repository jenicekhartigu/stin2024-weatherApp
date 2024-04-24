from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, AnonymousUserMixin
from website.getAPIdata import *

from .models import Places
from . import db
import json

views = Blueprint('views', __name__)

lastPlace = [None]


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        mesto = request.form.get('getMesto') #Gets the note from the HTML
        add = request.form.get('note')
        
        if isinstance(mesto,str) and add is None:
            print(mesto)
            
            weather_data, weather_forecast, weather_history, _, city = show_weather(mesto)
        
            text = weather_data['current']['condition']['text']
            iconUrl = weather_data['current']['condition']['icon']
            actualTemp = weather_data['current']['temp_c']
            
            print(weather_forecast)
            print()
            print(weather_history)
            
            
            
            lastPlace[0] = city

            return render_template("home.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, history = weather_history ,user=current_user)
    
        if mesto is None and add is None:
            
            if lastPlace[0] is None:
                flash('No place selected!', category='error') 
            else:
                new_note = Places(data=lastPlace[0], user_id=current_user.id)  #providing the schema for the note 
                db.session.add(new_note) #adding the note to the database 
                db.session.commit()
                flash('Place added!', category='success')
                lastPlace[0] = None
            return render_template("home.html", user=current_user)
    

    return render_template("home.html", user=current_user)

@views.route('/nologpage', methods=['GET', 'POST'])
def nologpage():
    if request.method == 'POST': 
        mesto = request.form.get('getMesto')#Gets the note from the HTML 
        
        weather_data, _ , _, _, city = show_weather(mesto)
        
        text = weather_data['current']['condition']['text']
        iconUrl = weather_data['current']['condition']['icon']
        actualTemp = weather_data['current']['temp_c']

        return render_template("nologpage.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=None)
    
    else:
        location = current_location()
        
        mesto = location[1]['location']['name']
        
        weather_data, _ , _, _, city = show_weather(mesto)
        
        text = weather_data['current']['condition']['text']
        iconUrl = weather_data['current']['condition']['icon']
        actualTemp = weather_data['current']['temp_c']
        
        return render_template("nologpage.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=None)

    
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