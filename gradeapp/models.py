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

class Assignment(models.Model):
    name = models.TextField()
    weight = models.IntegerField()
    score = models.IntegerField()
    due_date = models.DateField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-due_date']
        
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Categories'  # plural form of category
     
    def __str__(self):
        return self.name
        
