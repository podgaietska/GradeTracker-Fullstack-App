const burger = document.querySelector('.burger-menu');
const sidebar = document.querySelector('.sidebar');
const main = document.querySelector('.main-container');

burger.addEventListener('click', function() {
    sidebar.classList.toggle('sidebar-inactive');
    main.classList.toggle('main-container-fullscreen');
    console.log(main);
    console.log(sidebar);
    // main.classList.toggle('main-container-fullscreen');
});