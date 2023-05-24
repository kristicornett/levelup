"""View module for handling requests for game data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ValidationError

class GameView(ViewSet):
    """LevelUp game view"""
    def list(self, request):
        """Handles GET requests for games"""

        games = Game.objects.annotate(event_count=Count('events'))
        gamer = Gamer.objects.get(user=request.auth.user)
        games = Game.objects.annotate(event_count=Count('events'), user_event_count=Count('events', filter=Q(events__organizer=gamer)))

# Add in the next 3 lines
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    
    def retrieve(self, request, pk=None):
        """Handles GET request for single game"""
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)



    def create(self, request):
        """Handles POST"""

    
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(gamer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

     

        
    
   #def create(self, request):
        """Handles POST request"""
    #    gamer = Gamer.objects.get(user=request.auth.user)
    #    game_type = GameType.objects.get(pk=request.data["game_type"])

    #    game = Game.objects.create(
    #        title=request.data["title"],
    #        maker=request.data["maker"],
     #       number_of_players=request.data["number_of_players"],
     #       skill_level=request.data["skill_level"],
      #      game_type=game_type,
      #      gamer=gamer
            
     #   )
     #   serialized = GameSerializer(game)
    #    return Response(serialized.data)
    
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
        
    
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type']
   
    
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    event_count = serializers.IntegerField(default=None)

    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'game_type', 'gamer', 'event_count')
        depth = 1