function updateCourseList() {
    $.get('get-courses', function(data) {
        const coursesList = document.querySelector('#courses-list')

        coursesList.innerHTML = '';

        data.forEach(function(courseName){
            const listItem = document.createElement('li');
            listItem.className = 'nav-item';

            const link = document.createElement('a');
            link.className = 'nav-link';
            link.href = '#';
            link.textContent = courseName;

            listItem.appendChild(link);
            coursesList.appendChild(listItem);
        })
    })
}

document.addEventListener('DOMContentLoaded', updateCourseList);

