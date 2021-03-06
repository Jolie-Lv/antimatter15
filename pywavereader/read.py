"""
This prototype application is available under the terms of GPLv3
Permission for other licences can and probably will be granted
if emailed at antimatter15@gmail.com.
"""
import httplib
import pickle
import urllib
import json
from optparse import OptionParser

waveid = "googlewave.com!w+Mu9eK7j2H"

parser = OptionParser(usage="usage: %prog [options] waveid")
parser.add_option("-r", "--raw",action="store_true", dest="raw",help="include raw JSON")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose",help="verbose")

(options, args) = parser.parse_args()

if len(args) != 1:
  parser.error("incorrect number of arguments")
  exit()
elif args[0] == "default":
  pass #yay do nothin
else:
  waveid = urllib.unquote(urllib.unquote(args[0]))
  
if "+" not in waveid:
  waveid = "w+"+waveid
if "!" not in waveid:
  waveid = "googlewave.com!"+waveid

conn = httplib.HTTPSConnection("wave.google.com") 

state = pickle.load(open("state.txt","r"))
session = state['session']
cookie = state['cookie']


url = "/wave/wfe/fetch/"+waveid+"/"+str(session)+"?v=3"

conn.request("GET", url, "", {"Cookie": "WAVE="+cookie})
r2 = conn.getresponse()
print r2.status, r2.reason, r2.version
wavejson = r2.read()[5:]

if options.raw:
  print wavejson
  exit()

wave = json.loads(wavejson)

bliplist = wave['1'][0]['1']['2']

#print bliplist

for b in bliplist:
  if b['1'] == "conversation" or 'attach+' in b['1'] or 'spell+' in b['1']:
    continue
  print "--------------------------------------------"
  print "| blip",b['1'],",".join(b['7'])
  print "--------------------------------------------"
  if '16' in b:
    data = b['16']['2']
    out = ""
    for point in data: #...makes a beautiful line
      if '2' in point:
        out += point['2']
      elif '4' in point:
        out += "\n"
    try:
      print out.strip()
    except UnicodeEncodeError:
      print "Error Encoding Blip includes Non ASCII Character"
