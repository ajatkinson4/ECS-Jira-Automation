#######################################################
# This file, hello.py, is the backend of this full stack web application.
# Using the Python framework, Flask, allows the web app to run on a local server
# to make development easier. Flask uses a URL route, `app.route('/example')`, to render
# the html file used in the frontend, or to recieve html values from the frontend
# that can be used in backend functions.
#
# To run Flask on this file, follow these steps (command-line):
# `. flask/bin/activate`
# `export FLASK_APP="backend.py"`
# `flask run`
#######################################################

# Imported libraries #
from crypt import methods
import json
import sys
from telnetlib import STATUS
from turtle import update
from flask import request
from flask import Flask, render_template
import requests
from requests.auth import HTTPBasicAuth
import datetime

# These are global varibales that can be called from anywhere in the file:
#######################################################
# API_TOKEN = uniquely gernerated through Jira
# EMAIL = Jira account email address
# AUTH = an HTTP request to allow REST API access to Jira
# URL = Company's Jira link in JSON format.
#       JSON is a data interchange format that uses human-readable text
#       to store and transmit data objects consisting of attribute–value pairs and arrays.
#HEADERS = JSON requirement for HTTP requests
#######################################################
API_TOKEN = "sc1PXIxCb5xlTbD9ixUK68F1" 
EMAIL = "aatkinson@stutsmans.com"
AUTH = HTTPBasicAuth(EMAIL, API_TOKEN)
URL = "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

app = Flask(__name__) #Create varibale for Flask

# Homepage of the full stack web app that calls the file, `home.html` 
# (Find `home.html` in the project folder for details)
@app.route('/')
def index():
    return render_template('home.html')

# Forms page that calls the file, `forms.html`
# (Find `forms.html` in the project folder for details)
@app.route('/forms')
def forms():
    return render_template('forms.html')


