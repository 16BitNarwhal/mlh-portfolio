#!/bin/bash

tmux kill-server

for arg in "$@"; do
    if [ $arg="remote" ]; then
        git fetch
        git reset origin/main --hard
    fi
done

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

systemctl daemon-reload
systemctl restart myportfolio
