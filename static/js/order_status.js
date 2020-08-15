var updateBtns = document.getElementsByClassName("update-status")

for(var i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        var approve_id = this.dataset.status
        var action = this.dataset.action
        console.log('productId:', approve_id, 'Action:', action)

        console.log('USER:', user)
        if( user == 'AnonymousUser'){
            console.log("Not logged in")
        }else{
            updateOrderStatus(approve_id, action)
        }
    })
}

function updateOrderStatus(approve_id, action) {
    console.log('User is logged in sending data')
    var url = '/update_status/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'approve_status': approve_id, 'action': action})
    })
        .then((response) =>{
            return response.json()
        })
        .then((data) =>{
            console.log('data', data)
            location.reload()
        })
}