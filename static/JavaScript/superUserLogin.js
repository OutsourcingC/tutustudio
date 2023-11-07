const loginAccount = function() {
    const username = $("#username").val()
    const plaintext = $("#password").val()

    const iv = CryptoJS.lib.WordArray.random(16);
    const key = CryptoJS.lib.WordArray.random(32);

    const ciphertext = CryptoJS.AES.encrypt(
        plaintext,
        key,
        {
            iv: iv,
        }
    ).toString();

    const encryptedData = {
        usaername: username,
        iv: iv.toString(CryptoJS.enc.Base64),
        key: key.toString(CryptoJS.enc.Base64),
        ciphertext: ciphertext,
    };

    $.ajax({
        type: 'POST',
        url: '/api/super_user_login',
        data: JSON.stringify(encryptedData),
        contentType: 'application/json',
        success: function(response, status) {
            console.log("success")
        }
    });
}

