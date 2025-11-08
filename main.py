import pygsheets
import tkinter as tk
from tkinter import messagebox
import re
import datetime
import threading
import os
from dotenv import load_dotenv

class Registration:
    def __init__(self) -> None:
        load_dotenv()
        service_account_file = os.getenv("SERVICE_ACCOUNT_FILE")
        reg_sheet_url = os.getenv("REG_SHEET_URL")
        checkin_sheet_url = os.getenv("CHECKIN_SHEET_URL")
        gc = pygsheets.authorize(service_account_file=service_account_file)
        reg = gc.open_by_url(reg_sheet_url)
        chk = gc.open_by_url(checkin_sheet_url)
        self.sheet = reg.sheet1
        self.check_in_sheet = chk.sheet1
        self._reg_cache = None
        self._checkin_cache = None

    def refresh_cache(self):
        # Only fetch necessary columns for phone lookup and check-in
        self._reg_cache = self.sheet.get_all_values(returnas='matrix')
        self._checkin_cache = self.check_in_sheet.get_all_values(returnas='matrix')

    def get_row_by_phone(self, phone):
        # Clean phone number: remove non-digits
        cleaned_phone = re.sub(r"\D", "", phone)
        if self._reg_cache is None:
            self.refresh_cache()
        for row in self._reg_cache:
            row_phone = re.sub(r"\D", "", row[7][2:] if row[7].startswith("+1") else row[7])
            if cleaned_phone == row_phone:
                return row
        return None

    def check_in(self, row):
        # Prevent duplicate check-ins by searching for phone number in check-in sheet
        phone = re.sub(r"\D", "", row[7])
        if self._checkin_cache is None:
            self.refresh_cache()
        for existing in self._checkin_cache:
            existing_phone = re.sub(r"\D", "", existing[7])
            if phone == existing_phone:
                messagebox.showwarning("Already Checked In", f"{row[1]} {row[2]} is already checked in!")
                return False
        self.check_in_sheet.insert_rows(self.check_in_sheet.rows, values=[row], inherit=True)
        # Update cache after insert
        self.refresh_cache()
        print(row)
        print(f"inserted {row[0]} {row[1]}")
        return True

# GUI setup
window = tk.Tk()
window.geometry("700x400")
window.title("TigerHacks Check-In")
window.configure(bg="#f0f4f8")

reg_form = Registration()

instructions = tk.Label(window, text="Enter phone number:", font=("Arial", 14), bg="#f0f4f8")
instructions.pack(pady=(20, 5))

phonebox = tk.Entry(window, font=("Arial", 12), width=30)
phonebox.pack(pady=5)

user_frame = tk.Frame(window, bg="#f0f4f8", bd=2, relief=tk.GROOVE)

def search():
    def do_search():
        phone = phonebox.get().strip()
        if not phone:
            messagebox.showwarning("Input Error", "Please enter a phone number.")
            return
        # Clean phone number for validation
        cleaned_phone = re.sub(r"\D", "", phone)
        if len(cleaned_phone) < 10:
            messagebox.showwarning("Input Error", "Invalid phone format. Please enter a valid phone number.")
            return
        response = reg_form.get_row_by_phone(phone)
        for widget in user_frame.winfo_children():
            widget.destroy()
        if response is None:
            messagebox.showwarning("Not Found", "Phone number not registered!")
            return
        tk.Label(user_frame, text=f"{response[1]} {response[2]}", font=("Arial", 13, "bold"), bg="#f0f4f8").pack(pady=5)
        tk.Label(user_frame, text=f"Shirt Size: {response[13]}", font=("Arial", 12), bg="#f0f4f8").pack(pady=2)
        tk.Label(user_frame, text="Dietary restrictions:", font=("Arial", 12), bg="#f0f4f8").pack(pady=2)
        dietary_restrictions = tk.Entry(user_frame, font=("Arial", 12), width=30)
        dietary_restrictions.insert(0, response[14])
        dietary_restrictions.pack(pady=2)

        def submit():
            response[22] = str(datetime.datetime.now())
            response[14] = dietary_restrictions.get()
            success = reg_form.check_in(response[:25])
            if success:
                messagebox.showinfo("Success", f"Successfully checked in {response[1]} {response[2]}")
                phonebox.delete(0, tk.END)
                for widget in user_frame.winfo_children():
                    widget.destroy()

        submit_button = tk.Button(user_frame, text="Submit!", command=submit, font=("Arial", 12), bg="#4caf50", fg="white")
        submit_button.pack(pady=10)

    threading.Thread(target=do_search).start()

search_button = tk.Button(window, text="Search", command=search, font=("Arial", 12), bg="#2196f3", fg="white")
search_button.pack(pady=10)
user_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Bind Enter key to trigger search
window.bind('<Return>', lambda event: search())

window.mainloop()