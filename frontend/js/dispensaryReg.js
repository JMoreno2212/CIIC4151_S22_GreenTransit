




async function dispensaryReg() {
    let registration_type = "Dispensary";
    // let dispensary_name = $('#nameDispensary').val();
    //     // let registration_phone = $('#phoneDispensary').val();
    //     // let dispensary_location = $('#addressDispensary').val();
    //     // let registration_email = $('#emailDispensary').val();
    //     // let registration_password = $('#passwordDispensary').val();
    //     // let license_type = "Dispensary";
    //     // let license_name = $('#licenseDispensary').val();
    //     // let license_expiration = $('#licenseExpDateDispensary').val();
    //     // let license_file =  $('#dispensaryLicenseFile').val().replace(/C:\\fakepath\\/i, '');
    let dispensary_name = "DD";
    let registration_phone = "7875667878";
    let dispensary_location = "Aguadilla";
    let registration_email = "dd@gmail.com";
    let registration_password = "pass123";
    let license_type = "Dispensary";
    let license_name = "1234567";
    let license_expiration = "2022-02-27";
    let license_file =  "license_file.pdf";


    //console.warn(login_type,login_email, login_password)
    //console.log(login_password)
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