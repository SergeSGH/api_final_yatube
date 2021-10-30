from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from django.shortcuts import get_object_or_404

from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.StringRelatedField()

    # def create(self, validated_data):
    #    print(validated_data, type(validated_data))
    #    following_username = validated_data['following']
    #    following = get_object_or_404(User, username=following_username)
    #    follow, status = Follow.objects.get_or_create(
    #       user=user, following=following
    #    )
    #    return follow

    # def validate(self, data):
    #    print(data)
    #    if self.user.username == data['following']:
    #        raise serializers.ValidationError('Подписаться на себя нельзя!')
    #    return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
