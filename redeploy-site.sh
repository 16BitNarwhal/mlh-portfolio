#!/bin/bash

tmux kill-server

systemctl start mysqld

for arg in "$@"; do
    if [ $arg="$@" ]; then
        git fetch
        git reset origin/main --hard
    fi
done

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

tmux new-session -d -s flask_server "flask run --host=0.0.0.0"
