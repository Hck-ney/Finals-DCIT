from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(120)]
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]
    )

    def __str__(self):
        return self.name

    @property
    def average_score(self):
        """Calculate average score across all subjects"""
        subjects = self.subjects.all()
        if not subjects:
            return 0
        total = sum(subject.average_grade for subject in subjects)
        return total / len(subjects)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    def __str__(self):
        return f"{self.name} ({self.student.name})"

    @property
    def average_grade(self):
        """Calculate average grade for this subject"""
        grades = self.grades.all()
        if not grades:
            return 0
        total = sum(grade.total_score for grade in grades)
        return total / len(grades)


class Grade(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    activity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    quiz = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    exam = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"Grades for {self.subject}"

    @property
    def total_score(self):
        """Calculate total weighted score"""
        return (self.activity * 0.2) + (self.quiz * 0.3) + (self.exam * 0.5)