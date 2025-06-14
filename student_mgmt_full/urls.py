from django.contrib import admin
from django.urls import path, include
from students.views import student_list, student_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('students.urls')),
    path('', include('students.urls')),
    path('student/<int:pk>/', student_detail),
]
