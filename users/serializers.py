from rest_framework import serializers
from .models import User, Student, Teacher




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'profile_image', 'full_name', 'email', 'grade']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'profile_image', 'full_name', 'email', 'expertise', 'rating']

class UniqueTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['expertise', 'rating']

class UniqueStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['grade']

class UserSerializer(serializers.ModelSerializer):
    student = UniqueStudentSerializer(many=False, read_only=True)
    teacher = UniqueTeacherSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'profile_image', 'full_name', 'email', 'is_teacher', 'student', 'teacher')

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField( max_length=128, min_length=8, write_only=True)
 
    class Meta:
        model = Student
        fields = ('id', 'profile_image', 'full_name', 'email', 'password', 'grade')
 
    def create(self, validated_data):
        return Student.objects.create_student(**validated_data)


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
 
    class Meta:
        model = Teacher
        fields = ('id', 'profile_image', 'full_name', 'email', 'password', 'expertise')
 
    def create(self, validated_data):
        return Teacher.objects.create_teacher(**validated_data)

       
class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
