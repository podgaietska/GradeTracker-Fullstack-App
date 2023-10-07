function updateCourseList() {
    console.log('Updating course list...');
    $.get('/get-courses', function(data) {
        console.log(data);
        const coursesList = document.querySelector('#courses-list')

        coursesList.innerHTML = '';
        const courses = JSON.parse(data);
        console.log(courses);

        courses.forEach(function(course){
            const listItem = document.createElement('li');
            listItem.className = 'nav-item';

            const link = document.createElement('a');
            link.className = 'nav-link';
            link.href = `/course-home/${course.pk}`;
            link.textContent = course.fields.code;

            listItem.appendChild(link);
            coursesList.appendChild(listItem);
        })
    })
}

document.addEventListener('DOMContentLoaded', updateCourseList);



