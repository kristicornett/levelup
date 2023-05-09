"""View module for handling requests for GameType data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """LevelUP API GameType View"""

    def list(self, request):
        """Handles GET requests for Game Types"""

        game_types = GameType.objects.all()
        serialized = GameTypeSerializer(game_types, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handles GET for single gameType"""
        game_type = GameType.objects.get(pk=pk)
        serialized = GameTypeSerializer(game_type)
        return Response(serialized.data, status=status.HTTP_200_OK)


class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game type"""
    class Meta:
        model = GameType
        fields = ('id', 'label')