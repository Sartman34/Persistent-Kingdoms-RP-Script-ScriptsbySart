#!/bin/bash
gnome-terminal -- bash -c "
WINEDEBUG=fixme-all nohup wine mb_warband_wse2_dedicated.exe --config-path server_config.ini -r _pk_script.txt --module Persistent Kingdoms > /dev/null 2>&1 &
exec bash"
