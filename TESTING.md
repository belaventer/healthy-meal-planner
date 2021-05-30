# Healthy Meal Planner - Testing Protocol

[Demo of Website](https://healthy-meal-planner.herokuapp.com/).

Refer to [Main project file](README.md) for further detail.

## Code validation

- [W3C CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator/)
- [W3C Markup Validator](https://validator.w3.org/#validate_by_input)
- [JSHint Validator](https://jshint.com/)

<!--All HTML, CSS and JS files were validated with direct input and returned no errors at the time of this entry.-->

## User stories testing

1.	As a new visitor to the website, I want to understand the main concept of the plan.

![Home Page Text](screenshots/screenshot-user-story-1.png "Home Page Text")

    - As a new visitor, I understand the objective of the application with the welcoming Home page text.

2.	As a new visitor to the website, I want to find instructions on how to use the application.

![](# "")

    - 

3.	As a new visitor to the website, I want to register with the application.

![Log In / Register page](screenshots/screenshot-user-story-3.png "Log In / Register page"")

    - As a new visitor, I can navigate to Log In / Register page from the navigation bar and create a new account.

4.	As a user, I want to create meal options following the recommendation.

![](# "")

    - 

5.	As a user, I want to create a meal plan for the week.

![](# "")

    - 

## Manual testing of features

The deployed Heroku website was viewed on <!--2 desktops screens (21 and 13 inches) and also on Motorola G6 Play device.-->

The website was tested with <!--Google Chrome (v.##), Mozilla Firefox (v.##) and Microsoft Edge (v.##) browsers.-->

On mobile, it was viewed <!--with Google Chrome application v.## on Android #.-->

The Developer Tools of Google Chrome (v.##) on desktop was used to verify responsiveness on different devices.

1. **Home Page**:

   | Test No. | Action & expected results                                    | Pass / Fail |
   | -------- | :----------------------------------------------------------- | :---------- |
   | 1.1      | Enter https://healthy-meal-planner.herokuapp.com/ as the URL and verify the Home Page is displayed. | Pass        |

2. **Register / Log Out:**

   | Test No. | Action & expected results                                    | Pass / Fail |
   | -------- | :----------------------------------------------------------- | :---------- |
   | 2.1      | From the Navigation Bar, click on Log In / Register. Verify the Log In / Register page is loaded. | Pass        |
   | 2.2      | On the register side, enter a new user name and a password following the helper text and click Submit. Verify the Profile page for the created user is loaded. | Fail*       |
   | 2.3      | Click on the Log Out button on the Navigation Bar and verify the session is deleted and user is redirected to Home page. | Pass        |
   | 2.4      | Navigate to Log In / Register page and attempt to create the same user created on step 2.2. Verify a flash message is displayed indicating that the username already exists and registration does not complete. | Pass        |

   *As there was no meals prepared for the new user, there was the following error: "local variable 'servings_selected' referenced before assignment". Error was fixed with by declaring the servings_selected on the scope of route function.

3. **Log In:**

   | Test No. | Action & expected results                                    | Pass / Fail |
   | -------- | :----------------------------------------------------------- | :---------- |
   | 3.1      | Navigate to Log In / Register page and attempt to Log In using a random username and password. Verify a flash message is displayed indicating invalid username and / or password and log in does not complete. | Pass        |
   | 3.2      | Navigate to Log In / Register page and attempt to Log In using the username created in step 2.2 with an incorrect password. Verify a flash message is displayed indicating invalid username and / or password and log in does not complete. | Pass        |
   | 3.3      | Navigate to Log In / Register page and attempt to Log In using the username created in step 2.2 with the correct password. Verify the Profile page for the user is loaded. | Pass        |

4. :


   ### Known issues

   