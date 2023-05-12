from django.db import models
from django.db.models import Count

class Event(models.Model):
    description = models.CharField(max_length=155)
    date = models.DateField()
    time = models.TimeField()
    attendee = models.ManyToManyField("Gamer", related_name='events')
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='games')
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='events')

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value