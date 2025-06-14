from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    SubjectViewSet,
    GradeViewSet,
    student_list,
    student_detail,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView,
    GradeCreateView,
    GradeUpdateView,
    GradeDeleteView
)

router = DefaultRouter()
router.register(r'api/students', StudentViewSet)
router.register(r'api/subjects', SubjectViewSet)
router.register(r'api/grades', GradeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    # Student URLs
    path('', student_list, name='student-list'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('<int:pk>/', student_detail, name='student-detail'),
    path('<int:pk>/update/', StudentUpdateView.as_view(), name='student-update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),

    # Subject URLs
    path('<int:student_id>/subjects/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject-update'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject-delete'),

    # Grade URLs
    path('subjects/<int:subject_id>/grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/update/', GradeUpdateView.as_view(), name='grade-update'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade-delete'),
]