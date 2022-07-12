#!/bin/bash

tmux kill-server

cd project-sankalp

git fetch
git reset origin/main --hard

python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux new -d -s site-session 'flask run --host=0.0.0.0'
tmux send-keys 'exec redeploy-site.sh' C-m
tmux detach -s site-session
