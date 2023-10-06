
console.log("messages.js loaded");

const messageCloseBtn = document.querySelector('.message-close-btn');
const messageContainer = document.querySelector('.messages');

messageCloseBtn.addEventListener('click', function(){
    const message = messageCloseBtn.parentElement;
    message.remove();
    messageContainer.remove();
});