import os
import fnmatch
import csv
from datetime import datetime
import django

def populate():
    lev_root = Directory.objects.get_or_create(name='levels', oid = 0)[0]

    os.chdir("media")
    for root, dirnames, filenames in os.walk('levels'):
        order_dict = dict()
        oid = 0 # order id
        if '_order.X.txt' in filenames:
            order = open(os.path.join(root, '_order.X.txt'))
            for line in order:
                order_dict[line.strip()] = oid
                oid += 1
            order.close()
        par = Directory.objects.get(name=root) # TODO: add check for error (if [1] == FALSE)
        for dirname in dirnames:
            d_oid = oid
            if dirname in order_dict:
                d_oid = order_dict[dirname]
            else:
                oid += 1
            Directory.objects.get_or_create(name = os.path.join(root, dirname), parent = par, oid = d_oid)
        for filename in fnmatch.filter(filenames, '*.txt'):
            if filename == '_order.X.txt':
                continue
            f_oid = oid
            if filename in order_dict:
                f_oid = order_dict[filename]
            else:
                oid += 1
            title = str()
            lv = open(os.path.join(root, filename))
            for line in lv:
                if line[:8] == '$ENGLISH':
                    title = line[8:].strip()
                    break
            lv.close()
            Level.objects.get_or_create(name = os.path.join(root, filename), parent = par, title = title, oid = f_oid)
    os.chdir("..")

    now = datetime.utcnow()
    user = django.contrib.auth.models.User.objects.get(username = 'geoo')
    user2 = django.contrib.auth.models.User.objects.get(username = 'Nepster2')
    #try:
    with open('replay_list.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) == 8:
                #try:
                #    lv = Level.objects.get(name = row[2])
                    if row[0] == '(OK)' or row[0] == '(FAIL)':
                        if row[3] == 'geoo':
                            Replay.objects.get_or_create(status = row[0][1:-1], name = row[1], level_path = row[2], author = row[3], lems_saved = int(row[4]), lems_required = int(row[5]), skills = int(row[6]), time = int(row[7]), timestamp = now, owner = user)
                        else:
                            Replay.objects.get_or_create(status = row[0][1:-1], name = row[1], level_path = row[2], author = row[3], lems_saved = int(row[4]), lems_required = int(row[5]), skills = int(row[6]), time = int(row[7]), timestamp = now, owner = user2)
                #except lixdb.models.DoesNotExist:
                #    Replay.objects.get_or_create(status = 'NO-LEV', name = row[1], level_path = row[2], author = row[3], lems_saved = int(row[4]), lems_required = int(row[5]), skills = int(row[6]), time = int(row[7]), timestamp = now, owner = user)

    #except Exception as err: # I'm being very lazy here...
    #    print('File \'' + 'replay_list.csv' + '\' not found or something.')

    # Print out what we have added to the user.
    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print "- {0} - {1}".format(str(c), str(p))

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testprj.settings')
    from lixdb.models import Directory, Level, Replay
    populate()
    print "Done."
