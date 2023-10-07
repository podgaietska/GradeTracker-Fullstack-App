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
    
    def total_grade_gained(self):
        total = 0
        for event in self.event_set.all():  
            if event.student_grade is not None and event.max_grade is not None:
                total += event.grade
        return total*100
    
    def total_grade_possible(self):
        total = 0
        for event in self.event_set.all(): 
            if event.max_grade is not None:
                total += event.weight
        return total*100

    def total_grade_lost(self):
        total = 0
        for event in self.event_set.all(): 
            if event.student_grade is not None and event.max_grade is not None: 
                total += float(event.weight) - float(event.grade)
        return total*100
    
    def grade(self):
        if self.total_grade_lost() < 10:
            return 'A+'
        elif self.total_grade_lost() < 15:
            return 'A'
        elif self.total_grade_lost() < 20:
            return 'A-'
        elif self.total_grade_lost() < 25:
            return 'B'
        elif self.total_grade_lost() < 30:
            return 'B+'
        elif self.total_grade_lost() < 40:
            return 'B-'
        elif self.total_grade_lost() < 45:
            return 'C+'
        elif self.total_grade_lost() < 50:
            return 'C-'
        elif self.total_grade_lost() < 55:
            return 'D'
        else:
            return 'F'
        
    def calculate_gpa(self):
        grade = self.grade() 
        gpa_scale = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0,
            'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0
        }
        return gpa_scale.get(grade, 0.0)

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
    name = models.CharField(max_length=255)
    student_grade = models.IntegerField(null=True, blank=True)
    max_grade = models.IntegerField(null=True, blank=True)
    grading_component = models.ForeignKey(to=GradingComponent, on_delete=models.CASCADE)
    date = models.DateField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, null=True, blank=True)
    progress_style = models.CharField(max_length=100, null=True, blank=True, default=None)
    category = models.CharField(max_length=100, null=True, blank=True)
    category_style = models.CharField(max_length=100, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['date']

    @property  
    def weight(self):
        course_component = CourseGradingComponent.objects.get(course=self.course, grading_component=self.grading_component)
        total_events_in_grading_component = Event.objects.filter(course=self.course, grading_component=self.grading_component).count()
        return course_component.weight / total_events_in_grading_component if total_events_in_grading_component > 0 else 0
        
    @property 
    def grade(self):
        if self.student_grade != None and self.max_grade != None:
            student_grade_float = float(self.student_grade)
            max_grade_float = float(self.max_grade)
            return (student_grade_float / max_grade_float) * float(self.weight)
        else:
            return 0

class ToDoItem(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, null=True, blank=True)
    progress_style = models.CharField(max_length=100, null=True, blank=True, default=None)
    category = models.CharField(max_length=100, null=True, blank=True)
    category_style = models.CharField(max_length=100, null=True, blank=True, default=None)

    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['date']  
        
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name   
    
    class Meta:
        verbose_name_plural = "Categories"

class Progress(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name