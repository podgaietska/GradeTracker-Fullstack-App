from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name="gradeapp"),
    path('add-course', views.add_course, name="add-course"),
    path('get-grading-components', views.get_grading_components, name="get-grading-components"),
    path('get-courses', views.get_courses, name="get-couses"),
]