"""View module for handling requests for game data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType

class GameView(ViewSet):
    """LevelUp game view"""
    def list(self, request):
        """Handles GET requests for games"""

        games = Game.objects.all()
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handles GET request for single game"""

        game = Game.objects.get(pk=pk)
        serialized = GameSerializer(game)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handles POST request"""
        gamer = Gamer.objects.get(user=request.auth.user)
        game_type = GameType.objects.get(pk=request.data["game_type"])

        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            game_type=game_type,
            gamer=gamer
            
        )
        serialized = GameSerializer(game)
        return Response(serialized.data)
    
    def update(self, request, pk):
        """Handles PUT requests for a game"""

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]

        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
    
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type', 'gamer')