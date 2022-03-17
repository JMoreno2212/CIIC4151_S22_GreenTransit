
async function login() {
    // let login_email = document.getElementById('inputEmail').value;
    // let login_password = document.getElementById('inputPassword').value;
    let login_email = $('#inputEmail').val();
    let login_password = $('#inputPassword').val();
    let login_type=$('#inputSelectLoginType').val();

    console.log(login_password)
    let item = { login_type, login_email, login_password }
    await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: JSON.stringify(item),
    })
        .then((response) => response.json())
        .then((response) => {
            console.log(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}

async function register() {
    let registration_type=$('#inputSelectRegisterType').val();
    localStorage.setItem('registration_type', registration_type);
    if(registration_type === 'User') {
        window.location.href="http://localhost:{}/CIIC4151_S22_GreenTransit/frontend/userRegistrationPage.html?_ijt=7b67ai6dbicbr9hnusncjh0ovj&_ij_reload=RELOAD_ON_SAVE"
    }
    else if (registration_type === 'Driver'){
        window.location.href="http://localhost:{}/CIIC4151_S22_GreenTransit/frontend/driverRegister.html?_ijt=4rc81j0h57bkupo9a6jemcakph&_ij_reload=RELOAD_ON_SAVE";
    }
    else{
        window.location.href="http://localhost:{}/CIIC4151_S22_GreenTransit/frontend/dispensaryRegister.html?_ijt=4rc81j0h57bkupo9a6jemcakph&_ij_reload=RELOAD_ON_SAVE";
    }
    console.log(registration_type);
}
