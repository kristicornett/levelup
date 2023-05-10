from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, GameType
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level UP API event view"""
    def create(self, request):
        """Handles POST requests for events
        
        Returns:
            Response: JSON serialized representation of newly created event"""
        
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=gamer,
            game=game
        )

        serialized = EventSerializer(event)
        return Response(serialized.data)
    
    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        
        if "game" in request.query_params:
            game_id = request.query_params["game"]
            events = events.filter(game_id=game_id)

            
        for event in events:
            gamer = Gamer.objects.get(user=request.auth.user)
            event.joined = gamer in event.attendee.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handles GET of single event"""
        event = Event.objects.get(pk=pk)
        serialized = EventSerializer(event)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Handles PUT for single event"""

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.time = request.data["time"]
        event.date = request.data["date"]
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handles DELETE events"""
        event = Event.objects.get(pk=pk)
        event.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendee.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """DELETE request for a user to leave an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendee.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
    


class GamerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gamer
        fields = ('bio', 'full_name')

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    organizer = GamerEventSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'description', 'date', 'time', 'attendee', 'organizer', 'game', 'joined')
        depth = 1
