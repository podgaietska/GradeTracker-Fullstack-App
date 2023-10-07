from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, GradingComponent, CourseGradingComponent, Event, ToDoItem, Progress, Category
from django.contrib import messages
from django.core import serializers
from datetime import datetime
import re
from decimal import Decimal


# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    courses = Course.objects.filter(owner=request.user)
    events = Event.objects.filter(owner = request.user)
    todo_items = ToDoItem.objects.filter(owner = request.user)
    user = request.user
    
    gpas = [course.calculate_gpa() for course in courses]
    
    gpa = sum(gpas) / len(gpas) if gpas else 0.0

    context = {
        'courses': courses,
        'events': events,
        'todo_items': todo_items,
        'user': user,
        'gpa': gpa,
    }
    
    print(gpa)
    return render(request, 'gradeapp/index.html', context)  

def get_grading_components(request):
    if request.method == 'GET':
        grading_components = GradingComponent.objects.all().values_list('name', flat=True)
        return JsonResponse(list(grading_components), safe=False)
    
def get_courses(request):
    if request.method == 'GET':
        courses = Course.objects.filter(owner=request.user)
        courses_json = serializers.serialize('json', courses)
        return JsonResponse(courses_json, safe=False)  

def add_course(request):
    grading_components = GradingComponent.objects.all()
    lecture_sections = ['L01', 'L02', 'L03', 'L04', 'L05']
    lab_sections = ['B01', 'B02', 'B03']
    seminar_sections = ['S01', 'S02', 'S03']
    user = request.user
    
    context = {
            'grading_components' : grading_components,
            'values': request.POST,
            'lecture_sections': lecture_sections,
            'lab_sections': lab_sections,
            'seminar_sections': seminar_sections,
            'user': user,
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
        totalweight = Decimal('0.0')
        
        course = Course.objects.filter(code=code, owner=request.user)
        if course:
            messages.error(request, 'Course with that code already exists')
            return render(request, 'gradeapp/add_course.html', context)
        
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
            if weight == '' or not weight:
                messages.error(request, 'Weights are required')
                return render(request, 'gradeapp/add_course.html', context)
            else:
                totalweight += Decimal(weight)
                
        print(totalweight)
        if totalweight != Decimal('1.0'):
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
                course = Course.objects.get(code=code, owner=request.user),
                grading_component = GradingComponent.objects.get(name=grading_component),
                weight = weight          
            )
            course_grading_component.save()
        
        messages.success(request, 'Course added successfully')
        return redirect('gradeapp')
    
def edit_course(request, course_id):
    course = Course.objects.get(pk=course_id);
    course_grading_components = CourseGradingComponent.objects.filter(course=course);
    events = Event.objects.filter(owner = request.user, course=course)
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
        'events':events,
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
    
def course_home(request, course_id):
    course = Course.objects.get(pk=course_id);
    course_grading_components = CourseGradingComponent.objects.filter(course=course)
    events = Event.objects.filter(owner = request.user, course=course) 

    total_grades = {component.grading_component.id: 0 for component in course_grading_components}
    
    for event in events:
        if event.grading_component.id in total_grades:
            total_grades[event.grading_component.id] += event.grade

    context = {
        'course': course,
        'course_grading_components': course_grading_components,
        'events': events,
        'total_grades': total_grades,
    }
    
    if request.method == 'GET':
        return render(request, 'gradeapp/course_home.html', context)

