#!/bin/bash
ipadr=`ip -4 addr show eth0 | grep inet | awk '{print $2}' | awk -F "/" '{print $1}'`
curl -X PUT "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records/RECORD_ID" \
     -H "X-Auth-Email: EMAIL" \
     -H "X-Auth-Key: API_KEY" \
     -H "Content-Type: application/json" \
     --data '{"type":"A","name":"SUB.EXAMPLE.COM","content":"'${ipadr}'","ttl":1,"proxied":false}'
echo ""
