let img = document.querySelector(#image-slider);
window.onload = function() {
    alert("Welcome to Sorare!");
}
let btn = document.querySelector('.toggle-btn');
let element = document.querySelector('.element');

btn.addEventListener('click', function() {
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
});

document.getElementById("sign-in-button").addEventListener("click", function(){
    window.location.href = "login.html";
});

