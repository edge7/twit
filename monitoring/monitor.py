import datetime
import re
import time

from dateutil import parser
import http.client, urllib


def pushover(msg, cross):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "user": "ux7w4sef54hcfe7ufqw6u92k5mmfs6",
                     "message": msg,
                     'title': cross,
                     'token': "apq8s9bb2eq9ps58ktvhfihaxj2kzg",
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    return response.status

while True:
    n = datetime.datetime.now()
    with open("C:\\Users\\Administrator\\Desktop\\projects\\twit\\access.txt", 'r') as fo:
        while True:
            line = fo.readline()
            d = line.split(",")[0]
            try:
                da = parser.parse(d)
                if ( n-da).total_seconds() < 60*5:
                    if 'GET /superset/dashboard/' in line:
                        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
                        if ip and ip[0] not in ['89.36.64.155', '66.249.93.65']:
                            print("New access: " + ip[0])
                            msg = "New Access: " + str(ip[0])
                            pushover(msg, 'superset')
            except Exception as e:
                pass
            if line == '':
                break
    time.sleep(60*3)
