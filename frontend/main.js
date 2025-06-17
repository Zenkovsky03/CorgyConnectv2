console.log("dziala");


// LOGIN LOGOUT FUNCTIONALITY

let loginButton = document.getElementById('login-button')
let logoutButton = document.getElementById('logout-button')

let token = localStorage.getItem('token')

if(token){
    loginButton.remove()
}else{
    logoutButton.remove()
}
logoutButton.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    window.location = "http://localhost:63342/CorgyConnect-master/frontend/login.html"
})

// FETCHING DATA TO DISPLAY IN TEMPLATE

let dogsUrl = "http://127.0.0.1:8000/api/dogs/"
let getDogs = () =>{
    fetch(dogsUrl)
        .then(response => response.json())
        .then(data => {
            // console.log(data)
            displayDogs(data)
        })
}

let displayDogs = (dogsJson) =>{
    let dogsWrapper = document.getElementById('dogs-wrapper')
    dogsWrapper.innerHTML = '';
    for (let i = 0; i < dogsJson.length; i++){
        let dog = dogsJson[i];
        let dogCard = `
            <div class="dog--card">
                <img src="http://127.0.0.1:8000${dog.featured_image}" alt="dog_img">
                <div>
                    <div class="card--header">
                        <h3>${dog.name}</h3>
                        <strong class="vote--option" data-vote="up" data-dog="${dog.id}">&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-dog="${dog.id}">&#8722;</strong>
                    </div>
                    <i>${dog.vote_ratio}% Positive feedback</i>
                    <p>${dog.description.substring(0,150)}</p>
                </div>
            </div>
        `
        dogsWrapper.innerHTML += dogCard
    }
    addVoteEvents()
}
// FETCHING CURRENT DOG TO VOTE
let addVoteEvents = () => {
    let voteButtons = document.getElementsByClassName("vote--option")
    for(let i = 0; i < voteButtons.length; i++){
        voteButtons[i].addEventListener('click', (e) => {
            let vote = e.target.dataset.vote
            let dog = e.target.dataset.dog
            let token = localStorage.getItem('token')

            fetch(`http://127.0.0.1:8000/api/dogs/${dog}/vote/`, {
                method:"POST",
                headers:{
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ 'value':vote })
            })
            .then(response => response.json())
            .then(data => {
                console.log("success ", data)
                getDogs()
            })
        })
    }
}
getDogs()
