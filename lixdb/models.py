from django.db import models

# official flag default = true

class Directory(models.Model):
    name = models.CharField(max_length=128) # this is the full path
    parent = models.ForeignKey('self', null=True) # the root folder has 0 -- or make it refer to itself?
    ordered = models.BooleanField(default = False)
    oid = models.IntegerField() # order id
    # is_root

    def __unicode__(self): # add recursion here to get full path
        return self.name

    # associate a _order.X.txt with a directory

class Level(models.Model): # inherit from Directory?
    name = models.CharField(max_length=128) # this is the full path
    parent = models.ForeignKey(Directory)
    title = models.CharField(max_length=128)
    oid = models.IntegerField() # order id
    #lems_required = models.IntegerField()
    #time = models.IntegerField(default=0)
    # also use FileField/FilePathField?

    def __unicode__(self):
        return self.name

class Replay(models.Model):
    name = models.CharField(max_length=128)
    status = models.CharField(max_length=32)
    level_path = models.CharField(max_length=256)
    level = models.ForeignKey(Level, null = True)
    author = models.CharField(max_length=128) # in the future this should be come a user id
    lems_saved = models.IntegerField(default=0)
    lems_required = models.IntegerField(default=0)
    skills = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name + " by " + self.author + " " + self.status + " " + self.level_path

