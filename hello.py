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

API_TOKEN = "sc1PXIxCb5xlTbD9ixUK68F1"
EMAIL = "aatkinson@stutsmans.com"
AUTH = HTTPBasicAuth(EMAIL, API_TOKEN)
URL = "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/forms')
def forms():
    return render_template('forms.html')

@app.route('/create', methods=['POST'])
def create():
    output = request.get_json()
    # print(output) # This is the output that was stored in the JSON within the browser
    # print(type(output))

    result = json.loads(output) #this converts the json output to a python dictionary
    # print(result) #Printing the new dictionary
    # print(type(result)) #this shows the json converted as a python dictionary

    for key, value in result.items():
        if key == "form":
            if value == "onboard":
                # form = True
                summaryType = " - Onboarding"
            elif value == "offboard":
                # form = False
                summaryType = " - Offboarding"

        if key == "name":
            if value == "":
                raise Exception("ERROR: Invalid name! Please try again.")
            name = value

        if key == "date":
            if value == "":
                raise Exception("ERROR: Invalid date! Please try again.")
            else:
                date = value

                #SUMMARY DATE
                updateDate = date.split("-")   
                summaryDate = updateDate[1] + "/" + updateDate[2] + "/" + updateDate[0][-2:]    
                
                #DUE DATE
                dateObj = datetime.datetime.strptime(date, "%Y-%m-%d")
                daysAgo = datetime.timedelta(days=5)
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
        
        tasks = {}
        if key == "tasks":
            for i in value:
                if value[i] == "true":
                    tasks.update({"Contact Manager": {"checked":"true", "id":"10200"}})
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
    # print(tasks)
    print(list(tasks.values()))

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    #Creates an onboard issue
    # if (form):
    summary = summaryDate + " - " + name + summaryType
    createOnboard = json.dumps({
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

            #Onboarding Date
            "customfield_10101": date,

            #Company
            "customfield_10100": [{"value" : "Eldon C. Stutsman"}],

            #Department
            "customfield_10104": department,

            #Job Title
            "customfield_10103": jobTitle,

            #Employee ID
            "customfield_10107": employeeID,

            #Manager's Name
            "customfield_10105": manager,

            #Due Date
            "duedate": dueDate,

            #Request Type
            "customfield_10010": "st/newhires",

        }
    })
    data = createOnboard
    # else:
    #     summary = summaryDate + " - " + name + " - Offboarding"
    #     createOffboard = json.dumps({
    #         "fields": {
    #             "summary": summary,
    #             "issuetype": {
    #                 "id": "10002"
    #             },
    #             "components": [
    #             {
    #                 "id": "10534"
    #             }
    #             ],
    #             "project": {
    #             "id": "10001"
    #             },
    #             "description": {
    #                 "type": "doc",
    #                 "version": 1,
    #                 "content": [
    #                     {
    #                         "type": "paragraph",
    #                         "content": [
    #                             {
    #                                 "text": "This was a generated offboard issue by a Full Stack App.",
    #                                 "type": "text"
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             },
    #             "issuetype": {
    #                 "id": "10002"
    #             },
    #             #Request Type
    #             "customfield_10010": "st/dc693c21-9f78-4874-8fab-a0f26231b780",
    #             "duedate" : date
    #         }
    #     })
    #     data = createOffboard

    onCreate = requests.request(
        "POST",
        URL,
        data=data,
        headers=headers,
        auth=AUTH
    )

    global sendToJs
    sendToJs = json.loads(onCreate.text)
    # "{"id": "21827", "key": "ST-11552", "self": "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/21827"}"
    global issueKey
    issueKey = sendToJs["key"]

    # Edits a current issue
    payload = json.dumps( {
        "update": {
            "customfield_10200": [
                {
                    "set": list(tasks.values())
                }
            ]
        }
    } )

    onEdit = requests.request(
        "PUT",
        URL + issueKey,
        data=payload,
        headers=headers,
        auth=AUTH
    )
    # print(json.dumps(json.loads(onEdit.text), sort_keys=True, indent=4, separators=(",", ": ")))

    ticket = URL + issueKey
    return ticket

@app.route('/comments', methods=['POST'])
def addComments():
    output = request.get_json()
    result = json.loads(output)

    for key, value in result.items():
        if key == "otherInfo":
            otherInfo = value

        if key == "location":
            location = value

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

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

    response = requests.request(
        "POST",
        "https://stutsmans-sandbox-124.atlassian.net/rest/api/3/issue/" + issueKey + "/comment",
        data=payload,
        headers=headers,
        auth=AUTH
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

    return 

@app.route('/key', methods=['GET', 'PUT'])
def pythonJs():

    return sendToJs

# @app.route('/delete', methods=['DELETE'])
# def delete():
#     onDelete = requests.request(
#         "DELETE",
#         "https://stutsmans-sandbox-124.atlassian.net/rest/api/2/issue/" + issueKey 
#         auth=AUTH
#     )

    # print(json.dumps(json.loads(onDelete.text), sort_keys=True, indent=4, separators=(",", ": ")))

@app.route('/test')
def test():
    return render_template('test.html')