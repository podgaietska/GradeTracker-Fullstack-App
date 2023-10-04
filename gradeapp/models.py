from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=8)
    lecture = models.CharField(max_length=3, null=True, blank=True)
    lab = models.CharField(max_length=3, null=True, blank=True)
    seminar = models.CharField(max_length=3, null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    grading_component = models.ManyToManyField(to='GradingComponent', through='CourseGradingComponent')
    
    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ['code']

class GradingComponent(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class CourseGradingComponent(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    grading_component = models.ForeignKey(to=GradingComponent, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ['course', 'grading_component']
        
    def __str__(self):
        return self.course.code+' - '+self.grading_component.name

class Event(models.Model):
    PROGRESS_TYPES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
        ('Cancelled', 'Cancelled'),
        ('Urgent!', 'Urgent!'),
    )
    
    name = models.CharField(max_length=255)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grading_component = models.ForeignKey(to=GradingComponent, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, choices=PROGRESS_TYPES, default='Not Started')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
    
    @property  
    def weight(self):
        course_component = CourseGradingComponent.objects.get(course=self.course, grading_component=self.grading_component)
        total_events_in_grading_component = Event.objects.filter(course=self.course, grading_component=self.grading_component).count()
        return course_component.weight / total_events_in_grading_component if total_events_in_grading_component > 0 else 0
        
# class Progress(models.Model):
#     description = models.CharField(max_length=100)
    
#     class Meta:
#         verbose_name_plural = 'Categories'  # plural form of category
     
#     def __str__(self):
#         return self.name
        
