# ECS-Jira-Automation

*THERE IS NO API TOKEN INITIALIZED*
*MUST FOLLOW THE 'Jira Connection' STEPS BELOW BEFORE ANYTHING*

Jira Connection:
To connect to Jira, an account must be initialized using an email address and an API Token.
They will be stored in `backend.py` as the global variables `EMAIL` and `API_TOKEN`. 
To create an API Token, follow these steps:
* In Jira, click the account in the top right
* Click 'Manage Account'
* Open 'Security' settings
* Scroll to find 'API token' and click 'Create and manage API tokens'
* Click the blue 'Create API token'
* Give the new API token a name
* Click Create
A hidden API token should generate that will be able to copy. Once the unique
API token is copied, paste it into the global variable `API_TOKEN` to gain access to Jira.


How to run (command-line):
* Open terminal and cd to project
* Activate Flask:
  `. flask/bin/activate`
* Export backend file to flask:
  `export FLASK_APP="backend.py"`
* Run:
  `flask run`