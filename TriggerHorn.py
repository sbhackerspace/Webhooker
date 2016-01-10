#!/usr/bin/python
# Dan Loman
# Description:
#   This script will generate one time passwords for triggering the github
#   horn at SBHX
import hmac
import hashlib
import random
import requests
import time
from SecretKey import getSecretKey

################################################################################
def getOneTimePassword(key, nonce, localTime):
  timeVal = [chr(int(i)) for i in str(int(localTime/10))[::-1]]
  timeVal = ''.join(timeVal)
  return hmac.new(key, nonce + timeVal, hashlib.sha256).hexdigest()

################################################################################
def getNonce():
  return '%030x' % random.randrange(16**30)

################################################################################
def triggerHorn():
  nonce = getNonce()
  localTime = time.mktime(time.localtime())
  data = \
    {'otp' : getOneTimePassword(getSecretKey(), nonce, localTime), \
    'nonce' : nonce.encode("hex"), \
    'time' : localTime}
  try:
    requests.post('http://horn.local/horn', data = data)
  except Exception:
    return

################################################################################
################################################################################
if __name__ == "__main__":
  triggerHorn()
