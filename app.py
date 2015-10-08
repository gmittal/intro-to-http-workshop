# Setup and configuration of the server
from flask import Flask, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
appPhoneNumber = os.environ.get("APP_PHONE_NUMBER")

client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)





# Where the real magic happens
@app.route("/", methods=['GET', 'POST']) # handler for all server traffic
def hello_cat(): # executes code when server traffic is received

    # Let's extract what the user sent in the SMS
    fromNumber = request.values.get('From', None) # get phone number
    messageBody = request.values.get('Body', None) # get text body

    # Only send them a cute cat picture if they use the special keyword
    if ("meow" in messageBody.lower()):

            # Print to the console that the user wants a meow meow
            print fromNumber + " wants a meow meow!"

            # send a cute cat picture to the user, using The Cat API
            message = client.messages.create(to=fromNumber, from_=appPhoneNumber,
                                             body="Meow Meow!",
                                             media_url=['http://thecatapi.com/api/images/get'])

    else: # if they don't use the special keyword, echo back what they said

            print "Aw, " + fromNumber + " doesn't want a meow meow..."

            message = client.messages.create(to=fromNumber, from_=appPhoneNumber,
                                             body=messageBody) # send a message





    return "Hello, Meow Meow!" # standard message which tells the server everything (200) OK







# Just tells the Python app to run, nothing to see here folks
if __name__ == "__main__":
    app.run(debug=True)
