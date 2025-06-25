#!/bin/bash
cd ..
source source/env/bin/activate
gnome-terminal -- bash -c "python ./source/autosave.py"
