#!/usr/bin/python
import json
import requests

import flask
app = flask.Flask(__name__)

@app.route("/")
###############################################################################
def hello():
  return "Webhooks Options:\n \n\\yo \n\\github"

###############################################################################
def sendSMS(number, message = "Yo!"):
  data = {"number":number, "message":message}
  requests.post("http://textbelt.com/text", data = data)

@app.route("/yo")
###############################################################################
def yo():
  data = {"callerID":"Yo!", "extension":27000}
  requests.post("http://asterisk-02.west.sbhackerspace.com:8080/all", data = data)
  print "Yo Get"
  for number in phoneNumbers:
    sendSMS(number)
  return 'yo'

@app.route("/github")
###############################################################################
def github():
  print "github Post"
  return 'guthub'

###############################################################################
###############################################################################
if __name__ == "__main__":
  try:
    app.run(host='0.0.0.0', port=80)
  except:
    print 'shit failed'
    exit()
