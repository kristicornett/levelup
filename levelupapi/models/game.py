from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.IntegerField(blank=True, null=True)
    skill_level = models.CharField(max_length=155)
    game_type_id = models.ForeignKey('Game_Type', on_delete=models.CASCADE)