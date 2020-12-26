# Setup and Implementation Notes

## Specifications
I chose to stay with the casting agency for two reasons:
* following the concept of a customer providing specs/use cases
* consistency of terms if I need help with "Ask a Mentor"

**Description from UDacity**
```
The Casting Agency models a company that is responsible for creating movies and
managing and assigning actors to those movies. You are an Executive Producer
within the company and are creating a system to simplify and streamline your
process.

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

* Tests:
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role
```

## Platform
My development platform is:
* Windows 10 Pro
* Git bash shell


## Setup
1. create project directory and cd into that directory

2. initiate git repository locally
    * create .gitignore file

3. create virtual environment
    * run following in project root:
        - py -m venv env
    * run following in project root:
        - source ./env/Scripts/activate

4. update pip
    * python -m pip install --upgrade pip

5. Set up git remote origin
    * https://docs.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line
    * NOTE: after committing local changes, push them to remote with:
        - git push origin master

6. use psql to create database named casting
    * psql --username=postgres
    * create database casting;

7. I am not implementing the frontend; however, I created a directory structure with backend as I would in a project where both frontend and backend are included

8. Build Skeleton:
    * Build out skeleton route handlers
    * authenticate and authorize with Auth0
        - create application (casting-agency) as regular web application
            ```
            Log in to Auth0
            - create a new tenant
            - create new app
            - create one api (logical) with scope covering two endpoints (actors and movies)
            - created roles and assigned appropriate permissions
            - created test users:
                - executiveproducer@email.com - samepass!150
                - castingdirector@email.com - samepass!150
                - castingassistant@email.com - samepass!150
                - public@email.com - samepass!150 (no permissions)

            **To get web-based token (max 24 hours)**

https://fsnd-finalproject-burge.us.auth0.com/authorize?
audience=management&
response_type=token&
client_id=aCA7EjAuTW1h8cYBS8BnPz9lKXvKqlbM&
redirect_uri=http://127.0.0.1:5000/callback

            - Client secret: PnZGgR-m42u4e12Mpr81jgFc1J48O4mQBB6fNt6fQOZBu6hZ5bKdEQBMghcHLgHB
            - ID token expiration (30 days or 2592000 seconds)

            - to log out of domain in Auth0, use
                - https://fsnd-finalproject-burge.us.auth0.com/logout (change domain of course)

            - I logged in with test user to capture auth tokens for each role:
            - use jwt.io website to validate token. Then use those tokens to populate Postman below
            ```

9. Build out rest of app

10. Build unit tests
    * build out all endpoint tests with RBAC for success/failure
    * run full test

11. capture required packages (this must be executed to refresh after new packages installed):
    * pip freeze > requirements.txt

12. deploy on heroku
    - how to set and access evnironment variables
    - https://knowledge.udacity.com/questions/159048


## Daily project staging prior to continuing
* activate virtual env - change directory to project root and use following bash command:
    * source ./env/Scripts/activate
* running flask app with reload
    * export FLASK_APP=app.py
    * export FLASK_ENV=development
    * flask run
        - **(NOTE: MUST RUN THIS FROM DIRECTORY WHERE app.py IS LOCATED)**

## curl tests (prior to add authentication-authorization):

**get actors**
* valid entry
curl 'http://localhost:5000/actors'

**get movies**
* valid entry
curl 'http://localhost:5000/movies'

**add actor**
* valid entry
curl -X POST 'http://localhost:5000/actors' --header 'Content-Type: application/json' --data-raw '{"name": "Tony Mills", "dob": "12/13/1970", "gender": "M"}'

* valid entry
curl -X POST 'http://localhost:5000/actors' --header 'Content-Type: application/json' --data-raw '{"name": "Mary Poppins", "dob": "2/10/1975", "gender": "F"}'

* valid entry
curl -X POST 'http://localhost:5000/actors' --header 'Content-Type: application/json' --data-raw '{"name": "George Francios", "dob": "5/30/1968", "gender": "M"}'

* should fail: missing one or more required fields
curl -X POST 'http://localhost:5000/actors' --header 'Content-Type: application/json' --data-raw '{"name": "Tony", "dob": "12/13/1970"}'


**add movie**
* valid entry
curl -X POST 'http://localhost:5000/movies' --header 'Content-Type: application/json' --data-raw '{"title": "Freebird", "release_date": "10/4/2018", "cast": [1, 3]}'

* valid entry
curl -X POST 'http://localhost:5000/movies' --header 'Content-Type: application/json' --data-raw '{"title": "April Fools", "release_date": "4/1/2020", "cast": [1, 2, 3]}'

* should fail: cast is empty
curl -X POST 'http://localhost:5000/movies' --header 'Content-Type: application/json' --data-raw '{"title": "Racing Rain", "release_date": "6/3/2017", "cast": []}'

* should fail: missing one or more required fields
curl -X POST 'http://localhost:5000/movies' --header 'Content-Type: application/json' --data-raw '{"title": "Racing Rain", "cast": [1, 2]}'


**delete movie**
* valid id
curl -X DELETE 'http://localhost:5000/movies/1'

* should fail: didn't find id
curl -X DELETE 'http://localhost:5000/movies/-1'


**delete actor**
* valid id
curl -X DELETE 'http://localhost:5000/actors/1'

* should fail: didn't find id
curl -X DELETE 'http://localhost:5000/actors/-1'


**update movie**
* change title only
curl -X PATCH 'http://localhost:5000/movies/1' --header 'Content-Type: application/json' --data-raw '{"title": "Freebird & Willy"}'

* add new cast members
curl -X PATCH 'http://localhost:5000/movies/1' --header 'Content-Type: application/json' --data-raw '{"title": "Freebirds", "cast": [1, 2, 3]}'

* should fail: didn't find id
curl -X PATCH 'http://localhost:5000/movies/-1' --header 'Content-Type: application/json' --data-raw '{"title": "Freebird & Willy"}'

* should fail: no recognized fields
curl -X PATCH 'http://localhost:5000/movies/-1' --header 'Content-Type: application/json' --data-raw '{"uselessfield": "whatever"}'

* should fail: cast list present but empty
curl -X PATCH 'http://localhost:5000/movies/1' --header 'Content-Type: application/json' --data-raw '{"title": "Freebirds", "cast": []}'


**update actor**
* change name and date of birth
curl -X PATCH 'http://localhost:5000/actors/1' --header 'Content-Type: application/json' --data-raw '{"name": "Joel Blankenship", "dob": "4/3/1981"}'

* should fail: didn't find id
curl -X PATCH 'http://localhost:5000/actors/-1' --header 'Content-Type: application/json' --data-raw '{"name": "Joel Blankenship", "dob": "4/3/1981"}'

* should fail: no recognized fields
curl -X PATCH 'http://localhost:5000/actors/1' --header 'Content-Type: application/json' --data-raw '{"uselessfield": "whatever"}'
