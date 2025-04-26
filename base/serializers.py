
from rest_framework import serializers
from .models import HealthProgram, Client, Enrollment

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class HealthProgramSerializer(serializers.ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True  
    )
    doctor_details = UserSerializer(source='doctor', read_only=True)  

    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'date_created', 'doctor', 'doctor_details']
        read_only_fields = ['id', 'date_created', 'doctor_details']

    def validate_name(self, value):
       
        if HealthProgram.objects.filter(name=value).exists():
            raise serializers.ValidationError("A program with this name already exists.")
        return value

    def validate_doctor(self, value):
       
        if not value.groups.filter(name='Doctor').exists():
            raise serializers.ValidationError("The selected user must be a doctor.")
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer(read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthProgram.objects.all(), source='program', write_only=True
    )

    # client = HealthProgramSerializer(read_only=True)
    # client_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), source='client', write_only=True
    # )



    class Meta:
        model = Enrollment
        fields = ['id','client_id','client', 'program', 'program_id', 'enrolled_date']

class ClientSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'email', 'created_at', 'enrollments']




class DoctorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        user.groups.add(doctor_group)
        return user
