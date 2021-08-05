let form = document.getElementById('login-form')

form.addEventListener('submit', (e) =>{
    e.preventDefault() // prevent the page refreshing after pressing submit button
    
    let formData = {
        'username':form.username.value,
        'password':form.password.value,
    }
    
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body:JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('DATA', data)
        if(data.access){
            localStorage.setItem('token', data.access)
            window.location = "file:///C:/Users/giait/Desktop/Learn_Django/fontend/projects-list.html"
        }else{
            alert("Username or password is incorrect.")
        }
    })
})