from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, AnonymousUserMixin
from website.getAPIdata import *

from .models import Places
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    
    #prihlaseny uzivatel
    if not isinstance(current_user, AnonymousUserMixin) :
        if request.method == 'POST': 
            mesto = request.form.get('getMesto')#Gets the note from the HTML
            add = request.form.get('note')
            
            if isinstance(mesto,str) and add is None:
                print(mesto)
                
                weather_data, weather_forecast, weather_history, error, city = show_weather(mesto)
            
                print(weather_data)
                print(weather_forecast)
                print(weather_history)
                print(error)
                
                return render_template("home.html", city_name = city, user=current_user)
                
            if mesto is None and add is None:
                
                print("add place")
            # if len(note) < 1:
            #     flash('Note is too short!', category='error') 
            # else:
            #     new_note = Places(data=note, user_id=current_user.id)  #providing the schema for the note 
            #     db.session.add(new_note) #adding the note to the database 
            #     db.session.commit()
            #     flash('Note added!', category='success')

                return render_template("home.html", user=current_user)
    
    
    #Neprihlaseny uzivatel
    else:
        if request.method == 'POST': 
            mesto = request.form.get('getMesto')#Gets the note from the HTML 
            
            weather_data, _ , _, error, city = show_weather(mesto)
            
            print(weather_data)
            print(error)

            return render_template("home.html", city_name = city, user=None)
        
        else:
            
            return render_template("home.html", user=None)



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