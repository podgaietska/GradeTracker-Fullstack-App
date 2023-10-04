from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, GradingComponent, CourseGradingComponent, Event
from django.contrib import messages
from django.core import serializers
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    courses = Course.objects.filter(owner=request.user)
    
    context = {
        'courses': courses,
    }
    return render(request, 'gradeapp/index.html', context)

def add_instance(request, grading_component_id):
    component = CourseGradingComponent.objects.get(pk=grading_component_id)
    
    context = {
        'component': component,
    }
    
    if request.method == 'GET':    
        return render(request, 'gradeapp/add_instance.html', context)
    
    if request.method == 'POST':
        grading_component = component.grading_component
        course = component.course
        
        name = request.POST['name']
        date = request.POST['date']
        
        if not name:
            messages.error(request, 'Name for the Assignment/Quiz is required')
            return render(request, 'gradeapp/add_instance.html', context)
        
        if not date:
            messages.error(request, 'Date for the Assignment/Quiz is required')
            return render(request, 'gradeapp/add_instance.html', context)
        
        event = Event(
            name = name,
            grading_component = grading_component,
            date = date,
            course = course,
            owner = request.user
        )
        event.save()
        
        messages.success(request, 'Assignment/Quiz added successfully')
        return redirect('course-home', course_id=course.id)
        

def add_course(request):
    grading_components = GradingComponent.objects.all()
    lecture_sections = ['L01', 'L02', 'L03', 'L04', 'L05']
    lab_sections = ['B01', 'B02', 'B03']
    seminar_sections = ['S01', 'S02', 'S03']
    
    context = {
            'grading_components' : grading_components,
            'values': request.POST,
            'lecture_sections': lecture_sections,
            'lab_sections': lab_sections,
            'seminar_sections': seminar_sections,
        }
    
    if request.method == 'GET':
        return render(request, 'gradeapp/add_course.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        lecture_section = request.POST['lecture-section']
        lab_section = request.POST['lab-section']
        seminar_section = request.POST['seminar-section']
        grading_components = request.POST.getlist('grading-component')
        weights = request.POST.getlist('weight')
        totalweight = 0
        
        if not name:
            messages.error(request, 'Course name is required')
            return render(request, 'gradeapp/add_course.html', context)
        
        if not code:
            messages.error(request, 'Course code is required')
            return render(request, 'gradeapp/add_course.html', context)
        
        if not lecture_section:
            messages.error(request, 'Lecture section is required')
            return render(request, 'gradeapp/add_course.html', context)
        
        if lab_section == '-':
            lab_section = None
            
        if seminar_section == '-':
            seminar_section = None
    
        if not weights:
            messages.error(request, 'Weights are required')
            return render(request, 'gradeapp/add_course.html', context)
        
        for weight in weights:
            totalweight += float(weight)
                
        if totalweight != 1:
                messages.error(request, 'Weights of course components must add up to 1 (100%)')
                return render(request, 'gradeapp/add_course.html', context)
        
        if not grading_components:
            messages.error(request, 'Grading components are required')
            return render(request, 'gradeapp/add_course.html', context)
        
        if (len(grading_components) != len(weights)):
            messages.error(request, 'You must enter a weight for each grading component')
            return render(request, 'gradeapp/add_course.html', context)
            
        course = Course(
            name = name,
            code = code,
            lecture = lecture_section,
            lab = lab_section,
            seminar = seminar_section,
            owner = request.user
        )       
        course.save()
        
        for grading_component, weight in zip(grading_components, weights):
            course_grading_component = CourseGradingComponent(
                course = Course.objects.get(code=code),
                grading_component = GradingComponent.objects.get(name=grading_component),
                weight = weight          
            )
            course_grading_component.save()
        
        messages.success(request, 'Course added successfully')
        return redirect('gradeapp')
        
def get_grading_components(request):
    if request.method == 'GET':
        grading_components = GradingComponent.objects.all().values_list('name', flat=True)
        return JsonResponse(list(grading_components), safe=False)
    
def get_courses(request):
    if request.method == 'GET':
        courses = Course.objects.filter(owner=request.user)
        courses_json = serializers.serialize('json', courses)
        return JsonResponse(courses_json, safe=False)  
    
def course_home(request, course_id):
    course = Course.objects.get(pk=course_id);
    course_grading_components = CourseGradingComponent.objects.filter(course=course);

    context = {
        'course': course,
        'course_grading_components': course_grading_components,
    }
    
    if request.method == 'GET':
        for component in course_grading_components:
            print(component.id)
        return render(request, 'gradeapp/course_home.html', context)

def edit_course(request, course_id):
    course = Course.objects.get(pk=course_id);
    course_grading_components = CourseGradingComponent.objects.filter(course=course);
    lecture_sections = ['L01', 'L02', 'L03', 'L04', 'L05']
    lab_sections = ['B01', 'B02', 'B03']
    seminar_sections = ['S01', 'S02', 'S03']
        
    context = {
        'course': course,
        'edit': True,
        'lecture_sections': lecture_sections,
        'lab_sections': lab_sections,
        'seminar_sections': seminar_sections,
        'course_grading_components': course_grading_components,
    }
    
    if request.method == 'GET':
        return render(request, 'gradeapp/course_home.html', context)
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        lecture_section = request.POST['lecture-section']
        lab_section = request.POST['lab-section']
        seminar_section = request.POST['seminar-section']
        
        if not name:
            messages.error(request, 'Course name is required')
            return render(request, 'gradeapp/course_home.html', context)
        
        if not code:
            messages.error(request, 'Course code is required')
            return render(request, 'gradeapp/course_home.html', context)
        
        if not lecture_section:
            messages.error(request, 'Lecture section is required')
            return render(request, 'gradeapp/course_home.html', context)
        
        if lab_section == '-':
            lab_section = None
            
        if seminar_section == '-':
            seminar_section = None
            
        course.owner = request.user
        course.name = name
        course.lab = lab_section
        course.lecture = lecture_section
        course.seminar = seminar_section
        course.code = code
        
        course.save()
        
        return redirect('course-home', course_id=course_id)
        
        