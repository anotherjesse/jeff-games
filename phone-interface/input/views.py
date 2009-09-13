# Create your views here.
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from restclient import *

import twilio

# Twilio REST API version
API_VERSION = '2008-08-01'

# Twilio AccountSid and AuthToken
ACCOUNT_SID = 'YOUR_SID'
ACCOUNT_TOKEN = 'YOUR_TOKEN'

# Outgoing Caller ID previously validated with Twilio
CALLER_ID = 'YOUR_PHONE'

# Create a Twilio REST account object using your Twilio account ID and token
account = twilio.Account(ACCOUNT_SID, ACCOUNT_TOKEN)

def index(req, *args, **kwargs):
  return render_to_response('index.html', context_instance=RequestContext(req))


def play(req, *args, **kwargs):
  import twilio
  r = twilio.Response()
  g = r.addGather(action="/shoot", method="POST", finishOnKey="#", timeout="10")
  g.append(twilio.Say("Welcome to Jeff Game. Enter coordinates and press pound to fire.", voice=twilio.Say.MAN, language=twilio.Say.ENGLISH ))
  g.addSay("Ready?", voice=twilio.Say.WOMAN, language=twilio.Say.ENGLISH)
  r.addRedirect("/repeat")
  return HttpResponse(r,)

def repeat(req, *args, **kwargs):
  import twilio
  r = twilio.Response()
  g = r.addGather(action="/shoot", method="POST", finishOnKey="#", timeout="10")
  g.addSay("Ready?", voice=twilio.Say.WOMAN, language=twilio.Say.ENGLISH)
  r.addRedirect("/repeat")
  return HttpResponse(r,)


def shoot(req, *args, **kwargs):
  digits = ['1','2','3','4','5','6','7','8','9',]
  import twilio, sys, random
  try:
    digits = req.POST['Digits']
    x = digits[:1]
    y = digits[1:]
  except:
    digits = random.choice(digits) + random.choice(digits)
    x = digits[:1]
    y = digits[1:]
  target = "http://nasa.lovesthis.com/"
  # target = "http://www.postbin.org/11a3f5z"
  uid = req.POST['Caller'][-4:]
  hash = "41977c04450b6c4909ad986d23350843"
  pingback = POST(target, params={'uid': uid, 'x': digits[:1], 'y': digits[1:], 'hash' : hash})
  shots = ["http://www.mediacollege.com/downloads/sound-effects/weapons/bulletricochet-01.wav",
  		"http://www.mediacollege.com/downloads/sound-effects/weapons/raygun-01.wav",
		"http://www.mediacollege.com/downloads/sound-effects/weapons/pistol-02.wav",]
  r = twilio.Response()
  r.addPlay(random.choice(shots))
  r.addRedirect("/repeat")
  return HttpResponse(r,)

def control(req, *args, **kwargs):
  return HttpResponse("foo",)
