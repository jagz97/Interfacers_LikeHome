#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import math
from pyairports.airports import Airports
from amadeus import Client, ResponseError, Location
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from app.forms import RegisterForm, LoginForm, ForgotForm, SearchForm
import os
from unicodedata import category
from datetime import datetime
import secrets
from flask import render_template, redirect, url_for, request, flash, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

import airportsdata
import requests
from app import app as app
from app import db, photos, search
from app.models import User, Reservations
import stripe
import requests
from sqlalchemy import update
from datetime import datetime
import json


'''
obj = json.loads(response)
js = json.dumps(obj, indent=3)
print(js)

'''

stripe.api_key = 'sk_test_51KxjFzLGavGifIHgiMdIOOdRlyHLKg0elxsL5iStElwzlbGrboQmH7RHtS1CJ8VxmZ2IrefIiCjPjZpNqNwG1Aep00kaUCU9cP'

amadeus = Client(
    client_id='GHQQMBbsZrNAHakVbwH3pDT3OT5Qzge9',
    client_secret='n2x07IbGh6LkvTBg'
)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

'''app = Flask(__name__)
app.config.from_object('config')'''
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

'''
product = amadeus.reference_data.locations.get(keyword='San Jose',subType=Location.ANY).data
for p in product:


    code = p["iataCode"]
    break
'''


@app.route("/searchs", methods=['GET', 'POST'])
def searchs():
    search_input = request.form.get('q')

    return render_template('test.html', search_input=search_input)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_input = request.form.get('q')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')

    url1 = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"

    querystring1 = {"query": search_input,
                    "currency": "USD", "locale": "en_US"}

    headers1 = {
        "X-RapidAPI-Key": "5e7e5dccfdmsh167cbe3cb5f7241p1b67ffjsnd253c9c8d696",
        "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
    }

    response1 = requests.request(
        "GET", url1, headers=headers1, params=querystring1)

    data = response1.text
    print(data)
    jdata = json.loads(data)

    preety = json.dumps(jdata, indent=3)
# print(preety)

    city = jdata['suggestions'][0]['entities'][0]['destinationId']

    print(city)

    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"

    querystring = {"checkin_date": checkin, "checkout_date": checkout, "sort_order": "STAR_RATING_HIGHEST_FIRST",
                   "destination_id": city, "adults_number": "1", "locale": "en_US", "currency": "USD"}

    headers = {
        "X-RapidAPI-Key": "5e7e5dccfdmsh167cbe3cb5f7241p1b67ffjsnd253c9c8d696",
        "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring).text
    jres = json.loads(response)

    inc = 0

    return render_template('search.html', products=jres, inc=inc, checkin = checkin, checkout = checkout)


@app.route('/upcoming', methods=['GET', 'POST'])
def viewres():
    if current_user.is_authenticated:
        user = current_user
        reservation = Reservations.query.filter(
            Reservations.username == user.name).all()
        user_to_display = User.query.filter(
            User.name == user.name).one()

    return render_template('upcoming.html', reservation=reservation, user=user_to_display)


# for s in data:
 #   print(s["address"])

@app.route('/success', methods=['GET', 'POST'])
def success():
    """
    Success message display upon successful payment
    """

    return render_template('success.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_res():

    id = request.form.get('id')

    Reservations.query.filter(Reservations.id == id).delete()

    db.session.commit()
    

    return render_template('charge.html')

@login_required
@app.route('/payments', methods=['GET', 'POST'])
def payment():
    """
    Stripe payment setup for secure checkout
    Source: https://stripe.com/docs/payments/checkout/migration

   
        price = request.form.get('amount')
        hotelname = request.form.get('add')
        id = request.form.get('id')
        hotel_id_str = str(id)
        price_str = str(price)
        hotelname_str = str(hotelname)
        user = current_user
        username = user.name

       
    """
    if request.method == "POST":
        
        id = request.form.get('id')
        hotel_id_str = str(id)
        street_address = request.form.get('street_address')
        price = request.form.get('price')
        price_str = str(price)
        city = request.form.get('city')
        city_str = str(city)
        zip = request.form.get('zip')
        state = request.form.get('state')
        country = request.form.get('country')
        country_str = str(country)
        hotel_name = request.form.get('hotel_name')
        hotel_name_str = str(hotel_name)
        check_in = request.form.get('checkin')
        check_in_str = str(check_in)
        check_out = request.form.get('checkout')
        check_out_str = str(check_out)
        user = current_user
        username = user.name

        addres = Reservations(
            hotelId=id, hotelName=hotel_name_str, price=price_str, username=username, check_in= check_in_str, check_out=check_out_str, country=country_str)

        db.session.add(addres)

        user_to_update = User.query.filter(
            User.name == user.name).one()
        print(f"user is {user_to_update}")

        if user_to_update.points:
            user_to_update.points = math.floor(
                int(float(price)) / 10) + user_to_update.points
        else:
            user_to_update.points = math.floor(
                int(float(price)) / 10)

        db.session.commit()

        return redirect(url_for('success'))


''' 

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Hotel Booking',
        amount=price,
        currency='usd',
    )
'''


@app.route("/reservation", methods=['POST', 'GET'])
def reserve():

    
    id = request.form.get('id')
    street_address = request.form.get('street_address')
    price = request.form.get('price')
    image = request.form.get('image')
    city = request.form.get('city')
    zip = request.form.get('zip')
    state = request.form.get('state')
    country = request.form.get('country')
    hotel_name = request.form.get('hotel_name')
    check_in = request.form.get('checkin')
    check_out = request.form.get('checkout')


    
    ''' 
    if id and street_address and price and image and city and zip and state and country and request.method == "POST":
        p = price
        id = id
        add = street_address
        image = image
        city = city
        zip = zip
        state = state
        country = country   

'''

        
    return render_template('reservation.html', p = price, add = street_address, id= id, image= image, city= city, zip = zip, state = state, country = country, hotel_name = hotel_name, checkin = check_in, checkout= check_out)



@app.route('/logout')
def logout():
    """
    Manges the logout response from user
    Securely logs out the customer and redirects them to login page
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/results')
@login_required
def results():
    """
    Returns the items searched from added products
    Created search functionality using m-search
    Source: https://github.com/honmaple/flask-msearch
    """
    query = request.args.get("q")
    products = Hotels.query.filter(Hotels.region.like("%"+query+"%")).all()

    return render_template('search.html', products=products)


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
@login_required
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        session["name"] = user.name
        return redirect(url_for('login'))
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if not current_user.is_authenticated:
        form = RegisterForm(request.form)
        if request.method == "POST":
            name = form.name.data
            email = form.email.data
            password = form.password.data
            passwordh = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8)
            newuser = User(name=name, email=email, password=passwordh)
            try:
                db.session.add(newuser)
                db.session.commit()
                flash("Account Created for user {}".format(form.name.data))
            except Exception:
                flash('Username or email already taken')
                return redirect(url_for('register'))
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """
    Success message display upon successful payment
    """
    user = current_user
    user_to_display = User.query.filter(
        User.name == user.name).one()
    return render_template('profile.html', user=user_to_display)


'''
@app.route('/result')
def result():
    hotels = Hotels.query.all()

    return render_template('layouts/search.html', hotels= hotels)

'''

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
