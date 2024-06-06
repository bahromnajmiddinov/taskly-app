from users.models import Profile

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True, required=False)
    
    def validate(self, data):
        request_method = self.context['request'].method
        password = data.get('password', None)
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError({'Info': 'Password is required'})
        elif request_method == 'PUT' or request_method == 'PATCH':
            old_password = data.get('old_password', None)
            if password != None and old_password == None:
                raise serializers.ValidationError({'Info': 'Old password is required'})
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        profile = Profile.objects.create(**validated_data)
        profile.set_password(password)
        profile.save()

        return profile
    
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception('Old password is invalid')
                user.save()
        except Exception as e:
            raise serializers.ValidationError({'Info': e})
        return super(ProfileSerializer, self).update(instance, validated_data)
    
    class Meta:
        model = Profile
        fields = ['url', 'id', 'image', 'username', 'email', 'first_name', 'last_name', 'password', 'old_password']
