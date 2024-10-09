import tkinter as tk
from tkinter import ttk

class SancharSaathiGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sanchar Saathi Form Filler")
        self.create_widgets()
        self.submit_callback = None

    def create_widgets(self):
        # Medium of Communication
        ttk.Label(self.master, text="Medium of Communication:").pack()
        self.medium_var = tk.StringVar()
        ttk.Combobox(self.master, textvariable=self.medium_var, values=["Call", "SMS", "WhatsApp"]).pack()

        # Fraud Category
        ttk.Label(self.master, text="Fraud Category:").pack()
        self.category_var = tk.StringVar()
        ttk.Combobox(self.master, textvariable=self.category_var, values=[
            "KYC related to Bank / Electricity / Gas / Insurance policy etc",
            "Impersonation as Government official / relative",
            "Fake Customer Care Helpline",
            "Online job / lottery /gifts/loan offers",
            "Sextortion",
            "Multiple automated / robo communication",
            "Malicious link / website",
            "Any Other Suspected Fraud"
        ]).pack()

        # Other fields
        fields = [
            ("Suspected Number", "suspected_number"),
            ("Date of Communication", "date"),
            ("Time of Communication", "time"),
            ("Complaint Details", "complaint_details"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Mobile Number", "mobile_number")
        ]

        self.entries = {}
        for label, field in fields:
            ttk.Label(self.master, text=label).pack()
            self.entries[field] = ttk.Entry(self.master)
            self.entries[field].pack()

        # SMS-specific fields
        ttk.Label(self.master, text="SMS CTA (if applicable):").pack()
        self.entries["sms_cta"] = ttk.Entry(self.master)
        self.entries["sms_cta"].pack()

        ttk.Label(self.master, text="SMS CTA URL (if applicable):").pack()
        self.entries["sms_cta_url"] = ttk.Entry(self.master)
        self.entries["sms_cta_url"].pack()

        # WhatsApp-specific fields
        ttk.Label(self.master, text="Suspected WhatsApp Number (if applicable):").pack()
        self.entries["suspected_whatsapp_number"] = ttk.Entry(self.master)
        self.entries["suspected_whatsapp_number"].pack()

        # Submit button
        ttk.Button(self.master, text="Fill Form", command=self.on_submit).pack()

    def set_submit_callback(self, callback):
        self.submit_callback = callback

    def on_submit(self):
        if self.submit_callback:
            data = {
                'medium': self.medium_var.get(),
                'category': self.category_var.get(),
                **{field: entry.get() for field, entry in self.entries.items()}
            }
            self.submit_callback(data)