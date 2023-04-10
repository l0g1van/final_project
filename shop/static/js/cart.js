let updateBtns = document.getElementsByClassName('update-cart')

for(let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		let bookId = this.dataset.book
		let action = this.dataset.action
		console.log('bookId:', bookId, 'Action:', action)
		console.log('USER:', user)

		if (user === 'AnonymousUser'){
			window.location.href = '/login/';
			// console.log('Not logged in')
		}else{
			updateUserOrder(bookId, action)
		}
	})
}


function  updateUserOrder(bookId, action){
	console.log('User is logged in, sending data...')

	let url = '/update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body:JSON.stringify({'bookId': bookId, 'action': action})
	})

		.then((response) =>{
			return response.json()
		})

		.then((data) =>{
			location.reload()
		})
}