def add_instance(request, grading_component_id):
    progress_options = Progress.objects.all()
    category_options = Category.objects.all()
    component = CourseGradingComponent.objects.get(pk=grading_component_id)
    is_exam = False
    
    if component.grading_component.name == 'Final Exam' or component.grading_component.name == 'Midterm' or component.grading_component.name == 'Midterm 2' or component.grading_component.name == 'Final Project':
        is_exam = True
    
    context = {
        'component': component,
        'values': request.POST,
        'is_exam': is_exam,
        'progress_options': progress_options,
        'category_options': category_options,
    }
    
    if request.method == 'GET': 
        return render(request, 'gradeapp/edit_instance.html', context)
    
    if request.method == 'POST':
        grading_component = component.grading_component
        course = component.course
        name = grading_component.name
        progress = request.POST['progress']
        styling = {'Not Started': 'not-started', 'In Progress': 'in-progress', 'Finished': 'finished', 'Cancelled': 'cancelled', 'Urgent!': 'urgent', None: None}
        category = request.POST['category']
        category_styling = {'Urgent!': 'urgent', 'Important!': 'cancelled', None: None}
        
        if progress == '-':
            progress = None
            
        if category == '-':
            category = None
            
        if not is_exam:
            name = request.POST['name']
            
        date = request.POST['date']
        student_grade = request.POST['student-grade']
        max_grade = request.POST['max-grade']
        
        if not student_grade or student_grade == '0':
            student_grade = None
            
        if not max_grade or max_grade == '0':
            max_grade = None
            
        # Change if neccessary
        if student_grade and not max_grade or max_grade and not student_grade:
            max_grade = None
            student_grade = None
        
        if not name and not is_exam:
            messages.error(request, 'Name for the Assignment/Quiz is required')
            return render(request, 'gradeapp/edit_instance.html', context)
        
        if not date:
            messages.error(request, 'Date for the Assignment/Quiz is required')
            return render(request, 'gradeapp/edit_instance.html', context)
        
        event = Event(
            name = name,
            student_grade = student_grade,
            max_grade = max_grade,
            grading_component = grading_component,
            date = date,
            course = course,
            owner = request.user,
            progress = progress,
            progress_style = styling[progress],
            category = category,
            category_style = category_styling[category],
        )
        event.save()
        
        messages.success(request, 'Assignment/Quiz added successfully')
        return redirect('course-home', course_id=course.id)  
    
def edit_instance(request, event_id):
    event = Event.objects.get(pk=event_id)
    course = event.course
    grading_component = event.grading_component
    progress_options = Progress.objects.all()
    category_options = Category.objects.all()
    
    context = {
        'edit_instance': True,
        'values': request.POST,
        'grading_component': grading_component,
        'event': event,
        'course': course.code,
        'progress_options': progress_options,
        'category_options': category_options,
    }
    
    if request.method == 'GET': 
        return render(request, 'gradeapp/edit_instance.html', context)
    
    if request.method == 'POST':
        grading_component = event.grading_component
        course = event.course
        
        name = request.POST['name']
        input_date = request.POST['date']
        formatted_date = input_date
        student_grade = request.POST['student-grade']
        max_grade = request.POST['max-grade']
        
        progress = request.POST['progress']
        styling = {'Not Started': 'not-started', 'In Progress': 'in-progress', 'Finished': 'finished', 'Cancelled': 'cancelled', 'Urgent!': 'urgent', None: None}
        category = request.POST['category']
        category_styling = {'Urgent!': 'urgent', 'Important!': 'cancelled', None: None}
        
        if progress == '-':
            progress = None
            
        if category == '-':
            category = None
            
        if not formatted_date or formatted_date == '':
            formatted_date = None;
        else: 
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', input_date):    
                parsed_date = datetime.strptime(input_date, '%b. %d, %Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d') 
                
        if not student_grade or student_grade == '0':
            student_grade = None
            
        if not max_grade or max_grade == '0':
            max_grade = None
            
        # Change if neccessary
        if student_grade and not max_grade or max_grade and not student_grade:
            max_grade = None
            student_grade = None
        
        if not name:
            messages.error(request, 'Name for the Assignment/Quiz is required')
            return render(request, 'gradeapp/edit_instance.html', context)
        
        if not input_date:
            messages.error(request, 'Date for the Assignment/Quiz is required')
            return render(request, 'gradeapp/edit_instance.html', context)
        
        event.owner = request.user
        event.name = name
        event.student_grade = student_grade
        event.max_grade = max_grade
        event.grading_component = grading_component
        event.date = formatted_date
        event.course = course
        event.progress = progress
        event.progress_style = styling[progress]
        event.category = category
        event.category_style = category_styling[category]
        
        event.save()
        
        messages.success(request, 'Assignment/Quiz edited successfully')
        return redirect('course-home', course_id=course.id)      

