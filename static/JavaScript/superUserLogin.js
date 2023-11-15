const usernameInputBox = $("#username")
const passwordInputBox = $("#password")
const errorMessageLabel = $("#error-message")
const errorInputSpaceLabel = $("#error-input-space")
const buttonSubmit = $("#button-submit")

function containsSpace(inputValue) {
    let spaceRegex = /\s/;
    let result = spaceRegex.test(inputValue)

    errorMessageLabel.text("")

    if (result) {
        errorInputSpaceLabel.text("输入框中不可包含空格")
        buttonSubmit.prop("disabled", true);
    } else {
        errorInputSpaceLabel.text("")
        buttonSubmit.prop("disabled", false);
    }
}

const loginAccount = function() {
    let username = usernameInputBox.val()
    let password = passwordInputBox.val()


    const iv = CryptoJS.lib.WordArray.random(16);
    const key = CryptoJS.lib.WordArray.random(32);

    const ciphertext = CryptoJS.AES.encrypt(
        password,
        key,
        {
            iv: iv,
        }
    ).toString();

    const encryptedData = {
        username: username,
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
        },
        error: function(response, status) {
            errorMessageLabel.text(response.responseJSON.message)
        }
    });
}


usernameInputBox.on("input", function() {
    containsSpace(this.value)
});

passwordInputBox.on("input", function() {
    containsSpace(this.value)
});
