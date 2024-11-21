from accounts.models import User
from teacher.models import Class, Subject, Attendance, Grade
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken  # Place this import here
User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'guardian_first_name', 'guardian_last_name', 'guardian_phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='student',  # Ensure the role is set to commuter

            guardian_first_name=validated_data['guardian_first_name'],
            guardian_last_name=validated_data['guardian_last_name'],
            guardian_phone_number=validated_data.get(
                'guardian_phone_number', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user and user.role == 'student':  # Ensure only commuters can log in
            return user
        raise serializers.ValidationError(
            "Invalid credentials or user not allowed.")


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'email', 'guardian_first_name', 'guardian_last_name', 'guardian_phone_number', 'date_joined']


# students/serializers.py


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role']


class ClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher_name']


class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source='teacher.get_full_name', read_only=True)
    class_name = serializers.CharField(
        source='class_assigned.name', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher_name', 'class_name']


class AttendanceSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(
        source='class_assigned.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'class_name', 'date', 'is_present']


class GradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_teacher = serializers.CharField(
        source='subject.teacher.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'subject_name', 'subject_teacher',
                  'mid_term_score', 'final_exam_score', 'total_score']
