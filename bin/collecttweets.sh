#!/bin/bash
source $WATCHING_HOME/venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/yoshio/watching
python $WATCHING_HOME/bin/collecttweets.py