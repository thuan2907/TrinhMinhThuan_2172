import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests


BASE_URL = "http://127.0.0.1:5000/api/rsa"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    # ---------------- GENERATE KEYS ----------------
    def call_api_gen_keys(self):
        try:
            response = requests.get(f"{BASE_URL}/generate_keys")

            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "Success", data.get("message", "Done"))
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- ENCRYPT ----------------
    def call_api_encrypt(self):
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }

        try:
            response = requests.post(f"{BASE_URL}/encrypt", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data.get("encrypted_message", ""))

                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- DECRYPT ----------------
    def call_api_decrypt(self):
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }

        try:
            response = requests.post(f"{BASE_URL}/decrypt", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data.get("decrypted_message", ""))

                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- SIGN ----------------
    def call_api_sign(self):
        payload = {
            "message": self.ui.txt_info.toPlainText()
        }

        try:
            response = requests.post(f"{BASE_URL}/sign", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data.get("signature", ""))

                QMessageBox.information(self, "Success", "Signed Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- VERIFY ----------------
    def call_api_verify(self):
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }

        try:
            response = requests.post(f"{BASE_URL}/verify", json=payload)

            if response.status_code == 200:
                data = response.json()

                if data.get("is_verified"):
                    QMessageBox.information(self, "Success", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Fail", "Verification Failed")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())