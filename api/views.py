from django.shortcuts import render
from rest_framework import generics,status
from .serializer import RoomSerializer,CreateRoomSerializer,UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

# CreateAPIView - lets u create an instance of your class model using inbuilt view
# ListAPIView - Used for read-only endpoints to represent a collection of model instances.
    # displays a list of model instances

class RoomView(generics.ListAPIView):
    '''queryset - The queryset that should be used
     for returning objects from this view. Typically,
     you must either set this attribute'''
    queryset = Room.objects.all()

    '''serializer_class - The serializer class that should 
    be used for validating and deserializing input, and
       for serializing output.'''
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    roomCode = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.roomCode)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data , status=status.HTTP_200_OK)
            return Response("Room Not Found : Invalid Request" , status=status.HTTP_404_NOT_FOUND)
        return Response('Bad Request : Code Parameter Missing' , status=status.HTTP_400_BAD_REQUEST)
    
class JoinRoom(APIView):
    roomCode = 'code'
    
    def post(self , request , format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        # for get request we use .GET for post request we use .data
        code = request.data.get(self.roomCode)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = room[0]
                self.request.session['room_code'] = code
                return Response({"Message" : "Room Joined!"}, status=status.HTTP_200_OK)
            return Response({"Room Not Found" : "Invalid Room Code"} , status=status.HTTP_404_NOT_FOUND)
        print("Code Not Found")
        return Response({'Bad Request' : 'Code Parameter Missing'} , status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self,request,format=None):
        # If there already exist a session corresponding to a user, if not create
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        #take the json data came with the request and convert it to python format
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            #get the fields u want to update
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key

            #check if the host already already exist
            Prev_Room = Room.objects.filter(host=host)

            
            if Prev_Room.exists():  # if exist
                room = Prev_Room[0]
                #update the fields
                room.votes_to_skip = votes_to_skip
                room.guest_can_pause = guest_can_pause
                room.save(update_fields=['votes_to_skip' , 'guest_can_pause'])

                #updating user in room -> room_code
                self.request.session['room_code'] = room.code
                #return an OK response
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else :
                #else create a room with following fields
                room = Room(host=host , guest_can_pause=guest_can_pause , votes_to_skip = votes_to_skip)
                room.save()

                #updating user in room -> room_code
                self.request.session['room_code'] = room.code
                #return a 201 created response
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

        #if data not valid return 400 bad request response
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):
    def get(self , request , format=None):
        if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
        code=self.request.session.get("room_code" , None)
        data={
            'code' : code,
        }

        return JsonResponse(data , status=status.HTTP_200_OK)
    

class LeaveRoom(APIView):
    def post(self , request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            queryset = Room.objects.filter(host = host_id)
            if len(queryset) > 0:
                room = queryset[0]
                room.delete()

        return Response("Message : success" , status=status.HTTP_200_OK)
    

class UpadateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request , format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"Bad Request" :"Invalid Data"} , status=status.HTTP_400_BAD_REQUEST)
        
        guest_can_pause = serializer.data.get('guest_can_pause')
        votes_to_skip = serializer.data.get('votes_to_skip')
        code = serializer.data.get('code')
        queryset = Room.objects.filter(code = code)
        if not queryset.exists():
            return Response({"Room Not Found" : "Invalid Room Code"} , status=status.HTTP_404_NOT_FOUND)
        
        room = queryset[0]
        user_id = self.request.session.session_key
        if user_id != room.host:
            return Response({"Invalid request" : "Host_id mismatch"} , status=status.HTTP_403_FORBIDDEN)
        
        room.guest_can_pause = guest_can_pause
        room.votes_to_skip = votes_to_skip
        room.save(update_fields=['guest_can_pause','votes_to_skip'])

        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        
