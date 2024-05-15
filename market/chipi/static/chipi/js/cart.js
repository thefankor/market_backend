const input = document.querySelector('.cart-right-22-input');
const button = document.querySelector('.cart-right-22-btn1');
const promokod = document.querySelector('.promokod')
const cart_right = document.querySelector('.cart-right-2')

button.addEventListener( 'click', function() {
    if (input.value.length > 0) {
        promokod.style.display = 'block'
        cart_right.style.height = '250px'
    } else {
        promokod.style.display = 'none'
        cart_right.style.height = '230px'
    }
})