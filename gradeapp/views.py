from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, GradingComponent, CourseGradingComponent, Assignment, Category
from django.contrib import messages
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    grading_components = GradingComponent.objects.all()
    courses = Course.objects.filter(owner=request.user)
    
    context = {
        'courses': courses,
    }
    return render(request, 'gradeapp/index.html', context)

def add_course(request):
    grading_components = GradingComponent.objects.all()
    context = {
            'grading_components' : grading_components,
            'values': request.POST
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
        courses = Course.objects.filter(owner=request.user).values_list('code', flat=True)
        return JsonResponse(list(courses), safe=False)