// let login_email = document.getElementById('inputEmail').value;
// let login_password = document.getElementById('inputPassword').value;

let login_email = $('inputEmail').val();
let login_password = $('inputPassword').val();
let login_type="User";

// $("inputEmail").change(function(){
//   window.alert("cry");
// });

async function login() {
    console.warn(login_type,login_email, login_password)
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
