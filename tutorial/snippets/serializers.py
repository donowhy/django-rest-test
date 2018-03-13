from rest_framework import serializers
from models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions, routers, serializers, viewsets
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model # If used custom user model

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


UserModel = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('username', 'password')



#viewsets
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
