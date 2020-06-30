from django.db import models


class Player(models.Model):
    """Player class."""
    player_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rookie_season = models.CharField(max_length=100)
    last_season = models.CharField(max_length=100)
