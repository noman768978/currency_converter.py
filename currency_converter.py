import tkinter as tk
from tkinter import ttk, messagebox
from forex_python.converter import CurrencyRates
from datetime import datetime
import threading

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x600")
        
        # Initialize currency converter
        self.c = CurrencyRates()
        
        # Common currencies
        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY",
            "INR", "NZD", "BRL", "MXN", "SEK", "SGD", "HKD"
        ]
        
        # Variables
        self.amount_var = tk.StringVar(value="1.00")
        self.from_currency_var = tk.StringVar(value="USD")
        self.to_currency_var = tk.StringVar(value="EUR")
        self.result_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        ttk.Label(
            self.root,
            text="Currency Converter",
            font=("Arial", 16)
        ).pack(pady=20)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Amount entry
        amount_frame = ttk.LabelFrame(main_frame, text="Amount")
        amount_frame.pack(pady=10, fill="x")
        
        ttk.Entry(
            amount_frame,
            textvariable=self.amount_var,
            justify="center",
            font=("Arial", 12)
        ).pack(pady=5, padx=5, fill="x")
        
        # Currency selection
        currency_frame = ttk.LabelFrame(main_frame, text="Select Currencies")
        currency_frame.pack(pady=10, fill="x")
        
        # From currency
        from_frame = ttk.Frame(currency_frame)
        from_frame.pack(pady=5, fill="x")
        
        ttk.Label(from_frame, text="From:").pack(side="left", padx=5)
        ttk.Combobox(
            from_frame,
            textvariable=self.from_currency_var,
            values=self.currencies,
            state="readonly"
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # To currency
        to_frame = ttk.Frame(currency_frame)
        to_frame.pack(pady=5, fill="x")
        
        ttk.Label(to_frame, text="To:").pack(side="left", padx=5)
        ttk.Combobox(
            to_frame,
            textvariable=self.to_currency_var,
            values=self.currencies,
            state="readonly"
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Swap button
        ttk.Button(
            currency_frame,
            text="⇅ Swap Currencies",
            command=self.swap_currencies
        ).pack(pady=5)
        
        # Convert button
        ttk.Button(
            main_frame,
            text="Convert",
            command=self.start_conversion
        ).pack(pady=20)
        
        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Result")
        result_frame.pack(pady=10, fill="x")
        
        ttk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 14),
            justify="center"
        ).pack(pady=10)
        
        # Rate info
        self.rate_label = ttk.Label(result_frame, text="")
        self.rate_label.pack(pady=5)
        
        # Status bar
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def swap_currencies(self):
        from_curr = self.from_currency_var.get()
        to_curr = self.to_currency_var.get()
        self.from_currency_var.set(to_curr)
        self.to_currency_var.set(from_curr)
        if self.result_var.get():  # If there's a result, convert again
            self.start_conversion()
            
    def start_conversion(self):
        # Start conversion in a separate thread to keep UI responsive
        threading.Thread(target=self.convert_currency, daemon=True).start()
        
    def convert_currency(self):
        try:
            # Update status
            self.status_var.set("Converting...")
            self.result_var.set("")
            self.rate_label.config(text="")
            self.root.update()
            
            # Get values
            amount = float(self.amount_var.get())
            from_curr = self.from_currency_var.get()
            to_curr = self.to_currency_var.get()
            
            # Get conversion rate
            rate = self.c.get_rate(from_curr, to_curr)
            result = self.c.convert(from_curr, to_curr, amount)
            
            # Update result
            self.result_var.set(f"{result:.2f} {to_curr}")
            self.rate_label.config(
                text=f"1 {from_curr} = {rate:.4f} {to_curr}\n"
                     f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            self.status_var.set("Ready")
            
        except ValueError:
            self.status_var.set("Error")
            messagebox.showerror("Error", "Please enter a valid number!")
        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    converter = CurrencyConverter(root)
    root.mainloop() 
