




async function dispensaryReg() {
    let registration_type= localStorage.getItem('registration_type');
    let dispensary_name = $('#nameDispensary').val();
    let registration_phone = $('#phoneDispensary').val();
    let dispensary_location = $('#addressDispensary').val();
    let registration_email = $('#emailDispensary').val();
    let registration_password = $('#passwordDispensary').val();
    let license_type = "Dispensary";
    let license_name = $('#licenseDispensary').val();
    let license_expiration = $('#licenseExpDateDispensary').val();
    //let license_file =  $('#dispensaryLicenseFile').val().replace(/C:\\fakepath\\/i, '');

    
    let item = { registration_type, dispensary_name, registration_phone, dispensary_location, registration_email, registration_password, license_type, license_name, license_expiration, license_file }
    await fetch('http://127.0.0.1:5000/register', {
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

async function userImage() {
    let inputFile =  document.getElementById("dispensaryLicenseFile").files[0];
    let formData = new FormData();
    formData.append("user_picture", inputFile);
    alert(formData);
    console.log(formData)

    await fetch('http://127.0.0.1:5000/User/users/16/picture', {
        method: 'PUT',
        body: formData,
    })
        .then((response) => response.json())
        .then((response) => {
            console.log(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}