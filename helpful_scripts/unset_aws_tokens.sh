#!/bin/bash

# In case aws doesn't refresh my tokens
export | grep AWS
unset AWS_ACCESS_KEY_ID && unset AWS_SECRET_ACCESS_KEY && unset AWS_SESSION_TOKEN
echo "[+] Unsetting complete!"
aws configure
code ~/.aws/credentials