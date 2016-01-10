#!/usr/bin/python

from TriggerHorn import triggerHorn
from SecretKey import getGithubSecretKey

import json
from flask import jsonify
import requests

import flask
app = flask.Flask(__name__)
#app.config['DEBUG'] = True

@app.route("/")
###############################################################################
def hello():
  return "Webhooks Options:\n \n\\yo \n\\github"

###############################################################################
def sendSMS(number, message = "Yo!"):
  data = {"number":number, "message":message}
  requests.post("http://textbelt.com/text", data = data)

@app.route("/yo", methods=['GET'])
###############################################################################
def yo():
  username = flask.request.args.get('username')
  yo_text = "Yo!"
  if username is not None:
    yo_text = "Yo! from " + username
  data = {"callerID":yo_text, "extension":27000}
  requests.post("http://asterisk-02.west.sbhackerspace.com:8080/all", data = data)
  return 'yo', 200

@app.route("/github", methods=['POST'])
###############################################################################
def github():
  data = flask.request.get_json()
  try:
    githubSignature = flask.request.headers.get('X_HUB_SIGNATURE')[5:]

    localSignature = \
      hmac.new(getSecretGithubKey(), flask.request.get_data(), sha1).hexdigest()
    if constant_time_compare(githubSignature, localSignature):
      triggerHorn()
  except Exception as e:
    pass
  return 'github', 200

###############################################################################
###############################################################################
if __name__ == "__main__":
  try:
    app.run(host='0.0.0.0', port=80)
  except:
    print 'shit failed'
    exit()
