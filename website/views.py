from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.getAPIdata import *
from . import db
import json

from .models import Places

views = Blueprint('views', __name__)

lastPlace = [None]


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
                print(lastPlace)
                _, forecast, _, _, _ = show_weather(lastPlace[0])
                
                date = forecast['forecast']['forecastday'][0]['date']
                text = forecast['forecast']['forecastday'][0]['day']['condition']['text']
                avgTemp = forecast['forecast']['forecastday'][0]['day']['avgtemp_c']
                
                resultStr = date + " in " + lastPlace[0] + " will be average temp: " + str(avgTemp) + "°C" + " and " + text
                
                print(forecast)

                
                new_note = Places(data=resultStr, user_id=current_user.id)  #providing the schema for the note 
                db.session.add(new_note) #adding the note to the database 
                db.session.commit()
                flash('Place added!', category='success')
                lastPlace[0] = None
                resultStr = None
                
                
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
    if request.method == 'POST': 
        mesto = request.form.get('getMesto')#Gets the note from the HTML
        if mesto == '': 
            flash('No city', category='error')
            return render_template("nologpage.html", user=None)
        else:
            
            weather_data, _ , _, _, city = show_weather(mesto)
            
            text = weather_data['current']['condition']['text']
            iconUrl = weather_data['current']['condition']['icon']
            actualTemp = weather_data['current']['temp_c']

            return render_template("nologpage.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=None)

    elif request.method == 'GET':
        location = current_location()
        
        mesto = location[1]['location']['name']
        
        weather_data, _ , _, _, city = show_weather(mesto)
        
        text = weather_data['current']['condition']['text']
        iconUrl = weather_data['current']['condition']['icon']
        actualTemp = weather_data['current']['temp_c']
        
        return render_template("nologpage.html", city_name = city, actual_temp = actualTemp, weather = text, weather_image = iconUrl, user=None)

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