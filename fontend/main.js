
let projectsUrl =  'http://127.0.0.1:8000/api/projects/'
let loginBtn =  document.getElementById("login-btn")
let logoutBtn =  document.getElementById("logout-btn")

let token = localStorage.getItem('token')

if(token){
    loginBtn.remove()
}else{
    logoutBtn.remove()
}

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = "file:///C:/Users/giait/Desktop/Learn_Django/fontend/login.html"
})

let getProjects = () => {
    fetch(projectsUrl)
    .then(respone =>  respone.json())
    .then(data =>  {
        console.log(data)
        buildProjects(data)
    })
}


let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('projects--wrapper')
    projectsWrapper.innerHTML = ''
    // console.log('projectsWrapper:', projectsWrapper)
    for (let i=0; i < projects.length; i++){
        let project = projects[i]
        
        let projectCard = `
            <div class="project--card">
                <img src = "http://127.0.0.1:8000${project.featured_image}" />
                
                <div>
                    <div class="card--header"> 
                        <h3> ${project.title} </h3>
                        <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive feedback </i>
                    <p>${project.description.substring(0,150)}</p>
                </div>
            </div>
        `

        projectsWrapper.innerHTML += projectCard
    }
    addVoteEvents()
}

let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName("vote--option")
    
    for (let i = 0; i < voteBtns.length; i++){
        let token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI4MjgwMDQ4LCJqdGkiOiI2M2Y2ZmRkOWFhZmQ0YWU5OTI3NDYzOWYzNWM4NDE4MSIsInVzZXJfaWQiOjF9.0e0JLmzTbYai3sKuShby5vWcKKR1VPDHDlOXatkIB8M'
        voteBtns[i].addEventListener('click', (e)=>{
            let vote = e.target.dataset.vote
            let project = e.target.dataset.project
            // console.log("PROJECT:", project, "VOTE:", vote)

            fetch(`http://127.0.0.1:8000/api/project/${project}/vote/`, {
                method:'POST',
                headers: {
                    'Content-Type':'application/json',
                    Authorization: `Bearer ${token}`
                },
                body:JSON.stringify({'value':vote})
            })
            .then(response => response.json())
            .then(data =>{
                console.log("Success", data)
                getProjects()
            })
        })
    }
}

getProjects()