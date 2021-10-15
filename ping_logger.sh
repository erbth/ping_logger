#!/bin/bash -e

DELAY=60

if [ -z "$1" ] || [ -z "$2" ]
then
	echo "Usage: $0 <address> <logfile> [<delay/seconds (default: 60)>]"
	exit 1
fi

ADDR="$1"
LOGFILE="$2"

if [ -n "$3" ]
then
	DELAY="$3"
fi

while true
do
	echo -n "Attempting to ping $ADDR ... "
	time="$(date +"%Y-%m-%d %H:%M:%S")"

	responsetime="$(ping -c 1 "$ADDR"|head -n2|tail -n1|cut -d'=' -f4|cut -d' ' -f1)"
	if [ -n "$responsetime" ]
	then
		echo -e "[  \033[32mok\033[0m  ]"
		echo "$time $ADDR ok $responsetime" >> "$LOGFILE"
	else
		echo -e "[\033[31mfailed\033[0m]"
		echo "$time $ADDR failed" >> "$LOGFILE"
	fi

	sleep $DELAY
done
