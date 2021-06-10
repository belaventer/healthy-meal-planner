import os
import json
from collections import Counter
import re
from datetime import datetime, date
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
if os.path.exists('env.py'):
    import env


serving_categories = [
    ['breakfast', 'lunch', 'dinner', 'snack'],
    ['protein', 'grain', 'vegetables', 'fruit', 'fat',
        'carbohydrate']]


app = Flask(__name__)


app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = './static/images/meals'


mongo = PyMongo(app)


def get_user():
    """
    Helper function to get user if
    logged in.
    """
    if 'user' in session:
        return mongo.db.users.find_one(
            {'username': session['user']})
    return False


def format_meal():
    """
    Helper function to get form data
    and set in correct document format
    """
    servings_selected = []
    servings_quantities = {}
    # remove duplicated selections
    for input, value in request.form.to_dict().items():
        if (input != 'meal_name' and
                input != 'meal_category' and
                input != 'meal_image'):
            if (value not in servings_quantities.keys()):
                servings_quantities[value] = 1
            else:
                servings_quantities[value] += 1

            if (ObjectId(value) not in servings_selected):
                servings_selected.append(ObjectId(value))

    f = request.files['meal_image']
    filename = secure_filename(f.filename)
    f.save(os.path.join(
        app.config['UPLOAD_FOLDER'], session['user'] + filename))

    meal = {
        'meal_name': request.form.get('meal_name'),
        'meal_image': 'images/meals/' + session['user'] + filename,
        'category': request.form.get('meal_category'),
        'created_by': session['user'],
        'servings_selected': servings_selected,
        'servings_quantities': servings_quantities
    }
    return meal


def format_serving():
    """
    Helper function to get form data
    and set in correct document format
    """
    serving = {
        'category': '{}_{}'.format(
            request.form.get('category_meal').lower(),
            request.form.get('category_type').lower()),
        'ingredient': request.form.get('ingredient').lower(),
        'quantity': float(request.form.get('quantity')),
        'engineering_unit': request.form.get('engineering_unit')}

    return serving


def meal_to_servings(built_meals):
    """
    Helper function to set servings of meals in
    string format.
    """
    servings_selected = {}

    # turn servings IDs to strings
    for built_meal in built_meals:
        list_options = []
        for serving in built_meal['servings_selected']:
            serving_option = mongo.db.serving_options.find_one(
                {'_id': ObjectId(serving)})

            if serving_option:
                list_options.append('{} {} {}'.format(
                    serving_option['quantity'] *
                    built_meal['servings_quantities'][str(serving)],
                    serving_option['engineering_unit'],
                    serving_option['ingredient']))
            else:
                list_options.append(
                    'Serving not found. Please contact administrator')

        servings_selected.update({built_meal['meal_name']: list_options})

    return servings_selected


