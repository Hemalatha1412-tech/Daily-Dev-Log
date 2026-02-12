import customtkinter as ctk
from tkinter import messagebox
import os
import pyperclip

# --- UI Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CyberVault(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CyberVault v4.0 | Direct Security")
        self.geometry("500x600")
        
        # Configuration
        self.shift = 7 
        self.vault_file = "secure_storage.txt"
        self.master_key = "admin123" 

        self.setup_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- Authentication Gate ---
    def setup_login_screen(self):
        self.clear_screen()
        self.header = ctk.CTkLabel(self, text="🛡️ VAULT LOCKED", font=("Fixedsys", 28, "bold"))
        self.header.pack(pady=(120, 20))
        self.login_entry = ctk.CTkEntry(self, placeholder_text="Master Password", show="*", width=300, height=45)
        self.login_entry.pack(pady=20)
        self.unlock_btn = ctk.CTkButton(self, text="UNLOCK", command=self.check_login, width=150, height=45)
        self.unlock_btn.pack(pady=10)

    def check_login(self):
        if self.login_entry.get() == self.master_key:
            self.setup_main_interface()
        else:
            messagebox.showerror("Denied", "Incorrect Master Password")

    # --- Main Dashboard ---
    def setup_main_interface(self):
        self.clear_screen()
        self.header = ctk.CTkLabel(self, text="🔐 CYBERVAULT", font=("Fixedsys", 28, "bold"))
        self.header.pack(pady=(30, 20))

        # Inputs
        self.acc_input = ctk.CTkEntry(self, placeholder_text="Platform Name", width=350, height=45)
        self.acc_input.pack(pady=15)

        self.pw_input = ctk.CTkEntry(self, placeholder_text="Your Password", width=350, height=45, show="*")
        self.pw_input.pack(pady=15)

        # Actions
        self.save_btn = ctk.CTkButton(self, text="ENCRYPT & SAVE", command=self.lock_data, 
                                     fg_color="#1f538d", width=350, height=50)
        self.save_btn.pack(pady=30)

        self.view_btn = ctk.CTkButton(self, text="VIEW SAVED PASSWORDS", command=self.view_vault, 
                                     fg_color="transparent", border_width=2, width=350)
        self.view_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Vault Ready", font=("Arial", 12), text_color="#45e68d")
        self.status_label.pack(side="bottom", pady=20)

    # --- Cryptography Logic ---
    def encrypt(self, data):
        return "".join(chr(ord(c) + self.shift) for c in data)

    def decrypt(self, data):
        return "".join(chr(ord(c) - self.shift) for c in data)

    def lock_data(self):
        platform = self.acc_input.get().strip()
        secret = self.pw_input.get().strip()
        if platform and secret:
            encrypted_secret = self.encrypt(secret)
            with open(self.vault_file, "a", encoding="utf-8") as f:
                f.write(f"{platform}|{encrypted_secret}\n")
            messagebox.showinfo("Success", f"Credentials for {platform} saved!")
            self.acc_input.delete(0, 'end')
            self.pw_input.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please fill both fields")

    def view_vault(self):
        if not os.path.exists(self.vault_file):
            messagebox.showinfo("Empty", "No data found.")
            return

        view_window = ctk.CTkToplevel(self)
        view_window.title("Stored Passwords")
        view_window.geometry("400x500")

        scroll_frame = ctk.CTkScrollableFrame(view_window, width=370, height=450)
        scroll_frame.pack(padx=10, pady=10)

        with open(self.vault_file, "r", encoding="utf-8") as f:
            for line in f:
                clean_line = line.strip()
                if "|" in clean_line:
                    platform, encrypted_val = clean_line.split("|")
                    
                    # Decrypt the value so the button can hold the 'real' password
                    plain_password = self.decrypt(encrypted_val)
                    
                    item_card = ctk.CTkFrame(scroll_frame)
                    item_card.pack(fill="x", pady=5)
                    
                    ctk.CTkLabel(item_card, text=f"📍 {platform}", font=("Arial", 13, "bold")).pack(pady=5, padx=10, anchor="w")
                    
                    # Copy button tied directly to the decrypted value
                    ctk.CTkButton(item_card, text="Copy Password", width=120,
                                  command=lambda p=plain_password: self.copy_to_clip(p)).pack(pady=5, padx=10, anchor="e")

    def copy_to_clip(self, p):
        pyperclip.copy(p)
        self.status_label.configure(text="Password copied to clipboard!", text_color="#5ea1ff")

if __name__ == "__main__":
    app = CyberVault()
    app.mainloop()