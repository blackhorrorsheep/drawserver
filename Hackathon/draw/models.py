from django.db import models
import datetime
import time


class DrawData(models.Model):
    usid = models.CharField(max_length=200)
    user = models.CharField(max_length=100)
    latStart = models.FloatField()
    longStart = models.FloatField()
    latEnd = models.FloatField()
    longEnd = models.FloatField()
    thickness = models.FloatField()
    color = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #unix = models.TimeField()

    def __str__(self):
        return "ID/{},USER/{},TIME/{}".format(self.usid, self.user, self.timestamp)


class Data(models.Model):
    usid = models.CharField(max_length=200)
    user = models.CharField(max_length=100)
    latstart = models.FloatField()
    lonstart = models.FloatField()
    latend = models.FloatField()
    lonend = models.FloatField()
    thickness = models.FloatField()
    color = models.FloatField()
    timestamp = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        timestamp_now = datetime.datetime.now()
        self.timestamp = time.mktime(timestamp_now.timetuple())
        super(Data, self).save(*args, **kwargs)

    def __str__(self):
        return "ID/{},USER/{},TIMESTAMP/{}".format(self.usid, self.user, self.timestamp)
