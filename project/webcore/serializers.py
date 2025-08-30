from rest_framework import serializers
from rest_framework.response import Response

from .models import *

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ['id','name','slug']

class AdSerializerGet(serializers.ModelSerializer):
    rubric=RubricSerializer(read_only=True)
    class Meta:
        model = Ad
        fields = ['id','title','content','price','image','rubric',]

class AdSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['id','title','content','price','image','rubric','slug','seller']







