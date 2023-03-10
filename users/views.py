from django.utils import timezone
from .models import User
from address.models import Address
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework import generics, status
from .permissions import IsAccountOwner
from rest_framework_simplejwt.views import TokenObtainPairView
from address.serializers import AddressSerializer
from rest_framework import serializers


class UserView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        if "address" in self.request.data:
            address_request = self.request.data.pop("address")
            addressSerializer = AddressSerializer(data=address_request)

            addressSerializer.is_valid(raise_exception=True)
            address = Address.objects.create(**addressSerializer.data)

            return serializer.save(address=address)
        else:
            raise serializers.ValidationError(
                {"address": ["This field is required."]})


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "user_uuid"

    def perform_update(self, serializer):
        if "address" in self.request.data:
            user_address = Address.objects.get(pk=self.request.user.address.id)
            address_request = self.request.data.pop("address")
            addressSerializer = AddressSerializer(
                user_address, data=address_request, partial=True)

            addressSerializer.is_valid(raise_exception=True)
            addressSerializer.save()
        return serializer.save()


class PersonalizedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data.get("username"))
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return response
