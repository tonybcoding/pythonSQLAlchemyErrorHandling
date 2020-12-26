#########################################################################
#
# @file name: test_app_hosted.py
# @purpose: test file of backend app on hosted heroku instance
# @out_of_scope: no need to test every possible error. that is conducted
# in the unit tests of test_app_unit_local.py
# @author: Tony Burge
# @date: 2020-09-12
#
#########################################################################
#
#
# global imports
import requests
from flask import abort
from random import randint
#
# local imports
from test_config import ACCTS
from test_config import ACTORS, MOVIES
#
# constants
URL = "https://burgefsndcapstone.herokuapp.com/"

#############################################################################
# helper functions
#############################################################################
#
# display greeting
def print_greeting():
    print("\n" * 50)
    print("#" * 80)
    print("Testing Casting Application deployed on Heroku")
    print("Submitted by Tony Burge")
    print("#" * 80)

# This function is called to set database to a known state
# Only executive producer role is used. If an error is encountered,
# likely due to expired JWT
def set_db_to_known_state():
    #
    # find executive producer JWT
    print("...finding Executive Producer account...", end='')
    for acct in ACCTS:
        if acct['type'] == "Executive Producer":
            break
    print("Success")
    #
    # set up header with permissions of executive producer
    header = {
        "Authorization": f"Bearer {acct['jwt']}",
        "Content-Type": "application/json"
    }
    #
    # delete all movies and actors. N:M relationships will be removed based
    # on SQLAlechemy ORM model implemented in models.py/app.py
    for resource in ["movies", "actors"]:
        print("...deleting all " + resource + "...", end='')
        resource_list = get_resource(acct, resource)
        for item in resource_list:
            res = (requests.delete(URL + f"{resource}/" + str(item['id']),
                   headers=header))
    #
    # add actors
    print("...adding actors...")
    for actor in ACTORS:
        payload = ('{"name": ' + '"' + actor[0] + '"' + ', "dob": ' + '"' +
                   actor[1] + '"' + ', "gender": ' + '"' + actor[2] + '"}')
        add_resource(acct, "actors", payload)
    #
    # add movies
    # must first get list of actors to add to each movie
    print("...adding movies...")
    actor_list = get_resource(acct, "actors")
    for movie in MOVIES:
        payload = ('{"title": ' + '"' + movie[0] + '"' +
                   ', "release_date": ' + '"' + movie[1] + '"' +
                   ', "cast": ' + '[')
        # choose random number to determine how many actors to add to movie
        # to match actor_list indeces, had to modify with -1 on len
        # then add one to represent a number from 1 to actors
        cast_num = randint(0, len(actor_list) - 1) + 1
        for x in range (0, cast_num):
            payload += str(actor_list[x]['id'])
            if x != cast_num - 1:
                payload += ", "
        payload += "]}"
        add_resource(acct, "movies", payload)
    #
    # display actors and movies
    print("...resulting database:")
    print("\n* Actors *")
    print(get_resource(acct, "actors"))
    print("\n* Movies *")
    print(get_resource(acct, "movies"))
    print("\n* Database Ready *\n\n")

# function to get actor or movie list based on "resource" argument passed
def get_resource(acct, resource):
    #
    url = URL + resource
    header = {
      "Authorization": f"Bearer {acct['jwt']}",
      "Content-Type": "application/json"
    }
    res = requests.get(url, headers=header)
    if res.json()['success']:
        resource_list = res.json()[f'{resource}']
        print("Success")
    else:
        resource_list = []
        print("Failed: " + res.json()['message'])
    return resource_list

# function to add new actor or movie based on "resource" agrument passed
def add_resource(acct, resource, payload):
    #
    url = URL + resource
    header = {
      "Authorization": f"Bearer {acct['jwt']}",
      "Content-Type": "application/json"
    }
    print("......adding: " + payload + "...", end='')
    res = requests.post(url, data=payload, headers=header)
    if res.json()['success']:
        print("Success" )
    else:
        print("Failed: " + res.json()['message'])

# function to update actor or movie based on "resource" argument based
def update_resource(acct, resource, payload, id):
    #
    url = URL + resource + "/" + str(id)
    header = {
      "Authorization": f"Bearer {acct['jwt']}",
      "Content-Type": "application/json"
    }
    res = requests.patch(url, data=payload, headers=header)
    if res.json()['success']:
        print("Success" )
    else:
        print("Failed: " + res.json()['message'])

