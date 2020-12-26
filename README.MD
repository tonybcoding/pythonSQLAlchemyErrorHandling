# UCasting - Captsone Project

## Introduction
This application provides a central location for movies and actors to be joined together by Executive Producers, Casting Directors, and Casting Assistants. 

From a technical perspective, this application implements the following models, endpoints, and roles to manage actors and movies:

* Models:
    - Movies with attributes title and release date
    - Actors with attributes name, age and gender

* Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/

* Roles:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies

    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

***

## Descriptin of Files
Root direcory
- app.py - main project methods with all API route and error handlers
- auth.py - contains all authentication methods
- casting_dump.sql - file to restore casting database prior to running local unit test
- manage.py - permits Heroku to manage SQL migrations
- models.py - contains SQLAlchemy Classes/Models
- Procfile - required for Heroku deployment
- PROJECT_SETUP_NOTES.MD - file containing personal notes while setting up project. Want to maintain for future reference.
- README.MD - provides instructions on testing APIs
- requirements.txt - installations required for virtual environment prior to testing application
- setup.sh - file containing Auth0 export variables
- test_app_hosted.py - provides full heroku deployed permissions testing
- test_app_unit_local.py - unit/local test for all endpoints
- test_config.py - variables shared among local and deployed testing files

***

## Repositories and other relevant locations

**GitHub Project Repository**
https://github.com/tonybcoding/burgefsndcapstone

**Auth0 tenant URL**
https://fsnd-finalproject-burge.us.auth0.com/

The following test users were established:
- executiveproducer@email.com - samepass!150
- castingdirector@email.com - samepass!150
- castingassistant@email.com - samepass!150
- public@email.com - samepass!150 (no permissions)

**Heroku**
* Heroku App URL: https://burgefsndcapstone.herokuapp.com/
* Heroku App Name: burgefsndcapstone
* Heroku Git URL: https://git.heroku.com/burgefsndcapstone.git

***

## Testing
***Local Unit Test***
The unit test provides thorough API endpoint testing covering all possible successes and entry errors. Also, since permissions are required, permissions of primary roles are tested. Thorough permission testing is available in the Remove test on heroku deployment below.

***Remote test on heroku deployment***
The remote test accessing the heroku deploymnet serves two purposes:
1. Prove effective deployment on heroku 
2. Attempt each endpoint action with each role provided success or failure based on permissions

### Local Unit Test
To run the local unit test, please following these steps:

1. Ensure casting database is in proper state by restoring the casting dabase to a local postgres instance. From the project root directory, run the following shell command:
    > psql -U postgres casting < casting_dump.sql 
*(Note, you may change postgres in the shell command to a local user name)*

2. Set up environment. In project root, execute the following shell command
    > source ./env/Scripts/activate

3. Run local test script from root directory
    > python test_app_unit_local.py


### Remote test on heroku deployment
To run the remote test, please execute the following shell command in the project root directory:
> python test_app_hosted.py

The evaluator may query the contents of the remote database via the follow psql command:
> psql postgres://gjawgoezjiifnn:2a0a19c51a380c84e12c7baa64b51d7ecd46d7404cd96e6f87dd8b479842e4dc@ec2-3-215-207-12.compute-1.amazonaws.com:5432/d3emg2dn5g2cbp