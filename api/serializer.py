from rest_framework import serializers
from .models import Room

'''Serializers allow complex data such as querysets and model
instances to be converted to native Python datatypes that can
then be easily rendered into JSON, XML or other content types.
Serializers also provide deserialization, allowing parsed data
to be converted back into complex types, after first validating
 the incoming data.'''


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id','code','host','guest_can_pause','votes_to_skip','created_at')
 

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause' , 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause' , 'votes_to_skip' , 'code')