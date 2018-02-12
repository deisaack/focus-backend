from .models import  Employee
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User=get_user_model()



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=False,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):

        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.save()
        Employee.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username',
                                               instance.username)
        instance.first_name = validated_data.get('first_name',
                                                instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                               instance.last_name)

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and password == confirm_password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate(self, data):
        '''
        Ensure the passwords are the same
        '''
        if 'password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError(
                    "The passwords have to be the same"
                )
        return data

    class Meta:
        model = User
        write_only_fields=('password', 'confirm_password')
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password', 'confirm_password')
        read_only_fields = ('id', )



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=False)

    class Meta:
        fields=('username', 'password')
        write_only_fields = ('password', )


class EmployeeSerializer(serializers.ModelSerializer):
    current_image = serializers.SerializerMethodField()
    user = UserSerializer(required=False)

    class Meta:
        model=Employee
        fields =  ('id', 'user', 'employee_no', 'date_hired', 'id_no', 'id_file',
                   'phone', 'current_image', 'gender', 'image', 'phone_verified')
        read_only_fields= ('id',)
    def get_current_image(self, obj):
        return obj.get_picture