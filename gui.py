import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class SancharSaathiGUI:
    def __init__(self, master, submit_callback):
        self.master = master
        self.master.title("Sanchar Saathi Form Filler")
        self.submit_callback = submit_callback
        self.create_widgets()

    def create_widgets(self):
        # Initialize the entries dictionary
        self.entries = {}
        self.entries = {}

        # Medium of Communication
        ttk.Label(self.master, text="Medium of Communication:").pack()
        self.medium_var = tk.StringVar()
        self.medium_combo = ttk.Combobox(self.master, textvariable=self.medium_var, values=["Call", "SMS", "WhatsApp"])
        self.medium_combo.pack()
        self.medium_combo.bind("<<ComboboxSelected>>", self.on_medium_change)
        self.medium_combo.bind("<<ComboboxSelected>>", self.on_medium_change)

        # Fraud Category
        ttk.Label(self.master, text="Fraud Category:").pack()
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(self.master, textvariable=self.category_var, values=[
            "KYC related to Bank / Electricity / Gas / Insurance policy etc",
            "Impersonation as Government official / relative",
            "Fake Customer Care Helpline",
            "Online job / lottery /gifts/loan offers",
            "Sextortion",
            "Multiple automated / robo communication",
            "Malicious link / website",
            "Any Other Suspected Fraud"
        ])
        self.category_combo.pack()
        self.category_combo.pack()

        # SMS-specific fields
        self.sms_frame = ttk.Frame(self.master)
        self.sms_type_var = tk.StringVar(value="without_header")
        ttk.Radiobutton(self.sms_frame, text="Without Header", variable=self.sms_type_var, value="without_header").pack()
        ttk.Radiobutton(self.sms_frame, text="With Header", variable=self.sms_type_var, value="with_header").pack()
        ttk.Label(self.sms_frame, text="Suspected Number/Header:").pack()
        self.entries["sms_suspected_number"] = ttk.Entry(self.sms_frame)
        self.entries["sms_suspected_header"] = ttk.Entry(self.sms_frame)
        self.entries["sms_suspected_number"].pack()
        self.entries["sms_suspected_header"].pack()
        ttk.Label(self.sms_frame, text="SMS CTA:").pack()
        self.entries["sms_cta"] = ttk.Entry(self.sms_frame)
        self.entries["sms_cta"].pack()
        ttk.Label(self.sms_frame, text="SMS CTA URL:").pack()
        self.entries["sms_cta_url"] = ttk.Entry(self.sms_frame)
        self.entries["sms_cta_url"].pack()
        self.entries["sms_suspected_number"].bind('<FocusIn>', self.on_entry_click)

        # WhatsApp-specific fields
        self.whatsapp_frame = ttk.Frame(self.master)
        ttk.Label(self.whatsapp_frame, text="Suspected WhatsApp Number:").pack()
        self.entries["suspected_whatsapp_number"] = ttk.Entry(self.whatsapp_frame)
        self.entries["suspected_whatsapp_number"].pack()
        self.whatsapp_type_var = tk.StringVar(value="call")
        ttk.Radiobutton(self.whatsapp_frame, text="Call", variable=self.whatsapp_type_var, value="call").pack()
        ttk.Radiobutton(self.whatsapp_frame, text="Text", variable=self.whatsapp_type_var, value="text").pack()
        self.entries["sms_cta"] = ttk.Entry(self.sms_frame)

        # Other fields
        fields = [
         
            ("Complaint Details", "complaint_details"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Mobile Number", "mobile_number")
        ]
        self.entries["suspected_whatsapp_number"] = ttk.Entry(self.whatsapp_frame)
        for label, field in fields:
            ttk.Label(self.master, text=label).pack()
            if field == "date":
                self.entries[field] = DateEntry(self.master, width=12, background='darkblue')
            else:
                self.entries[field] = ttk.Entry(self.master)
            self.entries[field].pack()
            ("First Name", "first_name"),

        # Add these new fields
        ttk.Label(self.master, text="Date:").pack()
        self.entries["date"] = DateEntry(self.master, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entries["date"].pack()

        ttk.Label(self.master, text="Time:").pack()
        self.entries["time"] = ttk.Entry(self.master)
        self.entries["time"].pack()

        # Submit button
        ttk.Button(self.master, text="Fill Form", command=self.on_submit).pack()
        

    def on_medium_change(self, event):
        medium = self.medium_var.get()
        self.sms_frame.pack_forget()
        self.whatsapp_frame.pack_forget()
        if medium == "SMS":
            self.sms_frame.pack()
        elif medium == "WhatsApp":
            self.whatsapp_frame.pack()

    def on_submit(self):
        if self.submit_callback:
            data = {
                'medium': self.medium_var.get(),
                'category': self.category_var.get(),
                'sms_type': self.sms_type_var.get(),
                'whatsapp_type': self.whatsapp_type_var.get(),
                **{field: entry.get() for field, entry in self.entries.items() if field != "date"},
                'date': self.entries["date"].get_date().strftime('%Y-%m-%d'),
                'time': self.entries["time"].get()
            }
            self.submit_callback(data)

    # Add this new method
    def on_entry_click(self, event):
        """Handle the entry click event"""
        # Clear the default text when the user clicks on the entry
        if event.widget.get() == 'Enter suspected number':
            event.widget.delete(0, "end")
            event.widget.config(fg='black')

    def get_form_data(self):
        form_data = {}
        for key, entry in self.entries.items():
            form_data[key] = entry.get()
        return form_data