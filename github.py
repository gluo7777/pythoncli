
# Configure GitHub
# Store Credentials
import requests
import re
from config import *

# Project config
valid_repo_name = re.compile('^[a-zA-Z0-9_\- ]+$')
name_convention = re.compile(REPO_NAME_CONVENTION)


class Response:
    def __init__(self, status, message, payload={}):
        self.status = status
        self.message = message


def validate_repo_name(name):
    validation_result = {'valid': False, 'message': None}
    if valid_repo_name.fullmatch(name) is None:
        validation_result['message'] = "'%s' is not a valid repository name." % name
    elif name_convention.fullmatch(name) is None:
        validation_result['message'] = "'%s' is does not match the naming convention '%s'." % (
            name, REPO_NAME_CONVENTION)
    else:
        validation_result['valid'] = True
    return validation_result


def create_repo(name, description, private):
    # validate input
    validation = validate_repo_name(name)
    if not validation['valid']:
        return Response(False, validation['message'])

    # Build Request using good lib
    try:
        response = requests.post(url=API_ENDPOINT+'/user/repos', json={
            "name": name,
            "description": description,
            "private": private
        }, headers={
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }, auth=(USERNAME, PASSWORD), timeout=1.0)
        json = response.json()
        if response.status_code is 201:
            return Response(True, get_success_message(json), json)
        else:
            return Response(False, get_error_message(json), json)
    # Handle errors
    except (ConnectionError, KeyError) as e:
        return Response(False, e.message)


def get_success_message(json):
    return "Successfully created '%s'\
        \n%s\
        \ngit clone %s ." % (json['name'], json['html_url'], json['ssh_url'])


def get_error_message(json):
    # extract nested messages into single array
    messages = [f"'{error['message']}'" for error in json['errors']]
    # create single string delimited by a single EOL
    message = '\n'.join(messages)
    return "Unable to create repository.\
        \nReceived error message(s):\
        \n%s" % message


# Initialize local repo
# Get user input
# Handle error
# Pipe messages correctly
