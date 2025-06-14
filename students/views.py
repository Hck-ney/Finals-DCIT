from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Subject, Grade
from .serializers import StudentSerializer, SubjectSerializer, GradeSerializer
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer

    def get_queryset(self):
        """Allow filtering by name and age"""
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        age = self.request.query_params.get('age')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if age:
            queryset = queryset.filter(age=age)

        return queryset

    @action(detail=True, methods=['get'])
    def subjects(self, request, pk=None):
        """Get all subjects for a specific student"""
        student = self.get_object()
        subjects = student.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer

    def get_queryset(self):
        """Filter subjects by student"""
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset

    @action(detail=True, methods=['get'])
    def grades(self, request, pk=None):
        """Get all grades for a specific subject"""
        subject = self.get_object()
        grades = subject.grades.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def get_queryset(self):
        """Filter grades by subject"""
        queryset = super().get_queryset()
        subject_id = self.request.query_params.get('subject_id')
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset


def student_list(request):
    """Display list of all students"""
    students = Student.objects.all().order_by('name')
    return render(request, 'students/index.html', {'students': students})


def student_detail(request, pk):
    """Display details for a single student"""
    student = get_object_or_404(Student.objects.prefetch_related('subjects__grades'), pk=pk)
    return render(request, 'students/detail.html', {'student': student})

class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'age', 'email']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'age', 'email']
    template_name = 'students/student_form.html'

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True  # Add context for template to know it's an update
        return context

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')

class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name']
    template_name = 'students/subject_form.html'

    def form_valid(self, form):
        form.instance.student = Student.objects.get(pk=self.kwargs['student_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.kwargs['student_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        return context

class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name']
    template_name = 'students/subject_form.html'

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.student.id})

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'students/subject_confirm_delete.html'

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.student.id})

class GradeCreateView(CreateView):
    model = Grade
    fields = ['activity', 'quiz', 'exam']
    template_name = 'students/grade_form.html'

    def get_initial(self):
        initial = super().get_initial()
        self.subject = Subject.objects.get(pk=self.kwargs['subject_id'])
        return initial

    def form_valid(self, form):
        form.instance.subject = Subject.objects.get(pk=self.kwargs['subject_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.subject.student.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = Subject.objects.get(pk=self.kwargs['subject_id'])
        return context

class GradeUpdateView(UpdateView):
    model = Grade
    fields = ['activity', 'quiz', 'exam']
    template_name = 'students/grade_form.html'

    def get_success_url(self):
        # Get the student ID through the grade -> subject -> student relationship
        return reverse('student-detail', kwargs={'pk': self.object.subject.student.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add subject to context for the template
        context['subject'] = self.object.subject
        return context

class GradeDeleteView(DeleteView):
    model = Grade
    template_name = 'students/grade_confirm_delete.html'

    def get_success_url(self):
        return reverse('student-detail', kwargs={'pk': self.object.subject.student.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.object.subject
        return context