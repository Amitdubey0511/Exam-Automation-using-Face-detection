const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});


loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});
document.getElementById('alrt').innerHTML='<b>Invalid login credentials. Please try again.</b>'; 
setTimeout(function() {document.getElementById('alrt').innerHTML='';},5000);