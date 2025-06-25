#!/bin/bash
cd ..
source source/env/bin/activate
gnome-terminal -- bash -c "python ./source/ana\ script.py"
gnome-terminal -- bash -c "python ./source/autosave.py"
gnome-terminal -- bash -c "python ./source/açlık\ scripti.py"
