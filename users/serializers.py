from users.models import Profile

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True, required=False)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        profile = Profile.objects.create(**validated_data)
        profile.set_password(password)
        profile.save()

        return profile
    
    class Meta:
        model = Profile
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'password']
