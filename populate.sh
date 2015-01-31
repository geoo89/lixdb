#!/bin/bash

rm -f lix.db
cd media
./lix --verify=replays > ../replay_list.csv
cd ..
python manage.py syncdb --noinput
python populate.py