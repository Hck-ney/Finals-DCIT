from rest_framework import serializers
from .models import Student, Subject, Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate(self, data):
        """Validate grade values"""
        for field in ['activity', 'quiz', 'exam']:
            if data[field] < 0 or data[field] > 100:
                raise serializers.ValidationError(
                    f"{field} must be between 0 and 100"
                )
        return data


class SubjectSerializer(serializers.ModelSerializer):
    grades = GradeSerializer(many=True, read_only=True)
    average_grade = serializers.FloatField(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'student', 'grades', 'average_grade']


class StudentSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    average_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'email', 'subjects', 'average_score']

    def validate_email(self, value):
        """Ensure email is unique"""
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value