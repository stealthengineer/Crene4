from .models import (Branch,
                     Leaf,
                     Politician,
                     Rating,
                     Topic)
from rest_framework import serializers



class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    topicname = serializers.SerializerMethodField()
    fav_count = serializers.IntegerField()
    unfav_count = serializers.IntegerField()
    count_diff = serializers.IntegerField()
    user_vote = serializers.BooleanField()
    leaf_count = serializers.IntegerField(source='branchonleaf.count',read_only = True)


    def get_username(self,obj):
        return obj.user.username
    def get_topicname(self,obj):
        return obj.topic.title

    class Meta:
        model = Branch
        fields = '__all__'


class LeafSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    subleaf_count = serializers.IntegerField(source='sub_leaf.count',read_only=True)
    count_diff = serializers.IntegerField()
    user_vote = serializers.BooleanField()

    def get_username(self,obj):
        return obj.user.username
    class Meta:
        model = Leaf
        fields = '__all__'


class PoliticianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politician
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

