# -*- coding: utf-8 -*-
# Generated from rsa.ui using pyuic5
# WARNING: Any manual changes made here will be lost!

import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = "../platforms"

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 480)
        MainWindow.setWindowTitle("RSA Cipher")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ---------- Title Label ----------
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(QtCore.QRect(0, 10, 720, 40))
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        font_title = QtGui.QFont()
        font_title.setPointSize(16)
        font_title.setBold(True)
        self.lbl_title.setFont(font_title)
        self.lbl_title.setText("RSA CIPHER")
        self.lbl_title.setObjectName("lbl_title")

        # ---------- Generate Keys Button ----------
        self.btn_gen_keys = QtWidgets.QPushButton(self.centralwidget)
        self.btn_gen_keys.setGeometry(QtCore.QRect(580, 15, 120, 30))
        self.btn_gen_keys.setText("Generate Keys")
        self.btn_gen_keys.setObjectName("btn_gen_keys")

        # ---------- Plain Text ----------
        self.lbl_plain_text = QtWidgets.QLabel(self.centralwidget)
        self.lbl_plain_text.setGeometry(QtCore.QRect(20, 60, 100, 20))
        self.lbl_plain_text.setText("Plain Text:")
        self.lbl_plain_text.setObjectName("lbl_plain_text")

        self.txt_plain_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_plain_text.setGeometry(QtCore.QRect(20, 80, 330, 100))
        self.txt_plain_text.setObjectName("txt_plain_text")

        # ---------- Information ----------
        self.lbl_info = QtWidgets.QLabel(self.centralwidget)
        self.lbl_info.setGeometry(QtCore.QRect(370, 60, 100, 20))
        self.lbl_info.setText("Information:")
        self.lbl_info.setObjectName("lbl_info")

        self.txt_info = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_info.setGeometry(QtCore.QRect(370, 80, 330, 100))
        self.txt_info.setObjectName("txt_info")

        # ---------- Cipher Text ----------
        self.lbl_cipher_text = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cipher_text.setGeometry(QtCore.QRect(20, 195, 100, 20))
        self.lbl_cipher_text.setText("CipherText:")
        self.lbl_cipher_text.setObjectName("lbl_cipher_text")

        self.txt_cipher_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_cipher_text.setGeometry(QtCore.QRect(20, 215, 330, 100))
        self.txt_cipher_text.setObjectName("txt_cipher_text")

        # ---------- Signature ----------
        self.lbl_sign = QtWidgets.QLabel(self.centralwidget)
        self.lbl_sign.setGeometry(QtCore.QRect(370, 195, 100, 20))
        self.lbl_sign.setText("Signature:")
        self.lbl_sign.setObjectName("lbl_sign")

        self.txt_sign = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_sign.setGeometry(QtCore.QRect(370, 215, 330, 100))
        self.txt_sign.setObjectName("txt_sign")

        # ---------- Buttons Row ----------
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(60, 330, 100, 35))
        self.btn_encrypt.setText("Encrypt")
        self.btn_encrypt.setObjectName("btn_encrypt")

        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(200, 330, 100, 35))
        self.btn_decrypt.setText("Decrypt")
        self.btn_decrypt.setObjectName("btn_decrypt")

        self.btn_sign = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sign.setGeometry(QtCore.QRect(430, 330, 100, 35))
        self.btn_sign.setText("Sign")
        self.btn_sign.setObjectName("btn_sign")

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(570, 330, 100, 35))
        self.btn_verify.setText("Verify")
        self.btn_verify.setObjectName("btn_verify")

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
