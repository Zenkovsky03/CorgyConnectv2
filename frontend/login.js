let form = document.getElementById("login-form")

let api = "http://127.0.0.1:8000/api/users/token/"
form.addEventListener('submit', (e) =>{
    e.preventDefault()

    let formData = {
        'username': form.username.value,
        'password': form.password.value,
    }

    fetch(api, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)

    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data.access){
            localStorage.setItem('token', data.access)
            window.location = 'http://localhost:63342/CorgyConnect-master/frontend/dogs-list.html'
        }else
            alert("Incorrect username or password")
    })
})