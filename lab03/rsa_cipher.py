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

        self.ui.btnGeneratekeys.clicked.connect(self.call_api_gen_keys)
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btnSign.clicked.connect(self.call_api_sign)
        self.ui.btnVerify.clicked.connect(self.call_api_verify)

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
            "message": self.ui.txtPlaintext.toPlainText(),
            "key_type": "public"
        }

        try:
            response = requests.post(f"{BASE_URL}/encrypt", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txtCiphertext.setPlainText(data.get("encrypted_message", ""))

                QMessageBox.information(self, "Success", "Encrypted Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- DECRYPT ----------------
    def call_api_decrypt(self):
        payload = {
            "ciphertext": self.ui.txtCiphertext.toPlainText(),
            "key_type": "private"
        }

        try:
            response = requests.post(f"{BASE_URL}/decrypt", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txtPlaintext.setPlainText(data.get("decrypted_message", ""))

                QMessageBox.information(self, "Success", "Decrypted Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- SIGN ----------------
    def call_api_sign(self):
        payload = {
            "message": self.ui.txtInformation.toPlainText()
        }

        try:
            response = requests.post(f"{BASE_URL}/sign", json=payload)

            if response.status_code == 200:
                data = response.json()
                self.ui.txtSignature.setPlainText(data.get("signature", ""))

                QMessageBox.information(self, "Success", "Signed Successfully")
            else:
                print("Error:", response.status_code)
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error:", e)

    # ---------------- VERIFY ----------------
    def call_api_verify(self):
        payload = {
            "message": self.ui.txtInformation.toPlainText(),
            "signature": self.ui.txtSignature.toPlainText()
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