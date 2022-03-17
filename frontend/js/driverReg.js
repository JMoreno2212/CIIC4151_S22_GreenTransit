




async function driverReg() {
    let registration_type = "Driver";
    let registration_first_name = $('#firstNameDriver').val();
    let registration_last_name = $('#lastNameDriver').val();
    let registration_birth_date = $('#dobDriver').val();
    let registration_phone = $('#phoneDriver').val();
    let registration_email = $('#emailDriver').val();
    let registration_password = $('#passwordDriver').val();
    let driver_driving_license = $('#driverLicenseDriver').val();
    let driver_gmp_certificate = $('#gmpFileDriver').val().replace(/C:\\fakepath\\/i, '');
    let driver_dispensary_technician = $('#technicianFileDriver').val().replace(/C:\\fakepath\\/i, '');
    let license_type = "Occupational"
    let license_name = $('#licenseDriver').val();
    let license_expiration = $('#licenseExpDateDriver').val();
    let license_file = $('#occupationalFileDriver').val().replace(/C:\\fakepath\\/i, '');
    //let dispensary_name = "";
    //let dispensary_location = "";

    // let registration_type = "Driver";
    // let registration_first_name = "Manuel";
    // let registration_last_name = "Vega";
    // let registration_birth_date = "2022/03/01";
    // let registration_phone = "7875426982";
    // let registration_email = "mvega@gmail.com";
    // let registration_password = "pass123";
    // let driver_driving_license = "4587632";
    // let driver_gmp_certificate = "Proposal.pdf";
    // let driver_dispensary_technician = "Proposal.pdf";
    // let license_type = "Occupational"
    // let license_name = "asr454";
    // // let license_name = $('#licenseDriver').val();
    // let license_expiration = "2022/03/31";
    // let license_file = "Proposal.pdf";
    // //let dispensary_name = "";
    // //let dispensary_location = "";




    //console.warn(login_type,login_email, login_password)
    //console.log(login_password)
    let item = { registration_type, registration_first_name, registration_last_name, registration_birth_date, registration_phone, registration_email, registration_password, driver_driving_license, driver_gmp_certificate, driver_dispensary_technician, license_type, license_name, license_expiration, license_file }
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