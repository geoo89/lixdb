import os
import fnmatch
import csv

def populate():
    lev_root = Directory.objects.get_or_create(name='levels')[0]

    os.chdir("media")
    for root, dirnames, filenames in os.walk('levels'):
        par = Directory.objects.get_or_create(name=root)[0]
        for dirname in dirnames:
            Directory.objects.get_or_create(name = os.path.join(root, dirname), parent = par)
        for filename in fnmatch.filter(filenames, '*.txt'):
            Level.objects.get_or_create(name = os.path.join(root, filename), parent = par)
    os.chdir("..")

    #try:
    with open('replay_list.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if len(row) == 8:
                if row[0] == '(OK)' or row[0] == '(FAIL)':
                    Replay.objects.get_or_create(status = row[0], name = row[1], level_path = row[2], author = row[3], lems_saved = int(row[4]), lems_required = int(row[5]), skills = int(row[6]), time = int(row[7]))
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
