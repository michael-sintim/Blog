from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,min_length=8,style={"input_type":"password"})
    password2 = serializers.CharField(write_only=True,required=True,min_length=8,style={"input_type":"password"})

    class Meta:
        model = User
        fields = ['id','username','fullname','email','password','password2']
        read_only_fields = ['id']
        extra_kwargs = {
            "email":{"required":True},
            "username":{"required":False},
            "fullname":{"required":True},
        }

        
    def validate(self, attrs):
        if self.instance is None and 'password' in attrs:
            if 'password2' not in attrs:
                raise serializers.ValidationError({"password2":"this field is required"})
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password2":"these passwords do not match"})


        if 'password' in attrs:
            try:
                validate_password(attrs['password'])
            except DjangoValidationError as e:
                raise serializers.ValidationError({"password":list(e.messages)})
            
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({"email":"this email already exists"})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2",None)
        password = validated_data.pop("password",None)

        base_name = validated_data['email'].split("@")[0]
        username = base_name
        counter = 1

        if username not in validated_data or not validated_data:
            while  User.objects.filter(username=username).exists():
                username = f"{base_name}{counter}"
                counter += 1

            validated_data["username"]= username

        user = User(**validated_data)

        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password2',None)
        password = validated_data.pop('password',None)

        for attr,value in validated_data.items():
            setattr(instance,attr,value)

        if password:
            instance.set_password(password)
        instance.save()

        return instance

class LoginSerialize(serializers.ModelSerializer):
    email =serializers.EmailField()
    password = serializers.CharField(write_only=True,required=True,min_length=8,style={"input_type":"password"})
  

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
       
        read_only_field = ['id']
