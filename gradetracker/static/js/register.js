const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector('.invalid-feedback');

console.log(usernameField);

const emailField = document.querySelector('#emailField');
const emailFeedbackField = document.querySelector('.email-invalid-feedback');

const passwordField = document.querySelector('#passwordField');
const passwordToggle = document.querySelector('.password-toggle');

const submitBtn = document.querySelector('.submit-btn');

const handlePasswordToggle = (e) => {
    if(passwordToggle.textContent === 'SHOW'){
        console.log('show');
        passwordToggle.textContent = 'HIDE';
        passwordField.setAttribute('type', 'text');
    } else{
        passwordToggle.textContent = 'SHOW';
        passwordField.setAttribute('type', 'password');
    }
}

passwordToggle.addEventListener('click', handlePasswordToggle);

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove('is-invalid');
    emailFeedbackField.style.display = 'none';

    if(emailVal.length > 0){
        fetch('/auth/validate-email', {
            body: JSON.stringify({ email: emailVal }),
            method: 'POST',
        }).then(res => res.json()).then(data => {
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedbackField.style.display = 'block';
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`; 
                submitBtn.setAttribute("disabled", true);
            }else{
                submitBtn.removeAttribute('disabled');
            }
        })
    } 
});

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = 'none';

    if(usernameVal.length > 0){
        fetch('/auth/validate-username', {
            body: JSON.stringify({ username: usernameVal }),
            method: 'POST',
        }).then(res => res.json()).then(data => {
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackField.style.display = 'block';
                feedbackField.innerHTML = `<p>${data.username_error}</p>`; 
                submitBtn.setAttribute("disabled", true);
            } else{
                submitBtn.removeAttribute('disabled');
            }
        })
    }   
});
