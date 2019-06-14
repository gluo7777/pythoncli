from configparser import ConfigParser, RawConfigParser
from pathlib import Path

FILE_PATH = 'resources/config.ini'
GITHUB = 'GitHub'

# Specify global vars so they can be modified in local/function scope
file_parser = None
# Make sure file exists
config_file = Path(FILE_PATH)
assert all([config_file.exists()])
# Initialize parser
file_parser = RawConfigParser(allow_no_value=True,
                              comment_prefixes='#',
                              strict=True,
                              empty_lines_in_values=False)
file_parser.read(config_file)

# User configured values
USERNAME = file_parser[GITHUB]['username']
PASSWORD = file_parser[GITHUB]['password']
REPO_NAME_CONVENTION = file_parser[GITHUB]['repository_naming_convention']
API_ENDPOINT = file_parser[GITHUB]['api_endpoint']
