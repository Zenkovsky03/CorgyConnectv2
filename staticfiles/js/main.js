let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

if(searchForm){
    for(let i= 0; pageLinks.length > i; i++){
        pageLinks[i].addEventListener('click', function (e) {
            console.log(this)
            e.preventDefault()
            console.log('clicked')
            let page = this.dataset.page
            console.log(page)
            searchForm.innerHTML += `<input value=${page} name="page" hidden />`
            searchForm.submit()
        })
    }
}
//to dziala tak ze preventDefault nie przeladowywuje strony i my przez klikniecie przekazujemy page czyli numer strony i wteyd na danej stronie dalej mamy search wynik ktory chcemy
//sztuczne przeladowanie storny

let tags = document.getElementsByClassName('project-tag')

for(let i = 0; i < tags.length; i++){
    tags[i].addEventListener("click", (e) => {
        let tagID = e.target.dataset.tag
        let dogID = e.target.dataset.dog
        let api = "http://127.0.0.1:8000/api/remove-tag/"
        console.log(tagID + " " + dogID)
        fetch(api, {
            method: "DELETE",
            headers: {
                'Content-Type': "application/json",
            },
            body: JSON.stringify({
                'dog': dogID,
                'tag': tagID,
            })

        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })
    })
}