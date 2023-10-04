from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name="gradeapp"),
    path('add-course', views.add_course, name="add-course"),
    path('get-grading-components', views.get_grading_components, name="get-grading-components"),
    path('get-courses', views.get_courses, name="get-couses"),
    path('course-home/<int:course_id>', views.course_home, name="course-home"),
    path('course-home/<int:course_id>/edit', views.edit_course, name="edit-course"),
    path('add-instance/<int:grading_component_id>', views.add_instance, name="add-instance"),
]