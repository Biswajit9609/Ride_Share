document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let email = document.getElementById("email").value;
    let phone = document.getElementById("phone").value;

    if (!email.includes("@") || phone.length < 7) {
        alert("Please enter a valid email and phone number.");
    } else {
        alert("Sign-up successful!");
    }
});
