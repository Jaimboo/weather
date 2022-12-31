# **Weather WebApp**
> #### Video Demo: <URL HERE>
> #### Description: A basic webapp for visualize weather forecast providing detailed weather information and weather alerts for location all over the world.  

## **Introduction**
In this project i tried to recreate a basic web-app to consult weather information.

Into the web-app users are able to search for a certain location (or a deafult one has been chosen) and show weather info about the current or future days weather forecast, moreover they can sign in to store the preferred location to avoid searching.

The weather forecast are provided by [WeatherApi](https://www.weatherapi.com)

## **Requirements**
To Use the web app users must sign up to [WeatherApi](https://www.weatherapi.com) to obtain a personal secret key for api requests. The api key can be stored into the "config.cfg" file stored into the instance folder. The web app automatically create all the folders and all the required files on the first startup so just run the application with  `Flask --app weather run` than the config file will be created.

The project is created using [flask](https://flask.palletsprojects.com/en/latest/) framework and  [SQLite3](https://sqlite.org/about.html)

Use `pip install -r requirements.txt` to install all necessary dependencies.

# **WebApp explanation**

## **SQL**
For my project i only needed two tables into the database:
* user table to store users's account information
* favorite table to store information about the preferred location of all the users

## **FLASK**
The projects is composed by five python files that compose the app:
+ **\_\_init\_\_.py**: this is the origin file in which flask recall the configuration and import all the blueprint to create the app.
+ **config.py**: this file is used to add basic configuration info to the app and create the file `config.cfg` if does not exists yet.
+ **db.py**: contains all the function relative to the database usage.
+ **auth.py**: in this file are stored the view for login and registration that recalls the login and register templates to get user input and store the data into the database and into the session.
+ **api.py**: This file contains the remaining feature of the project:
    * the `index` function that check for a requested city, or use a default one, to show the first view in which the user can access to the current weather information;
    * the `days` function use another view to visualize some tables with more detailed data about the weather in three days;
    * `search` instead is the function that gets an user input to search for the requested city. This show a list of results and store the chosen one into the session;
    * `get_api` is the function that create the `api_response.json` if not exists and store in it the response of the requeste to the api. It also check if the old response is too old and update it only if necessary.
    * `search_api` is a function to request the list of results requested into the `search` view;
    * in addition to those function there are also four template filters used in jinja templates to format some data.

## **HTML, CSS AND JAVASCRIPT**
The design of the project is poorly treated and use the basics of [bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/) and just some css rules for make the project readable. Javascript is used to create a pagination system into the `days` template.

 ## **USAGE**
 1. Clone the repository.
 1. Run the command `pip install -r requirements.txt`.
 1. Once all the dependencies have been installed, run the command `flask --app weather run` and than stop it.
 1. Go to [WeatherApi](https://www.weatherapi.com/signup.aspx) signup page and register an account.
 1. [Login](https://www.weatherapi.com/login.aspx), if not automatically redirected, and access to the personal page.
 1. Copy the API key.
 1. After the first start the app has created the instance folder outside the app path. Here open `config.cfg` .and copy your api key into `SECRET_KEY`.
 1. Restart the app with `flask --app weather run`.