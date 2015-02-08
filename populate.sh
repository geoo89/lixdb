#!/bin/bash

verify=
filename=  # unused for now

function usage
{
    echo "usage: populate.sh [[-v]] | [-h]]\n -v     Re-verify replays\n -h     Display this help message."
}

while [ "$1" != "" ]; do
    case $1 in
        -f | --file )           shift
                                filename=$1
                                ;;
        -v | --verify )         verify=1
                                ;;
        -h | --help )           usage
                                exit
    esac
    shift
done

rm -f lix.db
if [ "$verify" = "1" ]; then
    cd media
    ./lix --verify=replays > ../replay_list.csv
    cd ..
fi
python manage.py syncdb --noinput
python populate.py