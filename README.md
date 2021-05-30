# Healthy Meal Planner!

![Healthy Meal Planner Website](/assets/images/website-mockup.jpeg "Healthy Meal Planner Website")

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

6. As a user, I want to be able to copy, update or delete the meal options and plan.

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

| Collection Name              | Document's Keys                                              |
| ---------------------------- | ------------------------------------------------------------ |
| users                        | username: String<br />password: String (hashed)<br />admin: Boolean |
| daily_intake* (admin only)   | total_calories: Int32<br />breakfast {<br />    protein: Int32,<br />    grain: Int32,<br />    fruit: Int32,<br />    fat: Int32}<br />lunch{<br />    protein: Int32,<br />    grain: Int32,<br />    vegetables: Int32,<br />    fruit: Int32,<br />    fat: Int32}<br />dinner{<br />    protein: Int32,<br />    grain: Int32,<br />    vegetables: Int32,<br />    fat: Int32}<br />snack{<br />    protein: Int32,<br />    carbohydrate: Int32} |
| serving_options (admin only) | category: String<br />ingredient: String<br />quantity: Int32<br />engineering_unit: String |
| built_meals                  | meal_name: String<br />created_by: String<br />servings_selected: Array of ObjectIDs<br />servings_quantities: Array of Int32 |
| build_plans                  | plan_start_date: Date<br />plan_end_date: Date<br />create_by: String<br />meals_selected: List String<br />groceries_list: List String |

*This collection is part of the future scope.

### Skeleton

- [Layout](wireframes/healthy-meal-planner-skeleton.jpg)

### Surface

#### Colour

The website will use grey background colours and the following accents for each serving category.

- Protein / Carbohydrate: red
- Grain: yellow
- Fat: orange
- Fruit: blue
- Vegetables: green

 

#### Typography

The default typography of Materialize will be used throughout.



## Features

**Home Page**: simple welcoming text explaining the purpose of the website.

**Login / Register Page**: form allowing to the user to Register or Log In to application.

**Profile Page**: main page when the user is logged in. It will display all the saved meals from the database of the user in session.

### Existing Features

- **Navigation Bar:** The navigation bar is present at the top and collapses to a side bar for mobile view. The options present on the navigation bar, are conditional to the amount of credentials of the session.

### Features left to implement



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

- <!--[AutoPrefixer](https://autoprefixer.github.io): -->
  <!--Used on CSS to ensure functionality across browsers.-->

- [jQuery API](https://api.jquery.com/):
  Used for Materialize components initialization.

- 

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

- 

## Credit

### Content

This web application was based on the guidelines published by [Live Health Online](https://livehealthonline.com/wp-content/uploads/2018/05/lho-wmp-1800-calorie-meal-plan.pdf).

### Media

Logo was created using [Canva](https://www.canva.com/) and edit with [Clip Studio Paint](https://www.clipstudio.net/en/).

### Code

Favicon added as per ["Add A Favicon to A Website in HTML | Learn HTML and CSS | HTML Tutorial | HTML for Beginners"](https://www.youtube.com/watch?v=kEf1xSwX5D8) by Dani Krossing

Register / Login and Logout functionality taken from the Task Manager Mini Project of [Code Institute](https://codeinstitute.net/) LMS.

Use of category for flashing messages explanation found in [Teclado Blog](https://blog.teclado.com/flashing-messages-with-flask/).

### Acknowledgment



## Disclaimer

This project purpose is only educational.