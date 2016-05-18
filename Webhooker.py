#!/usr/bin/python

from TriggerHorn import *
from SecretKey import *

import json
from flask import jsonify
import requests

import datetime
import flask
import hmac
import time
from hashlib import sha1
from django.utils.crypto import constant_time_compare

app = flask.Flask(__name__)

###############################################################################
def isAuthorized(username):
  if username in ['LOMANCER', 'MIKEKAPUSCIK', 'SLAPPLEBAGS']:
    return True
  elif 8 <= datetime.datetime.now().hour <= 20:
    return True
  else:
    return False

###############################################################################
def isAuthenticated(key, nonce, localTime, oneTimePassword):
  localOneTimePassword = getOneTimePassword(key, nonce, localTime)
  validHash = constant_time_compare(localOneTimePassword, oneTimePassword)
  validTimeDifference = abs(time.mktime(time.localtime()) - localTime) < 3
  return validHash and validTimeDifference

###############################################################################
@app.route("/")
def hello():
  return "Webhooks Options:\n \n/yo \n/yolights " + \
    "\n/yoworkroomlights \n/yoclassroomlights \n/github \n/sendyo"

###############################################################################
def sendSMS(number, message = "Yo!"):
  data = {"number":number, "message":message}
  requests.post("http://textbelt.com/text", data = data)

###############################################################################
@app.route("/yo", methods=['GET'])
def yo():
  username = flask.request.args.get('username')
  yo_text = "Yo!"
  if username is not None:
    yo_text = "Yo! from " + username
  data = {"callerID":yo_text, "extension":27000}
  requests.post("http://asterisk-02.west.sbhackerspace.com:8080/all", data = data)
  return 'yo', 200

###############################################################################
@app.route("/yolights", methods=['GET'])
def yoLights():
  username = flask.request.args.get('username')
  if isAuthorized(username):
    requests.get("http://classroom-lights.west.sbhackerspace.com/toggle")
    requests.get("http://workroom-lights.west.sbhackerspace.com/toggle")
  return 'yo', 200

###############################################################################
@app.route("/yoclassroomlights", methods=['GET'])
def yoClassroomLights():
  username = flask.request.args.get('username')
  if isAuthorized(username):
    requests.get("http://classroom-lights.west.sbhackerspace.com/toggle")
  return 'yo', 200

###############################################################################
@app.route("/yoworkroomlights", methods=['GET'])
def yoWorkroomLigts():
  username = flask.request.args.get('username')
  if isAuthorized(username):
    requests.get("http://workroom-lights.west.sbhackerspace.com/toggle")
  return 'yo', 200

###############################################################################
@app.route("/github", methods=['POST'])
def github():
  data = flask.request.get_json()
  try:
    githubSignature = flask.request.headers.get('X_HUB_SIGNATURE')[5:]

    localSignature = \
      hmac.new(getGithubSecretKey(), flask.request.get_data(), sha1).hexdigest()
    if constant_time_compare(githubSignature, localSignature):
      data = {"callerID":"Yo! from SBHXGITHUB", "extension":27000}
      requests.post("http://asterisk-02.west.sbhackerspace.com:8080/all", data = data)
      triggerHorn()
  except Exception as e:
    pass
  return 'github', 200

###############################################################################
@app.route("/sendyo", methods=['POST'])
def sendYo():
  inputData = flask.request.form
  nonce = str(inputData['nonce'])
  networkOneTimePassword = str(inputData['otp'])
  localTime = float(inputData['time'])

  if isAuthenticated(getYoSecretKey(), nonce, localTime, networkOneTimePassword):
    data = {'api_token' : getYoApiKey()}
    requests.post('https://api.justyo.co/yoall/', data = data)
  return 'Yo Sent', 200

###############################################################################
###############################################################################
if __name__ == "__main__":
  try:
    app.run(host='0.0.0.0', port=80)
  except:
    print 'shit failed'
    exit()
