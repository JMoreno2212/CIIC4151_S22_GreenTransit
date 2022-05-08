
async function login() {
    // let login_email = document.getElementById('inputEmail').value;
    // let login_password = document.getElementById('inputPassword').value;
    let login_email = $('#inputEmail').val();
    let login_password = $('#inputPassword').val();
    //let login_type=$('#inputSelectLoginType').val();

    // login_type,

    //console.log(login_password)
    let item = { login_email, login_password }
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
            let user_type = response[3];
                console.log(user_type)
            console.log(response.length)
            let user_id = response[1];
            if (response.length === 4){
                localStorage.setItem('user_id', user_id);
                if(user_type==="Driver"){
                    window.location.href="http://localhost:63342/CIIC4151_S22_GreenTransit/frontend/deliveryTrackerSystemNotAssigned.html?_ijt=blbsjt00ldruvqb7m5ac8rc7jn&_ij_reload=RELOAD_ON_SAVE";
                }
                else if (user_type==="Dispensary"){
                    window.location.href="http://localhost:63342/CIIC4151_S22_GreenTransit/frontend/dispensaryPurchasesTrackerSystem.html?_ijt=5hljvgd0gvuf59jbejnhj46j4h&_ij_reload=RELOAD_ON_SAVE";

                }
                else {
                    window.location.href="";

                }
            }
            else{
                alert("Wrong user/password");
            }

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
        window.location.href="http://localhost:63342/CIIC4151_S22_GreenTransit/frontend/deliveryTrackerSystem.html?_ijt=4d7usskiqlm3vdrqiecb4f49tf&_ij_reload=RELOAD_ON_SAVE";
    }
    else{
        window.location.href="http://localhost:{}/CIIC4151_S22_GreenTransit/frontend/dispensaryRegister.html?_ijt=4rc81j0h57bkupo9a6jemcakph&_ij_reload=RELOAD_ON_SAVE";
    }
    console.log(registration_type);
}

async function submitDeliveryInfo(delivery_id,driver_id){
    console.log("INFO IN THE DB" +"..."+ delivery_id +"..." + driver_id);

    let item = {delivery_id}
    await fetch(`http://127.0.0.1:5000/Driver/drivers/${driver_id}/deliveries`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: JSON.stringify(item),
    })
        .then((response) => response.json())
        .then((response) => {
            location.reload();
            console.log(response)
            //alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })


}

async function updateDeliveryStatus(delivery_id,delivery_status) {
    //window.location.href="http://localhost:63342/CIIC4151_S22_GreenTransit/frontend/deliveryTrackerSystemAssigned.html?_ijt=ipbf8bvtfv7ghif0f0jktibg9d&_ij_reload=RELOAD_ON_SAVE";

    console.log("INFO IN THE DB2" +"..."+ delivery_id +"..." + delivery_status);

    let item = {delivery_status}
    await fetch(`http://127.0.0.1:5000/Delivery/deliveries/${delivery_id}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: JSON.stringify(item),
    })
        .then((response) => response.json())
        .then((response) => {
            location.reload();
            console.log(response)
            //alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}

async function resetPassword() {
    let email = $('#inputEmail').val();
    let passwordNotConfirmed = $('#inputPasswordNotConfirmed').val();
    let password = $('#inputPassword').val();

    if(passwordNotConfirmed !== password){
        alert("Password and Confirm Password must be match!");
    }
    else{

        let item = {email,password}
        await fetch("http://127.0.0.1:5000/resetpassword", {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body: JSON.stringify(item),
        })
            .then((response) => response.json())
            .then((response) => {
                console.log(response)
                //alert(JSON.stringify(response).toString())
            })
            .catch((error) => {
                console.log('API failure' + error)
            })
    }

}


async function addNewProduct() {

    let dispensary_id= localStorage.getItem('user_id');
    let item_name = $('#inputItemName').val();
    let item_description = $('#inputItemDescription').val();
    let item_quantity = $('#inputItemQuantity').val();
    let item_price = $('#inputItemPrice').val();
    let item_category = $('#inputItemCategory').val();
    let item_type = $('#inputItemType').val();
    let item_picture = $('#inputItemPicture').val().replace(/C:\\fakepath\\/i, '');


    let item = { item_name,item_description,item_quantity, item_price, item_category,item_type,item_picture}

    await fetch(`http://127.0.0.1:5000/Dispensary/dispensaries/${dispensary_id}/items`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: JSON.stringify(item),
    })
        .then((response) => response.json())
        .then((response) => {
            console.log(response)
            //alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}


async function updateProductQuantity(item_id, item_quantity) {
    let item = {item_quantity}

    await fetch(`http://127.0.0.1:5000/Item/items/${item_id}/quantity`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: JSON.stringify(item),
    })
        .then((response) => response.json())
        .then((response) => {
            //location.reload();
            //console.log(response)
            //alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}


async function markOrderAsCompleted(purchase_id) {
   // let item = {purchase_id}

    await fetch(`http://127.0.0.1:5000/Purchase/purchases/${purchase_id}/completed`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
    })
        .then((response) => response.json())
        .then((response) => {
            location.reload();
            //console.log(response)
            //alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}