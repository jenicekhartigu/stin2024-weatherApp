from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from website.getAPIdata import current_location, show_weather
from .models import Places
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 
        
        

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Places(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

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