def edit_grades(request, course_id):
    course = Course.objects.get(pk=course_id);
    course_grading_components = CourseGradingComponent.objects.filter(course=course);
    events = Event.objects.filter(owner = request.user, course=course)
    exam_has_event = {'Final Exam': False, 'Midterm': False, 'Midterm 2': False, 'Final Project': False}

    total_grades = {component.grading_component.id: 0 for component in course_grading_components}

    for event in events:
        if event.grading_component.id in total_grades:
            total_grades[event.grading_component.id] += event.grade
        if event.grading_component.name == 'Final Exam':
            exam_has_event['Final Exam'] = event.id
        if event.grading_component.name == 'Midterm':
            exam_has_event['Midterm'] = event.id
        if event.grading_component.name == 'Midterm 2':
            exam_has_event['Midterm 2'] = event.id
        if event.grading_component.name == 'Final Project':
            exam_has_event['Final Project'] = event.id
    
    for event in events:
        print(event.id)
        
    print(exam_has_event)
    
    context = {
        'course': course,
        'edit_grades': True,
        'course_grading_components': course_grading_components,
        'events':events,
        'total_grades': total_grades,
        'exam_has_event': exam_has_event,
    }
    
    if request.method == 'GET':
        print(exam_has_event)
        return render(request, 'gradeapp/course_home.html', context)

def add_todo_item(request):
    progress_options = Progress.objects.all()
    category_options = Category.objects.all()
    
    context = {
        'progress_options': progress_options,
        'values': request.POST,
        'category_options': category_options,
    }
    
    if request.method == 'GET':
        return render(request, 'gradeapp/add_todo_item.html', context)
    
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        progress = request.POST['progress']
        category = request.POST['category']
        styling = {'Not Started': 'not-started', 'In Progress': 'in-progress', 'Finished': 'finished', 'Cancelled': 'cancelled', None: None}
        category_styling = {'Urgent!': 'urgent', 'Important!': 'cancelled', None: None}
                        
        if not name:
            messages.error(request, 'Name for the To-Do Item is required')
            return render(request, 'gradeapp/add_todo_item.html', context)
        
        if progress == '-':
            progress = None
            
        if category == '-':
            category = None
            
        if not date:
            date = None
        
        todo_item = ToDoItem(
            name = name,
            date = date,
            progress = progress,
            owner = request.user,
            progress_style = styling[progress],
            category = category,
            category_style = category_styling[category],
        )
        todo_item.save()
        
        messages.success(request, 'To-Do Item added successfully')
        return redirect('gradeapp')

def edit_todo_item(request, todo_id):
    todo = ToDoItem.objects.get(pk=todo_id)
    progress_options = Progress.objects.all()
    category_options = Category.objects.all()

    context = {
        'progress_options': progress_options,
        'edit_todo': True,
        'todo': todo,
        'values': request.POST,
        'category_options': category_options,
    }
    
    if request.method == 'GET':
        return render(request, 'gradeapp/add_todo_item.html', context);
    
    if request.method == 'POST':
        name = request.POST['name']
        input_date = request.POST['date']
        formatted_date = input_date
        progress = request.POST['progress']
        styling = {'Not Started': 'not-started', 'In Progress': 'in-progress', 'Finished': 'finished', 'Cancelled': 'cancelled', 'Urgent!': 'urgent', None: None}
        category = request.POST['category']
        category_styling = {'Urgent!': 'urgent', 'Important!': 'cancelled', None: None}

        
        if not name:
            messages.error(request, 'Name for the To-Do Item is required')
            return render(request, 'gradeapp/add_todo_item.html', context)
        
        if progress == '-':
            progress = None
            
        if category == '-':
            category = None
            
        if not formatted_date or formatted_date == '':
            formatted_date = None;
        else: 
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', input_date):    
                parsed_date = datetime.strptime(input_date, '%b. %d, %Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')   

        todo.name = name
        if formatted_date:
            todo.date = formatted_date
        else:
            todo.date = None
        todo.progress = progress
        todo.owner = request.user
        todo.progress_style = styling[progress]
        todo.category = category
        todo.category_style = category_styling[category]

        todo.save()
        
        messages.success(request, 'To-Do Item updated successfully')
        return redirect('gradeapp')