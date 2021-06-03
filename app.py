import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    if "user" in session:
        return redirect(url_for("profile", username=session["user"]))

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "login")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "login")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("new_username").lower()})

        if existing_user:
            flash("Username already exists", "register")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("new_username").lower(),
            "password": generate_password_hash(
                request.form.get("new_password")),
            "admin": False
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("new_username").lower()
        flash("Registration Successful!", "register")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    built_meals = mongo.db.built_meals.find(
        {"created_by": session["user"]})

    servings_selected = {}

    for built_meal in built_meals:
        list_options = []

        for serving in built_meal["servings_selected"]:
            serving_option = mongo.db.serving_options.find_one(
                {"_id": ObjectId(serving)})

            list_options.append("{} {} {}".format(
                serving_option["quantity"] *
                built_meal["servings_quantities"][str(serving)],
                serving_option["engineering_unit"],
                serving_option["ingredient"]))

        servings_selected.update({built_meal["meal_name"]: list_options})

    built_meals.rewind()

    if session["user"]:
        return render_template(
            "profile.html", user=user, built_meals=built_meals,
            servings_selected=servings_selected)

    return redirect(url_for("login"))


@app.route("/servings/<username>")
def servings(username):
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    if not user["admin"]:
        return redirect(url_for("home"))

    else:
        serving_options = mongo.db.serving_options.find()

        if session["user"]:
            return render_template(
                "servings.html", user=user, serving_options=serving_options)

    return redirect(url_for("login"))


@app.route("/add_serving", methods=["GET", "POST"])
def add_serving():
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})

        if not user["admin"]:
            return redirect(url_for("home"))

        else:
            if request.method == "POST":
                serving = {
                    "category": "{}_{}".format(
                        request.form.get("category_meal").lower(),
                        request.form.get("category_type").lower()),
                    "ingredient": request.form.get("ingredient").lower(),
                    "quantity": float(request.form.get("quantity")),
                    "engineering_unit": request.form.get("engineering_unit")
                }

                mongo.db.serving_options.insert_one(serving)
                flash("Serving Successfully Added", "general")

                return redirect(url_for("servings", username=session["user"]))

            categories = [
                ["breakfast", "lunch", "dinner", "snack"],
                ["protein", "grain", "vegetables", "fruit", "fat",
                    "carbohydrate"]]

            return render_template(
                "add_serving.html", user=user, categories=categories)

    return redirect(url_for("home"))


@app.route("/edit_serving/<serving_id>", methods=["GET", "POST"])
def edit_serving(serving_id):
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})

        if not user["admin"]:
            return redirect(url_for("home"))

        else:
            if request.method == "POST":
                update_serving = {
                    "category": "{}_{}".format(
                        request.form.get("category_meal").lower(),
                        request.form.get("category_type").lower()),
                    "ingredient": request.form.get("ingredient").lower(),
                    "quantity": float(request.form.get("quantity")),
                    "engineering_unit": request.form.get("engineering_unit")
                }

                mongo.db.serving_options.update(
                    {"_id": ObjectId(serving_id)}, update_serving)
                flash("Serving Successfully Updated", "general")

                return redirect(url_for("servings", username=session["user"]))

            serving = mongo.db.serving_options.find_one(
                {"_id": ObjectId(serving_id)})
            categories = [
                ["breakfast", "lunch", "dinner", "snack"],
                ["protein", "grain", "vegetables", "fruit", "fat",
                    "carbohydrate"]]
            category_selected = serving["category"].split("_")

            return render_template(
                "edit_serving.html", user=user,
                categories=categories, category_selected=category_selected,
                serving=serving)

    return redirect(url_for("home"))


@app.route("/delete_serving/<serving_id>")
def delete_serving(serving_id):
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})

        if not user["admin"]:
            return redirect(url_for("home"))

        else:
            mongo.db.serving_options.remove({"_id": ObjectId(serving_id)})
            flash("Serving Successfully Deleted", "general")

            serving_options = mongo.db.serving_options.find()

            return render_template(
                "servings.html", user=user, serving_options=serving_options)

    return redirect(url_for("home"))


@app.route("/add_meal", methods=["GET", "POST"])
def add_meal():
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})

        categories = ["breakfast", "lunch", "dinner", "snack"]

        if request.method == "POST":
            servings_selected = []
            servings_quantities = {}
            for input, value in request.form.to_dict().items():
                if (input != "meal_name"
                        and input != "meal_category"):
                    if (value not in servings_quantities.keys()):
                        servings_quantities[value] = 1
                    else:
                        servings_quantities[value] += 1

                    if (ObjectId(value) not in servings_selected):
                        servings_selected.append(ObjectId(value))

            meal = {
                "meal_name": request.form.get("meal_name"),
                "category": request.form.get("category"),
                "created_by": session["user"],
                "servings_selected": servings_selected,
                "servings_quantities": servings_quantities
            }

            mongo.db.built_meals.insert_one(meal)
            flash("Meal Successfully Added", "general")

            return redirect(url_for("profile", username=session["user"]))

        return render_template(
            "add_meal.html", user=user, categories=categories)

    return redirect(url_for("home"))


@app.route("/get_serving_options/<meal_category>")
def get_serving_options(meal_category):
    serving_options = mongo.db.serving_options.find(
        {"category": {'$regex': meal_category}})
    servings = []
    intakes = []
    daily_intake = mongo.db.daily_intake.find_one()

    intakes = daily_intake[meal_category]

    for serving in serving_options:
        serving["_id"] = str(serving["_id"])

        servings.append(serving)

    return json.dumps([servings, intakes])


@app.route("/edit_meal/<meal_id>", methods=["GET", "POST"])
def edit_meal(meal_id):
    if "user" in session:
        user = mongo.db.users.find_one(
            {"username": session["user"]})

        meal = mongo.db.built_meals.find_one(
            {"_id": ObjectId(meal_id)})

        for serving, quantity in meal["servings_quantities"].items():
            if quantity > 1:
                meal["servings_selected"].insert(
                    meal["servings_selected"].index(ObjectId(serving))+1,
                    ObjectId(serving))

        categories = ["breakfast", "lunch", "dinner", "snack"]

        # Use of wildcard https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo
        serving_options = mongo.db.serving_options.find(
            {"category": {'$regex': meal["category"]}})

        servings = []
        daily_intake = mongo.db.daily_intake.find_one()

        intakes = daily_intake[meal["category"]]

        for serving in serving_options:
            serving["_id"] = str(serving["_id"])

            servings.append(serving)

        return render_template(
            "edit_meal.html", user=user, categories=categories,
            meal=meal, intakes=intakes, servings=servings)

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out", "general")
    session.pop("user")
    return redirect(url_for("home"))


# Call the Flask application. Note: set debug=False before submission
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
