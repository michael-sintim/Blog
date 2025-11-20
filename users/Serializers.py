from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,min_length=8,style ={"input_type":"password"})
    password2 = serializers.CharField(write_only=True,required=True,min_length=8,style = {"input_type":"password"})

    class Meta:
        model = User
        fields = ['id','password','password2',
                  'email','first_name','last_name',
                  'username', 
                  'is_superuser','created_at','updated_at'
                  ]
        read_only_fields = ['id','created_at','updated_at','is_active','is_staff','is_superuser']
        extra_kwargs = {
            'email':{'required':True},
            'first_name':{'required':True},
            'last_name':{'required':True},
            'username': {'required':False},

        }


    def validate(self, attrs):
        if self.instance is None and 'password' in attrs:
            if 'password2' not in attrs:
                raise serializers.ValidationError({'password2':'this field is required'})
            
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password2":"these passwords do not match"})
            
        if 'password' in attrs:
            try:
                validate_password(attrs['password'])
            except DjangoValidationError as e :
                raise serializers.ValidationError({"password":list(e.messages)})
            
        email = attrs.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError({"email":"this email already exists"})
        
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2',None)
        password = validated_data.pop('password',None)

        if validated_data.get('username'):
            base_name = validated_data['email'].split("@")[0]
            username = base_name
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_name}{counter}"
                counter += 1
                
            validated_data['username']= username

        user = User(**validated_data)
        
    
        if password:
            user.set_password(password)
        user.save()
        return user
            
    

    def update(self, instance, validated_data):
        validated_data.pop('password2',None)
        password = validated_data.pop('password',None)

        for attr, value in validated_data.items():
            setattr(instance,attr,value)

        if password:
            instance.set_password(password)
        instance.save()

        return instance
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True,required=True,min_length=8 ,style=({'input_type':'password'}))

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = ['id',
                  'email','first_name','last_name',
                  
                  'created_at','updated_at'
                  ]
        read_only_fields = ['id','created_at','updated_at','is_active','is_staff',]
        