@app.route('/')
@app.route('/home')
def home():
    """
    Routing function to main page.
    If logged in, redirect to profile.
    """
    if get_user():
        return redirect(url_for('profile', username=session['user']))

    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Funtion to check entered credentials
    and create session to user.
    """
    if request.method == 'POST':
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('username').lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user['password'], request.form.get('password')):
                session['user'] = request.form.get('username').lower()
                return redirect(url_for('profile', username=session['user']))
            else:
                # invalid password match
                flash('Incorrect Username and/or Password', 'login')
                return redirect(url_for('login'))

        else:
            # username doesn't exist
            flash('Incorrect Username and/or Password', 'login')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Funtion to register new user
    to the database.
    """
    if request.method == 'POST':
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {'username': request.form.get('new_username').lower()})

        if existing_user:
            flash('Username already exists', 'register')
            return redirect(url_for('register'))

        register = {
            'username': request.form.get('new_username').lower(),
            'password': generate_password_hash(
                request.form.get('new_password')),
            'admin': False
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session['user'] = request.form.get('new_username').lower()
        flash('Registration Successful!', 'register')
        return redirect(url_for('profile', username=session['user']))

    return render_template('login.html')


@app.route('/profile/<username>')
def profile(username):
    """
    Funtion to get built meals
    if user is logged in.
    """
    user = get_user()

    if user:
        built_meals = mongo.db.built_meals.find(
            {'created_by': session['user']})

        servings_selected = meal_to_servings(built_meals)

        day = datetime.strftime(date.today(), '%d %b %Y')

        day_plan = mongo.db.built_plans.find_one(
                {'day': datetime.strptime(day, '%d %b %Y'),
                 'created_by': session['user']})

        if day_plan:
            day_plan['day'] = datetime.strftime(day_plan['day'], '%d %b %Y')

            day_meals = {}
            for meal in day_plan['selected_meals']:
                meal_name = mongo.db.built_meals.find_one(
                    {'_id': meal})['meal_name']
                meal_category = mongo.db.built_meals.find_one(
                    {'_id': meal})['category']
                day_meals[meal_category] = meal_name

            day_plan['selected_meals'] = day_meals
        else:
            day_plan = {
                'day': day,
                'selected_meals': {
                    'Nothing planned for the day': ""}}

        built_meals.rewind()

        return render_template(
            'profile.html', user=user, built_meals=built_meals,
            servings_selected=servings_selected, day_plan=day_plan)

    return redirect(url_for('login'))


@app.route('/servings/<username>')
def servings(username):
    """
    Funtion to get servings
    if admin user is logged in.
    """
    user = get_user()

    if user:
        # redirect if user is not admin
        if not user['admin']:
            return redirect(url_for('home'))

        else:
            serving_options = mongo.db.serving_options.find()

            return render_template(
                'servings.html', user=user, serving_options=serving_options)

    return redirect(url_for('login'))


@app.route('/add_serving', methods=['GET', 'POST'])
def add_serving():
    """
    Function to add new serving option
    to the database
    """
    user = get_user()

    if user:
        # redirect if user is not admin
        if not user['admin']:
            return redirect(url_for('home'))

        else:
            if request.method == 'POST':
                serving = format_serving()

                mongo.db.serving_options.insert_one(serving)
                flash('Serving Successfully Added', 'general')

                return redirect(url_for('servings', username=session['user']))

            return render_template(
                'add_serving.html', user=user, categories=serving_categories)

    return redirect(url_for('login'))


@app.route('/edit_serving/<serving_id>', methods=['GET', 'POST'])
def edit_serving(serving_id):
    """
    Function to edit a serving option
    on the database
    """
    user = get_user()

    if user:
        # redirect if user is not admin
        if not user['admin']:
            return redirect(url_for('home'))

        else:
            if request.method == 'POST':
                update_serving = format_serving()

                mongo.db.serving_options.update(
                    {'_id': ObjectId(serving_id)}, update_serving)
                flash('Serving Successfully Updated', 'general')

                return redirect(url_for('servings', username=session['user']))

            serving = mongo.db.serving_options.find_one(
                {'_id': ObjectId(serving_id)})

            category_selected = serving['category'].split('_')

            return render_template(
                'edit_serving.html', user=user,
                categories=serving_categories,
                category_selected=category_selected,
                serving=serving)

    return redirect(url_for('login'))


@app.route('/delete_item/<collection>/<item_id>')
def delete_item(collection, item_id):
    """
    Function to delete item from the database,
    depending on the collection.
    """
    user = get_user()

    if user:
        # redirect if user is not admin
        if collection == 'serving_options' and not user['admin']:
            return redirect(url_for('home'))

        # delete serving if user is admin
        elif collection == 'serving_options' and user['admin']:
            mongo.db.serving_options.remove({'_id': ObjectId(item_id)})

            flash('Serving Successfully Deleted', 'general')

            return 'Success'

        # delete meal
        else:
            mongo.db.built_meals.remove({'_id': ObjectId(item_id)})

            flash('Meal Successfully Deleted', 'general')

            return 'Success'

    return redirect(url_for('login'))


@app.route('/add_meal', methods=['GET', 'POST'])
def add_meal():
    """
    Function to add new meal option
    to the database
    """
    user = get_user()

    if user:
        categories = ['breakfast', 'lunch', 'dinner', 'snack']

        if request.method == 'POST':
            meal = format_meal()

            mongo.db.built_meals.insert_one(meal)
            flash('Meal Successfully Added', 'general')

            return redirect(url_for('profile', username=session['user']))

        return render_template(
            'add_meal.html', user=user, categories=categories)

    return redirect(url_for('login'))


@app.route('/get_serving_options/<meal_category>')
def get_serving_options(meal_category):
    """
    Function to get serving options
    and pass to front end
    """
    serving_options = mongo.db.serving_options.find(
        {'category': {'$regex': meal_category}})
    servings = []
    intakes = mongo.db.daily_intake.find_one()[meal_category]

    # turn ObjectId to string for JSON
    for serving in serving_options:
        serving['_id'] = str(serving['_id'])

        servings.append(serving)

    return json.dumps([servings, intakes])


@app.route('/edit_meal/<meal_id>', methods=['GET', 'POST'])
def edit_meal(meal_id):
    """
    Function to edit a meal option
    on the database
    """
    user = get_user()

    if user:
        meal = mongo.db.built_meals.find_one(
            {'_id': ObjectId(meal_id)})

        for serving, quantity in meal['servings_quantities'].items():
            if quantity > 1:
                meal['servings_selected'].insert(
                    meal['servings_selected'].index(ObjectId(serving))+1,
                    ObjectId(serving))

        # Use of wildcard https://stackoverflow.com/questions/55617412/
        # how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo
        serving_options = mongo.db.serving_options.find(
            {'category': {'$regex': meal['category']}})

        servings = []
        intakes = mongo.db.daily_intake.find_one()[meal['category']]

        for serving in serving_options:
            serving['_id'] = str(serving['_id'])

            servings.append(serving)

        if request.method == 'POST':
            updated_meal = format_meal()

            mongo.db.built_meals.update(
                {'_id': ObjectId(meal_id)}, updated_meal)
            flash('Meal Successfully Updated', 'general')

            return redirect(url_for('profile', username=session['user']))

        return render_template(
            'edit_meal.html', user=user, categories=serving_categories[0],
            meal=meal, intakes=intakes, servings=servings)

    return redirect(url_for('login'))


@app.route('/plan_week')
def plan_week():
    """
    Function to render boilerplate
    of week page.
    """
    user = get_user()

    if user:
        built_meals = list(mongo.db.built_meals.find(
            {'created_by': session['user']}))

        week_plans = mongo.db.built_plans.find(
            {'created_by': session['user']})

        return render_template(
            'plan_week.html', user=user, built_meals=built_meals,
            week_plans=week_plans)

    return redirect(url_for('login'))


@app.route('/submit_plan/<week>/<day>', methods=['GET', 'POST'])
def submit_plan(week, day):
    """
    Function to add or edit day plan
    on the database.
    """
    user = get_user()

    if user:
        if request.method == 'POST':
            existing_plan = mongo.db.built_plans.find_one(
                {'day': datetime.strptime(day, '%d %b %Y'),
                    'week': week,
                    'created_by': session['user']})

            selected_meals = []
            built_meals = []
            for input, value in request.form.to_dict().items():
                selected_meals.append(ObjectId(value.split('_')[0]))
                built_meals.append(mongo.db.built_meals.find_one(
                    {'_id': ObjectId(value.split('_')[0])}))

                groceries = meal_to_servings(built_meals)

            plan = {'day': datetime.strptime(day, '%d %b %Y'),
                    'week': week,
                    'created_by': session['user'],
                    'selected_meals': selected_meals,
                    'groceries': groceries}

            # check if day plan exists to either insert or update
            if not existing_plan:
                mongo.db.built_plans.insert_one(plan)

                return redirect(url_for('plan_week'))

            mongo.db.built_plans.update(
                existing_plan, plan)

        return redirect(url_for('plan_week'))

    return render_template('login.html')


@app.route('/get_week_plan/<day>')
def get_week_plan(day):
    """
    Function to get day plan
    and pass to front end
    """
    day_plan = mongo.db.built_plans.find_one(
                {'day': datetime.strptime(day, '%d %b %Y'),
                    'created_by': session['user']})

    # Set dates and ObjectId for JSON dump
    if day_plan:
        day_plan['day'] = datetime.strftime(day_plan['day'], '%d %b %Y')
        day_plan['_id'] = str(day_plan['_id'])

        day_meals = {}
        for meal in day_plan['selected_meals']:
            meal_name = mongo.db.built_meals.find_one(
                {'_id': meal})['meal_name']
            meal_category = mongo.db.built_meals.find_one(
                {'_id': meal})['category']
            day_meals[meal_category] = meal_name

        day_plan['selected_meals'] = day_meals
        return json.dumps(day_plan)
    return False


@app.route('/get_groceries/<week>')
def get_groceries(week):
    """
    Function to get all week plans
    and compile groceries list
    """
    week_plan = mongo.db.built_plans.find(
        {'week': week,
            'created_by': session['user']})

    groceries = [
        serving for plan in week_plan
        for meal in plan['groceries'].values()
        for serving in meal]

    count = Counter(groceries)

    groceries_list = []
    # extract floats solution found in
    # https://stackoverflow.com/questions/4703390/
    # how-to-extract-a-floating-number-from-a-string
    for item, value in count.items():
        groceries_list.append('{} {}'.format(
            float(re.findall("\d+\.\d+", item)[0])*value,
            ' '.join(item.split()[1:])))

    return render_template(
        'groceries.html', week=week, groceries=groceries_list)


@app.route('/logout')
def logout():
    """
    Function to remove logged session.
    """
    # remove user from session cookie
    flash('You have been logged out', 'general')
    session.pop('user')
    return redirect(url_for('home'))


# Call the Flask application. Note: set debug=False before submission
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
