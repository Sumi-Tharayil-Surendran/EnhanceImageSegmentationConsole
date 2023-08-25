from authapp.models import CustomUser
from rest_framework import serializers
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('about',
                  'first_name',
                  'middle_name',
                  'last_name',
                  'email','date_of_birth','passport','gender','nationality','marital_status')
