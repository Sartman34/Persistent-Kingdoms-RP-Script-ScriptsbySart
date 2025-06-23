#!/bin/bash
WINEDEBUG=fixme-all nohup wine mb_warband_wse2_dedicated.exe --config-path server_config.ini -r _pk_script.txt --module Persistent Kingdoms &