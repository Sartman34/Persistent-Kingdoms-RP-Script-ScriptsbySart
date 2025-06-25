#!/bin/bash
cd ..
source source/env/bin/activate
nohup python ./source/Server\ Owner\ Panel\ v1.3.3\ x64.pyw  >/dev/null 2>&1 &
sleep 3
