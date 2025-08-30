from rest_framework import serializers
from .models import *


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ['id', 'name','slug']



class AdSerializerGet(serializers.ModelSerializer):
    rubric=RubricSerializer(read_only=True)
    class Meta:
        model = Ad
        fields = ['id', 'rubric', 'title', 'price','image', 'content']

class AdSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ['id', 'rubric','slug','seller', 'title', 'price','image', 'content']