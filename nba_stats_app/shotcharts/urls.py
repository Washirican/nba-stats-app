from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='shot_charts-home'),

    path('player/<str:player_id>/',
         views.player_profile,
         name='player-profile'),

    path('player/<str:player_id>/<str:season_year>/',
         views.player_season_game_log,
         name='player-season-game-log'),

    path('player/<str:player_id>/<str:season_year>/<str:game_id>/shot_list/',
         views.player_game_shot_list,
         name='player-game-shot-list'),

    path('player/<str:player_id>/<str:season_year>/<str:game_id>/shot_chart/',
         views.player_game_shot_chart,
         name='player-game-shot-chart'),

    path('about/', views.about, name='shot-charts-about'),
]
