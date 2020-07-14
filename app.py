from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
from SendEmail.sendEmail import EmailSender
from logger import logger
from email_templates import template_reader

app = Flask(__name__)



# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST']) 
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    candidate_name=parameters.get("candidate_name")
    #print(cust_name)
    candidate_about = parameters.get("candidate_about")
    candidate_email=parameters.get("candidate_email")
    candidate_resume= parameters.get("candidate_resume")
    candidate_about= parameters.get("candidate_about")
    candidate_location= parameters.get("candidate_location")
    candidate_no= parameters.get("candidate_no.")
    course_name= parameters.get("course_name.")
    candidate_experience= parameters.get("candidate_experience")
    intent = result.get("intent").get('displayName')
    if (intent=='About'):

        email_sender=EmailSender()
        template= template_reader.TemplateReader()
        email_message=template.read_course_template(course_name)
        email_sender.send_email_to_student(candidate_email,email_message)
        email_file_support = open("email_templates/support_team_Template.html", "r")
        email_message_support = email_file_support.read()
        email_sender.send_email_to_support(candidate_name=candidate_name,candidate_email=candidate_email,candidate_experience=candidate_experience,body=email_message_support)
        fulfillmentText="We have sent the course syllabus and other relevant details to you via email. An email has been sent to the Support Team with your contact information, you'll be contacted soon. Do you have further queries?"
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
 #   port = int(os.getenv('PORT', 5000))
 #   print("Starting app on port %d" % port)
    app.run()
