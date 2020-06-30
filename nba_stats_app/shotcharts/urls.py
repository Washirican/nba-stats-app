from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='shotcharts-home'),

    path('player/<str:player_id>/',
         views.player_profile,
         name='player-profile'),

    path('player/<str:player_id>/<str:season_year>/',
         views.player_season_gamelog,
         name='player-season-gamelog'),

    path('player/<str:player_id>/<str:season_year>/<str:game_id>/',
         views.player_game_shot_list,
         name='player-game-shot-list'),

    path('player/<str:player_id>/<str:season_year>/<str:game_id>/shot_chart/',
         views.player_game_shot_chart,
         name='player-game-shot-chart'),

    path('about/', views.about, name='shotcharts-about'),
]
