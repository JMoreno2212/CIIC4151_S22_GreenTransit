
async function userRegistration() {
    let registration_type= localStorage.getItem('registration_type');
    let license_file = $('#inputPatientLicenseIDFile').val().replace(/C:\\fakepath\\/i, '');
    let license_name = $('#inputPatientLicense').val();
    let license_expiration = $('#inputLicenseExpirationDate').val();
    let registration_first_name = $('#inputUserFirstName').val();
    let registration_last_name = $('#inputUserLastName').val();
    let registration_birth_date = $('#inputDateOfBirth').val();
    let registration_phone = $('#inputUserPhoneNumber').val();
    let registration_email = $('#inputUserEmail').val();
    let registration_password = $('#inputUserPassword').val();
    let dispensary_name = '';
    let dispensary_location = '';

    let item = {registration_type, license_file, license_name, license_expiration, registration_first_name, registration_last_name, registration_birth_date, registration_phone, registration_email, registration_password, dispensary_name, dispensary_location }
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
            alert(JSON.stringify(response).toString())
        })
        .catch((error) => {
            console.log('API failure' + error)
        })
}

// console.warn(registration_type);
// console.warn(license_file);
// console.log(license_name);
// console.log(license_expiration);
// console.log(registration_first_name);
// console.log(registration_last_name);
// console.log(registration_birth_date);
// console.log(registration_phone);
// console.log(registration_email);
// console.log(registration_password);

//alert(registration_type + "   "+license_file+ "   "+license_expiration);