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
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from webusers.models import User
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import django.contrib.auth.password_validation as validators
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
    password = serializers.CharField(write_only=True, required=False)
    def to_internal_value(self, data):
        if data['password']:
            return data
        elif self.context['request'].method=='PUT':
            return data
        else:
            return super().validate(data)
       
    def validate(self, data):
       
        if data['password']:
            return data
        elif self.context['request'].method=='PUT':
            return data
        else:
            return super().validate(data)
       
       
        
  
    def create(self, validated_data):
        
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
       
        if  validated_data['password'] and validated_data['password'].strip():
            super(UserSerializer, self).update(instance, validated_data)
            instance.set_password(validated_data.get('password', instance.password))
            instance.save()
            return instance
        if not validated_data['password']:
            instance.name=validated_data.get('name', instance.name)
            instance.email=validated_data.get('email', instance.email)
            instance.identity=validated_data.get('identity', instance.identity)
            instance.country=validated_data.get('country', instance.country)
            instance.state=validated_data.get('state', instance.state)
            instance.city=validated_data.get('city', instance.city)
            instance.street=validated_data.get('street', instance.street)
            instance.number=validated_data.get('number', instance.number)
            instance.save()
            return instance
       
        
    class Meta:
        model = UserModel
        fields = ['id', 'name','identity' ,'email', 'country', 'password', 'state', 'city', 'street', 'number']

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
