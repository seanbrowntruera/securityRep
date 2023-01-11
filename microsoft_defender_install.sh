#!/bin/bash

# Micorsoft Defender install
curl -w ' %{url_effective}\n' 'https://x.cp.wd.microsoft.com/api/report' 'https://cdn.x.cp.wd.microsoft.com/ping'

echo "Test microsoft defender conectivity"
mdatp connectivity test