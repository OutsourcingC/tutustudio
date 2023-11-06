
const plaintext = "Hello, World!";

// 生成随机IV
const iv = CryptoJS.lib.WordArray.random(16); // 16字节的IV

// 密钥（需要与后端相同）
const key = CryptoJS.lib.WordArray.random(32); // 32字节密钥

// 加密
const ciphertext = CryptoJS.AES.encrypt(plaintext, key, {
  iv: iv,
}).toString();

// 将IV和密文一起发送到后端
const encryptedData = {
  iv: iv.toString(CryptoJS.enc.Base64),
  key: key.toString(CryptoJS.enc.Base64),
  ciphertext: ciphertext,
};

console.log(encryptedData)
// 发送encryptedData到后端
