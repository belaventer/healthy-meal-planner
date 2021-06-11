# Healthy Meal Planner!

![Healthy Meal Planner Website](/screenshots/website-mockup.png "Healthy Meal Planner Website")

[Demo of Website](https://healthy-meal-planner.herokuapp.com/).

Healthy Meal Planner is a application to aid diet planning. It is based on the guidelines for a 1800 calorie intake per day of [Live Health Online](https://livehealthonline.com/wp-content/uploads/2018/05/lho-wmp-1800-calorie-meal-plan.pdf). 

The **primary goal** of this application is to help the user plan a balanced diet.

Other user goals:

- Be able to save meal options.
- Be able to plan meals for the entire week.
- Receive groceries list based on selected meals.

## UX

### User stories

1. As a new visitor to the website, I want to understand the main concept of the plan.

2. As a new visitor to the website, I want to find instructions on how to use the application.

3. As a new visitor to the website, I want to register with the application.

4. As a user, I want to create meal options following the recommendation.

5. As a user, I want to create a meal plan for the week.

6. As a user, I want to be able to create, update or delete the meal options and plan.

7. As the application administrator, I want to be able to update the servings portions.

   

### Strategy 

As the main user goal is to easily build a diet plan following the health guidelines, the product is a simple web application that allow the user to choose based on its own personal taste between the serving options available. The application also generates a groceries list based on the planned meals for the week. 


### Scope

The main features in scope is the meal planner with CRUD (Create, Read, Update, Delete) interactions, the user authentication and the groceries list generation.

The features available for the application administrator also includes serving portions and daily intake CRUD.

A how to use static front-end section will also be provided to improve user experience.

Future scope:

- User weight tracker

- Admin able to manage daily intake recommendation options

- Automated Newsletter for Tips and Recipes

  

### Structure

The website will have a responsive grid system with the use of selection for the forms and cards for the documents (saved meals, plan), simple and light in design.

The help section will be a single continuous page that opens on a new tab with a Scrollspy to aid navigation.

#### Database Structure

| Collection Name              | Document's Keys                                              | Example                                                      | Function                                                     |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| users                        | username: String<br />password: String (hashed)<br />admin: Boolean | {"username":"admin",<br />"password":"****",<br />"admin":true} | Documents store the user credentials.<br />It is used for login sessions. |
| daily_intake* (admin only)   | total_calories: Int32<br />breakfast {<br />    protein: Int32,<br />    grain: Int32,<br />    fruit: Int32,<br />    fat: Int32}<br />lunch{<br />    protein: Int32,<br />    grain: Int32,<br />    vegetables: Int32,<br />    fruit: Int32,<br />    fat: Int32}<br />dinner{<br />    protein: Int32,<br />    grain: Int32,<br />    vegetables: Int32,<br />    fat: Int32}<br />snack{<br />    protein: Int32,<br />    carbohydrate: Int32} | {"total_calories":{"$numberInt":"1800"},<br /><br />"breakfast":{<br />"protein":{"$numberInt":"2"},<br />"grain":{"$numberInt":"2"},<br />"fruit":{"$numberInt":"1"},<br />"fat":{"$numberInt":"1"}},<br /><br />"lunch":{<br />"protein":{"$numberInt":"3"},<br />"grain":{"$numberInt":"3"},<br />"vegetables":{"$numberInt":"2"},<br />"fruit":{"$numberInt":"1"},<br />"fat":{"$numberInt":"2"}},<br /><br />"dinner":{<br />"protein":{"$numberInt":"4"},<br />"grain":{"$numberInt":"2"},<br />"vegetables":{"$numberInt":"2"},<br />"fat":{"$numberInt":"2"}},<br /><br />"snack":{<br />"protein":{"$numberInt":"1"},<br />"carbohydrate":{"$numberInt":"1"}}} | Documents store the amount of servings for each meal type.<br />It is used for building/editing meals. |
| serving_options (admin only) | category: String<br />ingredient: String<br />quantity: Double<br />engineering_unit: String | {"category":"breakfast_protein",<br />"ingredient":"whole egg",<br />"quantity":{"$numberDouble":"1.0"},<br />"engineering_unit":""} | Documents store the servings available.<br />It is used for building/editing meals.<br />Engineering unit is optional. |
| built_meals                  | meal_name: String<br />meal_image: String<br />category: String<br />created_by: String<br />servings_selected: Array of ObjectIDs<br />servings_quantities{<br />    serving_selected_id: Int32} | {meal_name":"Eggs and Grapes",<br />"meal_image":"images/meals/admineggs-and-grapes.png",<br />"category":"breakfast",<br />"created_by":"admin",<br />"servings_selected":[{"$oid":"60b4b31e8a8eade5e6c5b5af"},{"$oid":"60b4b3e98a8eade5e6c5b5bb"},{"$oid":"60b4b4718a8eade5e6c5b5c3"},{"$oid":"60be0e4a2735e150452d75f3"}],<br />"servings_quantities":{"60b4b31e8a8eade5e6c5b5af":{"$numberInt":"2"},"60b4b3e98a8eade5e6c5b5bb":{"$numberInt":"2"},"60b4b4718a8eade5e6c5b5c3":{"$numberInt":"1"},"60be0e4a2735e150452d75f3":{"$numberInt":"1"}}} | Documents store the user meal information.<br />It is used for creating a meal plan. |
| build_plans                  | day: Date<br />week: String<br />create_by: String<br />selected_meals: Array of ObjectIDs<br />groceries: {<br />meal_selected_id: String} | {"day":{"$date":{"$numberLong":"1622937600000"}},<br />"week":"06 Jun 2021 to 12 Jun 2021",<br />"created_by":"admin",<br />"selected_meals":[{"$oid":"60b64add263886db5a736707"},{"$oid":"60be391809136cead192080a"},{"$oid":"60be320a09136cead1920807"}],<br />"groceries":{"Eggs and Grapes":["2.0  whole egg","2.0 slice whole-grain bread","1.0 cup grapes","1.0 tbsp light butter spread"],"Mince Tortilla":["2.0 ounce  lean beef","0.5 cup beans","1.0  whole-wheat tortilla","1.0 cup brown rice","1.0 cup peppers","1.0  small banana","2.0 tsp olive oil"],"Bolognese":["4.0 ounce lean pork","1.0 cup whole-wheat pasta","1.0 cup carrots","2.0 tsp  olive oil"]}} | Documents store the user daily plan information.<br />It is used for generating groceries lists. |

*This collection is part of the future scope.

All documents will have a unique document ID automatically generated by MongoDB.

### Skeleton

- [Layout](wireframes/healthy-meal-planner-skeleton.jpg)

  #### Deviation from layout

  Instead of using a carousel for selecting the Serving Options, a dropdown for each category is available instead.

  On the profile page, the meals planned for the day are displayed to the user.

  The meals creation allow for user uploaded images and it is displayed on the home page.

  Instead of a PDF, the Groceries list is open on a simple webpage with no design.

### Surface

#### Colour

The website will use grey background colours and the following accents for each serving category.

- Protein / Carbohydrate: red

- Grain: yellow

- Fat: orange

- Fruit: blue

- Vegetables: green

  Note: to better increase accessibility, the background was updated from a light blue grey to plain white. 

#### Typography

The default typography of Materialize will be used throughout.



## Features

**Home Page**: simple welcoming text explaining the purpose of the website.

**Login / Register Page**: form allowing to the user to Register or Log In to application.

**Profile Page**: main page when the user is logged in. It will display all the saved meals from the database of the user in session and the meals planned for the current day.

**Servings Page**: page exclusive for administrator users to display the serving options available on the database.

**Built Meal Page**: page used to add a new personalized meal on the database following the guidelines recommendation.

**Plan Week Page:** page used to  add or update weekly meal plans.

**Help Page:** page with information on how to use the functionality of the website. Admin exclusive functionality is not included.

**Custom Error Pages:** 404 and 500 errors will have a custom page with the link to the Home page so the user can return without the need to use browser buttons.

### Existing Features

- **Navigation Bar:** The navigation bar is present at the top and collapses to a side bar for mobile view. The options present on the navigation bar, are conditional to the amount of credentials of the session.
- **Manage Servings:** From the Servings page, the administrator can add, update or delete serving options available on the database.
- **Manage Meals:** From the Profile page, the user can add, update or deleted personalized meals on the database.
- **Manage Plans**: From the Plan Week Page, the user can navigate to the desired week and add or update the menu for each day.
- **Generate Groceries List:** From the Plan Week Page, the user can get a list of required ingredients for the meals selected for that week.

### Features left to implement

- User weight tracker input
- Admin able to manage daily intake recommendation options front the front-end
- Automated Newsletter for Tips and Recipes
- Defensive program to avoid accidental deletions on the database of referenced documents
- A method to allow user to recover forgotten password or to change passwords

## Technologies used

### Languages

- HTML | HTML5
- CSS | CSS3
- JavaScript | JS ES6
- Python | Python3

### Libraries, Frameworks & Programs

- [Gitpod](https://gitpod.io/workspaces/):
  The developer used Gitpod as the IDE for building the website.

- [MongoDB](https://www.mongodb.com/):

  Used for database management.

- [Heroku](https://www.heroku.com/):

  Used for application deployment.

- [Flask](https://flask.palletsprojects.com/en/2.0.x/):

  Used throughout for routing / templating .

- [Fonts Awesome v5.15](https://fontawesome.com/):
  Used for several icons throughout the project.

- [Materialize](https://materializecss.com/):

  Used for templates styling.

- [Typora](https://typora.io/#):
  Used for Markdown editing of README and TESTING files.

- [Clip Studio Paint](https://www.clipstudio.net/en/):
  Used for logo editing.

- [Canva](https://www.canva.com/):
  Used for logo development.

- [AutoPrefixer](https://autoprefixer.github.io):
  Used on CSS to ensure functionality across browsers.

- [jQuery API](https://api.jquery.com/):
  Used for Materialize components initialization and custom JavaScript code.

- [Gif Compressor](https://gifcompressor.com/):

  Used to reduce Gif file sizes of help page.

  

## Testing

Refer to [TESTING.md](TESTING.md) file for testing details.



## Deployment

This project was developed using the Gitpod IDE, committed to git and pushed to GitHub.

### Deploy to Heroku from GitHub Repository:

- Log in to [Heroku](https://id.heroku.com/login).
- Create a new application with unique name and setting the region.
- Under Deploy tab, select GitHub as the Deployment Method.
- Search for the GitHub repository and click Connect.
- Under Settings tab, click "Reveal Config Vars"
- Include the env.py private variables and values:
  - IP: 0.0.0.0
  - PORT: 5000
  - SECRET_KEY: custom secret key used for sessions security
  - MONGO_URI: URI from the MongoDB Cluster, selecting CONNECT > Connect to your Application and replacing with correct password and database name
  - MONGO_DB: database name in use

- Under Deploy tab, choose the branch and click Enable Automatic Deploys in the Automatic Deploys section.

Note: ensure you have a Procfile and requirements.txt indicating language and packs required to run the application on your repository.

### Download project to local IDE:

- Navigate to [GitHub Repository](https://github.com/belaventer/healthy-meal-planner).
- Click in Code and choose the local download method:
  - ZIP file - unpack - run on local IDE
  - Copy Git URL - open IDE terminal - run git clone
- A clone of the project is now available on your machine.

Note: ensure you have the configuration variables defined in the env.py file and the you install the requirements for the application.

`- pip install -r requirements.txt`

### Fork project:

- Navigate to [GitHub Repository](https://github.com/belaventer/healthy-meal-planner).
- Click in Fork. A duplicate repo will be created for your user.

Further information on [GitHub Docs](https://docs.github.com/en).



## Credit

### Content

This web application was based on the guidelines published by [Live Health Online](https://livehealthonline.com/wp-content/uploads/2018/05/lho-wmp-1800-calorie-meal-plan.pdf).

### Media

Logo was created using [Canva](https://www.canva.com/) and edit with [Clip Studio Paint](https://www.clipstudio.net/en/).

No Image Available was created using [Canva](https://www.canva.com/).

### Code

Favicon added as per ["Add A Favicon to A Website in HTML | Learn HTML and CSS | HTML Tutorial | HTML for Beginners"](https://www.youtube.com/watch?v=kEf1xSwX5D8) by Dani Krossing

Register / Login, Logout and Select Validation functionalities taken from the Task Manager Mini Project of [Code Institute](https://codeinstitute.net/) LMS.

Use of category for flashing messages explanation found in [Teclado Blog](https://blog.teclado.com/flashing-messages-with-flask/).

Example on how to use AJAX to connect JavaScript and Python found in [Stack Overflow](https://stackoverflow.com/questions/13808187/how-can-i-call-a-specific-function-method-in-a-python-script-from-javascriptjqu)

How to append in Jinja solution found in [Stack Overflow](https://stackoverflow.com/questions/49619445/how-to-append-to-a-list-in-jinja2-for-ansible )

Use of wildcard to search MongDB found in [Stack Overflow](https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo)

Uploading files following example of [Flask](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/)

[W3Schools](https://www.w3schools.com/) was referenced throughout the project for HTML, CSS and Python references.

How to remove floats from the string with python solution by [Stack Overflow](https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string).

[jQuery Documentation](https://api.jquery.com/) was referenced throughout the project for jQuery references.

### Acknowledgment

I would like to thank my mentor Gerry McBride for insightful tips and suggestions. 

## Disclaimer

This project purpose is only educational.