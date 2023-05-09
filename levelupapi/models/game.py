from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=155)
    maker = models.CharField(max_length=155)
    number_of_players = models.IntegerField(blank=True, null=True)
    skill_level = models.CharField(max_length=155)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE, related_name='games')
    gamer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='gamers')