from django.contrib import admin
from .models import Course, GradingComponent, CourseGradingComponent, Event

# Register your models here.

# admin.site.register(Category) # maybe delete
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(GradingComponent)
admin.site.register(CourseGradingComponent)