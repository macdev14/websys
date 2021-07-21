"""websys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from webusers.models import User
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

UserModel = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # Add extra responses here
        data['name'] = self.user.name
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        print(validated_data)
        user = UserModel.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
            identity=validated_data['identity'],
            country=validated_data['country'],
            state=validated_data['state'],
            city=validated_data['city'],
            street=validated_data['street'], 
            number=validated_data['number']
        )
      
        return user
    def update(self, instance, validated_data):
        super(UserSerializer, self).update(instance, validated_data)
        user = User.objects.get(pk=self.context['request'].user.id)
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = UserModel
        fields = ['id', 'name','identity' ,'email', 'password', 'country', 'state', 'city', 'street', 'number']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super(UserViewSet, self).get_permissions()
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


class obtainToken(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webusers.urls')),
    path('api/', include(router.urls)),
    path('api/token/', obtainToken.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
