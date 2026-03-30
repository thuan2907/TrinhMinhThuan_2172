import customtkinter as ctk
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import datetime
import hashlib
from tkinter import messagebox

# Cấu hình chủ đề
ctk.set_appearance_mode("dark")  # Chế độ tối
ctk.set_default_color_theme("blue") # Tông màu xanh dương hiện đại

# ==================== CRYPTO FUNCTIONS ====================
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# ==================== MODERN GUI APPLICATION ====================
class ModernChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SecureChat Pro - AES/RSA")
        self.geometry("1000x700")

        # Khởi tạo biến
        self.client_socket = None
        self.aes_key = None
        self.connected = False

        # Chia bố cục chính thành 2 cột: Sidebar và Chat Area
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_chat_area()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo/Title
        self.logo = ctk.CTkLabel(self.sidebar, text="🔒 SECURE MSG", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(pady=(30, 20))

        # Nhập liệu kết nối
        self.name_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Tên hiển thị", width=220)
        self.name_entry.insert(0, "User_1")
        self.name_entry.pack(pady=10)

        self.host_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Server IP", width=220)
        self.host_entry.insert(0, "localhost")
        self.host_entry.pack(pady=10)

        self.port_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Port", width=220)
        self.port_entry.insert(0, "12345")
        self.port_entry.pack(pady=10)

        self.connect_btn = ctk.CTkButton(self.sidebar, text="Kết nối ngay", command=self.toggle_connection, 
                                        fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(weight="bold"))
        self.connect_btn.pack(pady=20)

        # Panel thông tin khóa (Crypto Info)
        self.info_label = ctk.CTkLabel(self.sidebar, text="THÔNG SỐ MÃ HÓA", font=ctk.CTkFont(size=12, weight="bold"))
        self.info_label.pack(pady=(20, 5))
        
        self.key_box = ctk.CTkTextbox(self.sidebar, width=240, height=150, font=("Consolas", 10), 
                                      fg_color="#1e1e1e", border_width=1)
        self.key_box.pack(padx=20, pady=10)
        self.key_box.configure(state="disabled")

        self.status_indicator = ctk.CTkLabel(self.sidebar, text="● Chưa kết nối", text_color="gray")
        self.status_indicator.pack(side="bottom", pady=20)

    def _build_chat_area(self):
        self.chat_main = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.chat_main.grid_rowconfigure(0, weight=1)
        self.chat_main.grid_columnconfigure(0, weight=1)

        # Khung hiển thị chat
        self.chat_display = ctk.CTkTextbox(self.chat_main, font=("Segoe UI", 14), corner_radius=15, 
                                           border_width=2, border_color="#333")
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 20))
        self.chat_display.configure(state="disabled")

        # Khung nhập tin nhắn
        self.input_frame = ctk.CTkFrame(self.chat_main, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.msg_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Nhập nội dung bảo mật...", 
                                      height=50, corner_radius=10)
        self.msg_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_frame, text="GỬI", width=100, height=50, 
                                      corner_radius=10, command=self.send_message)
        self.send_btn.grid(row=0, column=1)

    # ---- LOGIC PHẦN MỀM ----

    def toggle_connection(self):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username = self.name_entry.get()

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))

            # RSA Handshake
            self.append_sys_msg("🔄 Đang thiết lập kênh bảo mật RSA...")
            client_key = RSA.generate(2048)
            server_pub = RSA.import_key(self.client_socket.recv(2048))
            self.client_socket.send(client_key.publickey().export_key())

            enc_aes_key = self.client_socket.recv(2048)
            self.aes_key = PKCS1_OAEP.new(client_key).decrypt(enc_aes_key)

            # Cập nhật UI
            self.connected = True
            self.update_ui_state(True, username)
            self.update_key_info(client_key, self.aes_key)
            
            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.append_sys_msg(f"✅ Đã kết nối an toàn. Chào {username}!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Kết nối thất bại: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        self.update_ui_state(False)
        self.append_sys_msg("🔌 Đã ngắt kết nối.")

    def update_ui_state(self, connected, user=""):
        if connected:
            self.status_indicator.configure(text=f"● Trực tuyến ({user})", text_color="#2ecc71")
            self.connect_btn.configure(text="Ngắt kết nối", fg_color="#e74c3c", hover_color="#c0392b")
        else:
            self.status_indicator.configure(text="● Chưa kết nối", text_color="gray")
            self.connect_btn.configure(text="Kết nối ngay", fg_color="#2ecc71", hover_color="#27ae60")

    def update_key_info(self, rsa_key, aes_key):
        rsa_hash = hashlib.sha256(rsa_key.publickey().export_key()).hexdigest()[:20]
        self.key_box.configure(state="normal")
        self.key_box.delete("1.0", "end")
        self.key_box.insert("end", f"AES-128 Key:\n{aes_key.hex()}\n\nRSA Fingerprint:\n{rsa_hash}...\n\nProtocol: CBC/PKCS7")
        self.key_box.configure(state="disabled")

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg and self.connected:
            encrypted = encrypt_message(self.aes_key, msg)
            self.client_socket.send(encrypted)
            self.append_chat_msg("Bạn", msg, "#3498db")
            self.msg_entry.delete(0, "end")

    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024)
                if not data: break
                decrypted = decrypt_message(self.aes_key, data)
                self.append_chat_msg("Đối phương", decrypted, "#2ecc71")
            except: break

    def append_chat_msg(self, sender, text, color):
        self.chat_display.configure(state="normal")
        time_now = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert("end", f"[{time_now}] ", "time")
        self.chat_display.insert("end", f"{sender}: ", "sender")
        self.chat_display.insert("end", f"{text}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def append_sys_msg(self, text):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"System: {text}\n", "sys")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    app = ModernChatApp()
    app.mainloop()