import os
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

    servings_selected = []

    for built_meal in built_meals:
        servings_selected = []

        for index, serving in enumerate(built_meal["servings_selected"]):
            serving_option = mongo.db.serving_options.find_one(
                {"_id": ObjectId(serving)})

            servings_selected.append("{} {} {}".format(
                serving_option["quantity"] *
                built_meal["servings_quantities"][index],
                serving_option["engineering_unit"],
                serving_option["ingredient"]))

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
