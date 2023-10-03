from django.contrib import admin
from .models import Course, Assignment, Category, GradingComponent, CourseGradingComponent

# Register your models here.

# admin.site.register(Category) # maybe delete
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(GradingComponent)
admin.site.register(CourseGradingComponent)