# function to delete actor or movie based on id
def delete_resource(acct, resource, id):
    #
    url = URL + resource + "/" + str(id)
    header = {
      "Authorization": f"Bearer {acct['jwt']}",
      "Content-Type": "application/json"
    }    
    res = requests.delete(url, headers=header)
    if res.json()['success']:
        print("Success" )
    else:
        print("Failed: " + res.json()['message'])

##########################################################################
# MAIN APP
##########################################################################
#
# display greeting and set database to known state
print_greeting()
print("\n* Setting database to known state at start of test *")
set_db_to_known_state()
#
# ------------------------------------------------------------------------
# GET ACTORS and MOVIE TESTS
# ------------------------------------------------------------------------
print("----------------------------------------------------------------")
print("GET tests for each account type")
for acct in ACCTS:
    print("\n" + acct['type'])
    print("...get actors...", end='')
    get_resource(acct, "actors")
    print("...get movies...", end='')
    get_resource(acct, "actors")

# ------------------------------------------------------------------------
# POST / ADD ACTOR and MOVIE TESTS
# ------------------------------------------------------------------------
print("\n----------------------------------------------------------------")
print("POST tests to add actor for each account type")
for acct in ACCTS:
    print("\n" + acct['type'])
    print("...add actor...", end='')
    # can use same actor info. duplicates allowed.
    payload = ('{"name": "AddTest Actor", "dob": "1/1/2000", "gender": "F"}')
    add_resource(acct, "actors", payload)
#
print("\n----------------------------------------------------------------")
print("POST tests to add movie for each account type")
for acct in ACCTS:
    print("\n" + acct['type'])
    #
    # must get actor ids here using role with permission. actor ids can't be
    # random as enpoint API checks for valid actor ids
    if acct['type'] == "Executive Producer":
        actor_list = get_resource(acct, "actors")
        actor_ids = ([actor_list[0]['id'], actor_list[1]['id'],
                     actor_list[2]['id']])
    print("...add movie...", end='')
    # can use same movie info. duplicates allowed.
    payload = ('{"title": "AddTest Movie", "release_date": "2/2/2002", "cast"')
    payload += f': {actor_ids}' + '}'
    add_resource(acct, "movies", payload)

# ------------------------------------------------------------------------
# PATCH / UPDATE ACTOR and MOVIE TESTS
# ------------------------------------------------------------------------
#
# must get actor and movie ids using account with known permissions
# as endpoing APIs check for valid ids before performing this action
actor_list = get_resource(ACCTS[0], "actors")
movie_list = get_resource(ACCTS[0], "movies")
#
print("\n----------------------------------------------------------------")
print("PATCH tests to update an actor record for each account type")
for acct in ACCTS:
    print("\n" + acct['type'])
    actor_to_update = actor_list[0]['id']
    print("...update actor...", end='')
    # can update with same info. no checks on if update info is same
    # as existing
    payload = '{"name": "UpdateTest Actor"}'
    update_resource(acct, "actors", payload, actor_to_update)
#
print("\n----------------------------------------------------------------")
print("PATCH tests to update a movie record for each account type")
for acct in ACCTS:
    print("\n" + acct['type'])
    movie_to_update = movie_list[0]['id']
    print("...update movie...", end='')
    # can update with same info. no checks on if update info is same
    # as existing
    payload = '{"title": "UpdateTest Movie"}'
    update_resource(acct, "movies", payload, movie_to_update)

# ------------------------------------------------------------------------
# DELETE ACTOR and MOVIE TESTS
# ------------------------------------------------------------------------
#
# must get actor and movie ids using account with known permissions
# as endpoing APIs check for valid ids before performing this action
actor_list = get_resource(ACCTS[0], "actors")
movie_list = get_resource(ACCTS[0], "movies")
#
print("\n----------------------------------------------------------------")
print("DELETE tests to delete an actor record for each account type")
#
x = 0
for acct in ACCTS:
    print("\n" + acct['type'])
    actor_to_delete = actor_list[x]['id']
    print("...delete actor...", end='')
    delete_resource(acct, "actors", actor_to_delete)
    x += 1  # this is used to index to next actor after previous deleted
#
print("\n----------------------------------------------------------------")
print("DELETE tests to delete a movie record for each account type")
#
x = 0
for acct in ACCTS:
    print("\n" + acct['type'])
    movie_to_delete = movie_list[x]['id']
    print("...delete movie...", end='')
    delete_resource(acct, "movies", movie_to_delete)
    x += 1  # this is used to index to next actor after previous deleted
