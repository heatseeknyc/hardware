PI_ID=$(grep '^Serial\s*: ' /proc/cpuinfo | awk '{print $3}')

PORT=""
while true
do NEWPORT=$(grep '^Allocated port ' /var/log/supervisor/ssh-stderr* | tail -1 | awk '{print $3}')
    if [ "$NEWPORT" != "$PORT" ]
	then if curl -d "hub=$PI_ID" -d "port=$NEWPORT" http://hubs.heatseeknyc.com/hubs
	    then PORT="$NEWPORT"
	fi
    fi
    sleep 60
done
