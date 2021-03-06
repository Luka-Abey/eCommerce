var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var itemId = this.dataset.product
    var action = this.dataset.action
    console.log(itemId, action)

    console.log(user)
    if(user === 'AnonymousUser'){
      console.log("you are not logged in")
    }
    else {
      updateUserOrder(itemId, action)
    }

  })
}

function updateUserOrder(itemId, action){

  var url = '/update_item/'

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({'itemId': itemId, 
    'action': action})
  })
  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    location.reload()
  })
}