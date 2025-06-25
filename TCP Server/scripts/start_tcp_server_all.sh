#!/bin/bash
cd ..
source source/env/bin/activate
gnome-terminal -- bash -c "python ./source/ana\ script.py"
gnome-terminal -- bash -c "python ./source/autosave.py"
gnome-terminal -- bash -c "python ./source/açlık\ scripti.py"
nohup python ./source/Server\ Owner\ Panel\ v1.3.3\ x64.pyw  >/dev/null 2>&1 &
sleep 3
