#!/bin/bash
# LOG8415E - Final assignment
# Author: Jimmy Bell
# Sample requests

echo 'Please enter proxy public IP:'
read proxy_ip
curl 'http://'$proxy_ip':5000/default?query=SELECT%20*%20from%20actor%3B'
curl 'http://'$proxy_ip':5000/random?query=SELECT%20*%20from%20actor%3B'
curl 'http://'$proxy_ip':5000/ping?query=SELECT%20*%20from%20actor%3B'
curl "http://'$proxy_ip':5000/ping?query=INSERT%20INTO%20actor%20VALUES%20(2004,'a','a',CURDATE())%3B"
curl "http://'$proxy_ip':5000/ping?query=INSERT%20INTO%20actor%20VALUES%20(2005,'b','b',CURDATE())%3B"
curl 'http://'$proxy_ip':5000/random?query=SELECT%20*%20from%20actor%20WHERE%20actor_id=2005%3B'