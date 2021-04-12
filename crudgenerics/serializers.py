#from django.contrib.auth.models import User
from crudgenerics.models import Speaker
from rest_framework import serializers



class SpeakerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Speaker
        fields = '__all__'



