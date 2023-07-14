from django.db import models
import string , random

#function to generate unique code for Room.code
def generate():
    length = 6
    while True:
        # nice method to  generate random strings
        # '#'.join given a list of elements joins the by '#' character, here '' means join them by blank
        Code = ''.join(random.choices(string.ascii_uppercase, k=length))

        # if list of Room filtered by code that has code = Code has len > 0 implies code is already used
        if Room.objects.filter(code = Code).count() == 0:
            break
    
    return Code



# Create your models here.
# Rule of thumb - django Fat models thin views
class Room(models.Model):
    # Room has a Code which is unique identifer for that room
    #by default that field is blank - no default val
    code = models.CharField(max_length=8, default=generate, unique=True)

    # host hosting the room
    # one host only has one room
    # single host cannot host multiple rooms
    host = models.CharField(max_length=50 , unique=True)

    # permissions
    guest_can_pause = models.BooleanField(null = False , default=False)

    #votes to skips the track
    votes_to_skip = models.IntegerField(null=False , default=1)

    #created at - time of creation of Room
    #DateField.auto_now - Automatically set the field to now every time the object is saved. Useful for “last-modified” timestamps
    #DateField.auto_now_add =Automatically set the field to now when the object is first created.
    created_at = models.DateTimeField(auto_now_add=True)