# The function `create()` uses the HTTP POST request to create either
# an onboarding or offboarding ticket in Jira. Later, the function
# uses the HTTP PUT request to edit/update the new created ticket's 
# fields with the approriate values given by the html values in `forms.html`.
#
# THIS FUNCTION RUNS WHEN A FORM HAS BEEN SUBMITTED #
@app.route('/create', methods=['POST'])
def create():
    output = request.get_json() # gets the html values from `forms.html`

    result = json.loads(output) # converts the html values output to a Python dictionary
    # print(result)

    # Example #
    # {'form': 'onboard', 'name': 'Alex Atkinson', 'date': '2022-09-27', 'manager': 'Matt Mapel', 
    #   'description': 'This is the description.', 'company': '10116', 'department': 'IT', 
    #   'jobTitle': 'Intern', 'employeeID': '12345', 'tasks': {'AD': 'true', 'email': 'true', 
    #   'computer': 'true', 'agvantage': 'true', 'paperwise': 'true', 'officePhone': 'true', 
    #   'mobile': 'true', 'fob': 'true', 'print': 'true'}}

    # Iterate through the result dictionary in a "key, value" format
    # These iterations will first check the dictionaries key to see if it exists
    # in the dict. If it does, then assign the value to a variable that will later be used.
    # Otherwise, if it's not in the dict, then check for next key.
    #
    # The keys of the dictionary come from `forms.html`. The key's name comes from the 
    # varibale that is assigned to the specific html value. 
    # (See the function `createForm()` in `forms.html`)
    for key, value in result.items():
        if key == "form": # check what type of form is recieved
            if value == "onboard": # onboard = True
                form = True
                summaryType = " - Onboarding"
            elif value == "offboard": # offboard = False
                form = False
                summaryType = " - Offboarding"
            # The `form` variable is later used to specify which type of ticket to create in Jira

        if key == "name": 
            name = value

        if key == "date":
            date = value

            # SUMMARY DATE #
            # Converts the given date format, `2022-09-27`, to 9/27/2022
            updateDate = date.split("-")   
            summaryDate = updateDate[1] + "/" + updateDate[2] + "/" + updateDate[0][-2:]    
            
            # DUE DATE #
            # Converts the date format into the format required for the custom jira field
            dateObj = datetime.datetime.strptime(date, "%Y-%m-%d")
            daysAgo = datetime.timedelta(days=5) # specify how many days before the given date
            dueDate = dateObj - daysAgo
            dueDate = str(dueDate.strftime('%Y-%m-%d'))

        if key == "manager":
            manager = value

        if key == "description":
            description = value

        if key == "company":
            company = value

        if key == "department":
            department = value

        if key == "jobTitle":
            jobTitle = value

        if key == "employeeID":
            employeeID = value


        #######################################
        ############## IMPORTANT ##############
        #######################################
        # Each custom field in Jira has a `customfield_id` that must be specified in order to update the field.
        # The custom field checklist is trickier because each created item has its own unique id.
        # You MUST be sure to have the correct ids for each customfield / items.
        # A previous problem was when the Sandbox was updated. Majority of the custom fields were changed, therefore
        # the program crashed because it did not know the new ids.
        # Below is a commented dictionary of the item's names and their unique ids for reference.
        # 
        # tasks = {
        #          "Contact Manager": {"checked":"false", "id":10200},
        #          "Create user in AD":{"checked":"false", "id":10201} - AD account needed?,
        #          "Assign user to AD groups":{"checked":"false", "id":10202} - AD account needed?,
        #          "Assign M365 license":{"checked":"false", "id":10203} - Email address needed?,
        #          "Setup workstation":{"checked":"false", "id":10204},
        #          "Add computer into AD security group":{"checked":"false", "id":10205} - Computer needed?,
        #          "Install Office":{"checked":"false", "id":10206} - Computer needed?,
        #          "Install and configure AgVantage":{"checked":"false", "id":10207} - AgVantage needed?,
        #          "Setup OneDrive":{"checked":"false", "id":10208} - Computer needed?,
        #          "Configure mobile phone":{"checked":"false", "id":10209} - Mobile phone needed?,
        #          "Configure desk phone":{"checked":"false", "id":10210} - Office phone needed?,
        #          "Turn on MFA":{"checked":"false", "id":10211},
        #          "Add user to KnowBe4":{"checked":"false", "id":10212},
        #          "Add user to CodeTwo signature group":{"checked":"false", "id":10212},
        #          "Configure door fob":{"checked":"false", "id":10214} - Key Fob needed?,
        #          "Add to document portal":{"checked":"false", "id":10215},
        #          "Verify computer":{"checked":"false", "id":10216} - Computer needed?,
        #          "Print welcome packet":{"checked":"false", "id":10217} - Welcome form printed?,
        #          "Install and configure Paperwise":{"checked":"false", "id":10218} - Paperwise needed?,
        #          }
        #
        #
        # The key `tasks` is different from the others
        # `tasks` is used to update the custom checklist in Jira
        # The value of `tasks` is a dictionary, so an iteration is required
        # to check whether or not to mark the item as "true" in the checklist.
        #
        # The varibale "tasks" is a dictionary, (do not confunse the varibale "tasks" and the key `tasks`),
        # that gets updated according to the key's value inside the value of tasks.
        # If the key's value is "true", then check if the key matches the given variable name in `forms.html`
        # and update the dictionary "tasks" with the item name, checked:true, id
        # 
        # Example #
        # {'tasks': {'AD': 'true', 'email': 'true', 'computer': 'true', 'agvantage': 'true', 'paperwise': 'true', 
        #            'officePhone': 'true', 'mobile': 'true', 'fob': 'true', 'print': 'true'}}
        #
        # key = 'tasks'
        # value = {'AD': 'true', 'email': 'true', 'computer': 'true', 'agvantage': 'true', 'paperwise': 'true', 
        #          'officePhone': 'true', 'mobile': 'true', 'fob': 'true', 'print': 'true'}
        # value[i] = {'true','true','true','true','true','true','true','true','true'}
        # i = {'AD', 'email', 'computer', 'agvantage', 'paperwise', 'officePhone', 'mobile', 'fob', 'print'}
        #
        # For all items that are "true", tasks.update(item name, checked:true, id)
    
        tasks = {}
        tasks.update({"Contact Manager": {"checked":"true", "id":"10200"}}) # Always contact manager
        if key == "tasks":
            for i in value:
                if value[i] == "true":
                    if i == "AD":
                        tasks.update({"Create user in AD":{"checked":"true", "id":"10201"}})
                        tasks.update({"Assign user to AD groups":{"checked":"true", "id":"10202"}})

                    if i == "email":
                        tasks.update({"Assign M365 license":{"checked":"false", "id":"10203"}})

                    if i == "computer":
                        tasks.update({"Add computer into AD security group": {"id":"10205", "checked":"true"}})
                        tasks.update({"Install Office": {"id":"10206", "checked":"true"}})
                        tasks.update({"Setup OneDrive": {"id":"10208", "checked":"true"}})
                        tasks.update({"Add to document portal":{"checked":"false", "id":"10215"}})
                        tasks.update({"Verify computer": {"id":"10216", "checked":"true"}})

                    if i == "agvantage":
                        tasks.update({"Install and configure AgVantage":{"checked":"true", "id":"10207"}})

                    if i == "paperwise":
                        tasks.update({"Install and configure Paperwise":{"checked":"true", "id":"10218"}})

                    if i == "officePhone":
                        tasks.update({"Configure desk phone":{"checked":"true", "id":"10210"}})

                    if i == "mobile":
                        tasks.update({"Configure mobile phone": {"checked":"true", "id":"10209"}})

                    if i == "fob":
                        tasks.update({"Configure door fob":{"checked":"true", "id":"10214"}})

                    if i == "print":
                        tasks.update({"Print welcome packet":{"checked":"true", "id":"10217"}})
                        tasks.update({"Setup workstation":{"checked":"false", "id":"10204"}})

    # print(list(tasks.values()))

    # Creates an Employee Onboarding
    # The format of `json.dumps()` is a direct copy from the Jira documentation.
    # It uses a "field" key to specify the field you want to update, and the value 
    # of that specified field. Almost all field values are of type string, but fields
    # such as the "Company customfield_10100", takes in a list of dictionaries. 
    # The format of all field values can be found in the Atlassian documentation.
    if (form):
        summary = summaryDate + " - " + name + summaryType
        createOnboard = json.dumps({
            "fields": {
                "summary": summary, #Updates summary
                "issuetype": { 
                    "id": "10002" # Specify issue type with unique id
                },

                "components": [
                {
                    "id": "10534"
                }
                ],

                "project": {
                    "id": "10001" # Specify unique project key/id
                },

                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": description, #Description's text is the html value from `forms.html`
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                },
                # Assignee
                "assignee": {"accountId": "62c49022efb17d6ce62ef3b9"}, # Personal account ID
                
                # These are the custom fields updated during ticket creation #
                #
                # Onboarding Date
                "customfield_10101": date, 

                # Company - "Eldon C. Stutsman"
                "customfield_10100": [{"value" : "Eldon C. Stutsman"}],

                # Department
                "customfield_10104": department,

                # Job Title
                "customfield_10103": jobTitle,

                # Employee ID
                "customfield_10107": employeeID,

                # Manager's Name
                "customfield_10105": manager,

                # Due Date
                "duedate": dueDate,

                # Request Type
                # The value of this field is the projectKey/requestTypeKey
                # newhires is the requestTypeKey for onboarding
                "customfield_10010": "st/newhires",

            }
        })
        data = createOnboard

    # Creates an Employee Offboarding #
    # Exact same format as the onboarding, but less custom fields needed.
    else:
        summary = summaryDate + " - " + name + summaryType
        createOffboard = json.dumps({
            "fields": {
                "summary": summary,
                "issuetype": {
                    "id": "10002"
                },
                "components": [
                {
                    "id": "10534"
                }
                ],
                "project": {
                "id": "10001"
                },
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "text": description,
                                    "type": "text"
                                }
                            ]
                        }
                    ]
                },
                #Assignee
                "assignee": {"accountId": "62c49022efb17d6ce62ef3b9"},

                #Offboarding Date
                "customfield_10102": date,

                #Company
                "customfield_10100": [{"value" : "Eldon C. Stutsman"}],

                # Department
                "customfield_10104": department,

                #Manager's Name
                "customfield_10105": manager,

                #Due Date
                "duedate": dueDate,

                #Request Type
                # requestTypeKey for offboarding = dc693c21-9f78-4874-8fab-a0f26231b780
                "customfield_10010": "st/dc693c21-9f78-4874-8fab-a0f26231b780",

            }
        })
        data = createOffboard

    # `requests.request()` is the HTTP request for POST.
    # (Variables that are all caps are global variables)
    # The following parameters are required:
    #
    # Request type = a string of either POST, PUT, GET, or DELETE (HTTP requests)
    # URL = the JSON url to send the information. (Variables that are all caps are global variables)
    # data = the JSON data to send
    # headers = JSON requirement
    # auth = the authentication of a Jira account and an API key
    onCreate = requests.request(
        "POST",
        URL,
        data=data,
        headers=HEADERS,
        auth=AUTH
    )
    #######################################################

    # To update the custom field checklist in Jira, it requires an HTTP PUT request
    # to edit the Jira ticket. Another VERY IMPORTANT piece to the PUT request is the
    # `issueKey`. The issueKey is needed to tell Jira which ticket to edit. To get the 
    # issueKey, we take the response of the POST method, called "onCreate", which is 
    # returned as a dictionary. Meaning, we can search the dictionary for it's issueKey value.
    #
    # The "global" type before `sendJs` and `issueKey` is needed if the variable is going to be 
    # used outside of the `create()` function, which will be explained and seen later.
    global sendToJs
    sendToJs = json.loads(onCreate.text)
    # "{"id": "21827", "key": "ST-11552", "self": "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/21827"}"
    global issueKey
    issueKey = sendToJs["key"] # Since we know that "key" is a key name of the dictionary 
                               # is always there, we do not need to iterate the dictionary to check.

    # Edits a current issue
    # Same JSON format as the "createOn/Offboard", but this time
    # "update" is used to edit the custom field checklist.
    # Tasks Checklist's value is a list of dictionaries which uses "set"
    # that takes in its own list of dictionaries, which is why a list 
    # is casted around the dictionary of values.
    # Only the values of "tasks" are needed to update the custom field.
    payload = json.dumps( {
        "update": {
            # Tasks Checklist
            "customfield_10200": [
                {
                    "set": list(tasks.values())
                }
            ]
        }
    } )

    # The same idea as `onCreate`, but `onEdit` uses a slightly differet
    # url that appends the newly found "issueKey" of the newly created Jira ticket
    onEdit = requests.request(
        "PUT",
        URL + issueKey, # https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/{issueKey}
        data=payload,
        headers=HEADERS,
        auth=AUTH
    )
    # print(json.dumps(json.loads(onEdit.text), sort_keys=True, indent=4, separators=(",", ": ")))

    ticket = URL + issueKey # URL for the newly created ticket
    return ticket

