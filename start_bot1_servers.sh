source ./venv/bin/activate
cd bot1
# only needed on pi
# on other linux or max start wirh "rasa ..."
python3 call_rasa.py run &
python3 call_rasa.py run actions &
