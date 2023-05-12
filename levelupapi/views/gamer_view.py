from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Gamer 

class GamerView(ViewSet):
    """levelup API Gamer view"""

    def list(self, request):
        """Handles GET requests to get all gamers
        
        Returns:
            Response -- JSON serialized list of gamers"""
        
        gamers = Gamer.objects.all()
        serialized = GamerSerializer(gamers, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handles GET requests for single gamer
        
        Returns:
            Response -- JSON serialized gamer record
        """
        try:
            gamer = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(gamer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Gamer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
       


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""

    class Meta: 
        model = Gamer
        fields = ('id', 'bio', 'full_name')