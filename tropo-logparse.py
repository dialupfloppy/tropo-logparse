#!/usr/bin/python

import requests
import ftplib
import re
import os
import datetime
import time
import pytz

ftpuser = 'username'
ftppass = 'password'

#launch tropo hosted script
tokendata = 'tokenstring'
payload = {'action': 'create', 'token': tokendata}

#error codes from http post
r = requests.post('https://api.tropo.com/1.0/sessions?', params=payload)
print(r.url)
print(r.json)
print(r.text)

#wait for end of call
time.sleep(55)

#check log file for great justice
#ftp connect and dir list
f = ftplib.FTP('ftp.tropo.com')
f.login(ftpuser, ftppass)

f.cwd('/logs/')
data = []
f.dir('-t',data.append)

#get filename from ftp dir output
#this will fail if logs have been archived to .gz
#launch application again
output = data[0]
print output
filename = output[-19:]
print filename

#write logfile
#with open('logfile.txt') as logf:
logf = open('logfile.txt', 'wb')
f.retrbinary('RETR ' + filename, logf.write, 1024)
f.quit()
logf.close()

#get current day and hour for regex
now = datetime.datetime.now(pytz.timezone('UTC'))
stamp = now.strftime("%d %H")
print stamp

#search log file for expression, match and compare time
#regex = re.compile(r'[a-zA-Z]+ *{}[a-zA-Z]+_state=ANSWERED'.format(stamp))
#success = re.compile(r'({}:)+.+(\sringingnow)'.format(stamp))
success = re.compile(r'({}:).+( calliscomplete)'.format(stamp))
fail = re.compile(r'({}:)+.+(\sError100)'.format(stamp))

#print regex1
#print regex2

with open('logfile.txt') as log:
	lines = log.readlines()
	lines.reverse()
	for line in lines:
		for m in re.findall(success, line):
			print line
			os.system("send.sh")
		if re.findall(fail, line):
			print line
			os.system("send.sh FAIL")

#logfile.close()
#re.search('_state=ANSWERED')