# The function `addComments` uses an HTTP POST request
# to post the HTML values of value inputed in the text area by the user.
# Jira or HTTP did not like an overload of HTTP requests for one function,
# so a workaround was needed. The function is the same concept as the previous,
# where an iteration is needed to check for HTML values, and also is a direct copy
# from Jira documentation.
@app.route('/comments', methods=['POST'])
def addComments():
    output = request.get_json()
    result = json.loads(output)

    for key, value in result.items():
        if key == "otherInfo":
            otherInfo = value

        if key == "location":
            location = value

    payload = json.dumps( {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                    {
                        "text": otherInfo + "\n",
                        "type": "text"
                    },
                    {
                        "text": location,
                        "type": "text"
                    }
                    ]
                }
            ]
        }
    })

    # This request useses its own unique url by adding "/comment" to the end.
    # This is another reason why a new function is needed. 
    response = requests.request(
        "POST",
        "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/" + issueKey + "/comment",
        data=payload,
        headers=HEADERS,
        auth=AUTH
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

#######################################################
# This function allows the frontend to use the Python value, `sendToJs`
# `sendToJs` is the global variable used in the `create()` function,
# which was previously explained. So, this means, once the ticket is created, 
# the issueKey value is sent to the frontend which is then used to make 
# a button locate the browser to the new Jira ticket. Essentially, this function
# gives the frontend the link to the new ticket.
@app.route('/key', methods=['GET', 'PUT'])
def pythonJs():
    return sendToJs

#######################################################
# NOT IN USE #
# This method is just an example of how to delete an issue from Jira.
# @app.route('/delete', methods=['DELETE'])
# def delete():
#     onDelete = requests.request(
#         "DELETE",
#         "https://stutsmans-sandbox-124.atlassian.net/rest/api/2/issue/" + issueKey 
#         auth=AUTH
#     )

    # print(json.dumps(json.loads(onDelete.text), sort_keys=True, indent=4, separators=(",", ": ")))