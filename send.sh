#!/bin/bash

#./send.sh FAIL
# 		- sends fail email


#if [ -n "$1" -eq "FAIL" ]; then
#if [ "$?" -eq "99" ]; then

if [[ ${1+isset} = isset ]]; then
	echo "No One Picked Up"
	/usr/sbin/ssmtp test@example.com, test@email.com < /home/pi/failed.txt
	date | tr -d '\n' >> /home/pi/test.log
	echo "   -Fail" >> /home/pi/test.log
exit 0

else
	echo "Input detected on FrontDesk Phone"
	/usr/sbin/ssmtp test@example.com, test@email.com < /home/pi/worked.txt
	date | tr -d '\n' >> /home/pi/test.log  
	echo "   -Success" >> /home/pi/test.log

exit 1
fi
