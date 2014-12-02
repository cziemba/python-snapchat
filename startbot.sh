#!/bin/bash
until /home/cziemba/devel/python-snapchat/snapchat-bot.py; do
    echo "'snapchat-bot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
