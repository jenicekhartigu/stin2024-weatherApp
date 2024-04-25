from flask import Blueprint, render_template, request, flash

from website.getAPIdata import current_location, show_weather

noAuth = Blueprint('noAuth', __name__)

@noAuth.route('/nologin', methods=['GET', 'POST'])
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
        
        return render_template("nologpage.html", user=None)

    else:
        return render_template("base.html", user = None)
