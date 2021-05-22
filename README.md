# Healthy Meal Planner!

![Healthy Meal Planner Website](/assets/images/website-mockup.jpeg "Healthy Meal Planner Website")

[Demo of Website](#).

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
| users                        | username<br />password<br />admin                            |
| daily_intake* (admin only)   | daily_intake_name<br />breakfast_protein<br />breakfast_grain<br />breakfast_fruit<br />breakfast_fat<br />lunch_protein<br />lunch_grain<br />lunch_vegetables<br />lunch_fruit<br />lunch_fat<br />dinner_protein<br />dinner_grain<br />dinner_vegetables<br />dinner_fat<br />snack_protein<br />snack_carbohydrate |
| serving_options (admin only) | category<br />ingredient<br />quantity<br />engineering_unit |
| built_meals                  | meal_name<br />created_by<br />servings_selected             |
| build_plans                  | plan_start_date<br />plan_end_date<br />create_by<br />meals_selected |

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



### Existing Features



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

- <!--[Fonts Awesome v5.15](https://fontawesome.com/):-->
  <!--Used for the Settings (cog) and restart icons.-->

- [Typora](https://typora.io/#):
  Used for Markdown editing of README and TESTING files.

- [Clip Studio Paint](https://www.clipstudio.net/en/):
  Used for images development and editing.

- <!--[AutoPrefixer](https://autoprefixer.github.io):-->
  <!--Used on CSS to ensure functionality across browsers.-->

- <!--[jQuery API](https://api.jquery.com/):-->
  <!--Used during coding for element selection and promises.-->

- <!--[Jasmine](https://jasmine.github.io/):-->
  <!--Used for automated testing of function.-->

## Testing

Refer to [TESTING.md](TESTING.md) file for testing details.

## Deployment

This project was developed using the Gitpod IDE, committed to git and pushed to GitHub.

### Deploy to Heroku from GitHub Repository:

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



### Code



### Acknowledgment



## Disclaimer

This project purpose is only educational.