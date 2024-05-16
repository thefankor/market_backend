const passwordInput = document.getElementById('password')
const changeButton = document.getElementById('parol')


changeButton.addEventListener( 'click', function() {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text'
    } else {
        passwordInput.type = 'password'
    }
})



