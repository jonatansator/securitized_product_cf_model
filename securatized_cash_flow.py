import numpy as np
import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Step 1: Define cash flow calculation function (modified to return components)
def calc_tranche_cf(balance, rate, term, def_rate, prepay_rate, tranche_size):
    monthly_rate = rate / 12
    payment = balance * monthly_rate / (1 - (1 + monthly_rate) ** -term)
    remaining = balance
    cf_principal = []
    cf_interest = []
    for t in range(1, term + 1):
        interest = remaining * monthly_rate
        principal = payment - interest
        prepay = remaining * prepay_rate
        default = remaining * def_rate
        total_principal = min(principal + prepay, remaining)
        remaining -= (total_principal + default)
        total_cf = min(total_principal + interest, tranche_size)
        # Apportion principal and interest within the cap
        if total_cf < tranche_size:
            cf_principal.append(total_principal)
            cf_interest.append(interest)
        else:
            interest_fraction = interest / (total_principal + interest)
            cf_interest.append(tranche_size * interest_fraction)
            cf_principal.append(tranche_size * (1 - interest_fraction))
        if remaining <= 0:
            break
    # Pad with zeros if shorter than term
    cf_principal.extend([0] * (term - len(cf_principal)))
    cf_interest.extend([0] * (term - len(cf_interest)))
    return cf_principal[:term], cf_interest[:term]

# Step 2: Define plot
def refresh_output():
    try:
        bal = float(ent_bal.get())
        rt = float(ent_rt.get()) / 100
        trm = int(ent_trm.get())
        dr = float(ent_dr.get()) / 100
        pr = float(ent_pr.get()) / 100
        ts = float(ent_ts.get())

        # Step 3: Validate inputs
        if bal <= 0 or rt <= 0 or trm <= 0 or ts <= 0:
            raise ValueError("Balance, rate, term, and tranche size must be positive")
        if dr < 0 or pr < 0:
            raise ValueError("Default and prepayment rates cannot be negative")

        # Step 4: Compute cash flows
        cf_principal, cf_interest = calc_tranche_cf(bal, rt, trm, dr, pr, ts)
        months = np.arange(1, len(cf_principal) + 1)
        total_cf = sum(cf_principal) + sum(cf_interest)

        # Step 5: Update display labels
        lbl_tot.config(text=f"Total CF: ${total_cf:.2f}")
        lbl_avg.config(text=f"Avg CF: ${total_cf / len(cf_principal):.2f}")

        # Step 6: Generate plot
        ax.clear()
        ax.stackplot(months, cf_principal, cf_interest, labels=['Principal', 'Interest'],
                     colors=['#4ECDC4', '#45B7D1'], alpha=0.8)
        ax.axhline(ts, color='#FF6B6B', ls='--', lw=2, label=f'Tranche Size={ts}')
        ax.set_xlabel('Month', fontsize=12, color='white')
        ax.set_ylabel('Cash Flow ($)', fontsize=12, color='white')
        ax.set_title('Tranche Cash Flow Waterfall', fontsize=14, color='white', pad=10)
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.3)
        ax.legend(loc='upper right', facecolor='#333333', edgecolor='white', 
                  labelcolor='white', fontsize=10, framealpha=0.7)
        ax.tick_params(colors='white', labelsize=10)
        
        # Add annotation for tranche cap intersection (first point where total CF = tranche size)
        total_cf = np.array(cf_principal) + np.array(cf_interest)
        cap_idx = np.argmax(total_cf >= ts) if np.any(total_cf >= ts) else -1
        if cap_idx >= 0:
            ax.annotate(f'Cap at {ts:.0f}', xy=(months[cap_idx], ts), xytext=(months[cap_idx] + 10, ts + 500),
                        arrowprops=dict(facecolor='white', shrink=0.05, alpha=0.7),
                        color='white', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="#444444", ec="white", alpha=0.8))

        canv.draw()

    except ValueError as err:
        messagebox.showerror("Error", str(err))

# Step 7: Initialize GUI
win = tk.Tk()
win.title("Securitized Cash Flow Model")
win.configure(bg='#1E1E1E')

frm = ttk.Frame(win, padding=10)
frm.pack()
frm.configure(style='Dark.TFrame')

# Step 8: Set up plot
fig, ax = plt.subplots(figsize=(7, 5))
canv = FigureCanvasTkAgg(fig, master=frm)
canv.get_tk_widget().pack(side=tk.LEFT)

# Step 9: Create input panel
inp_frm = ttk.Frame(frm)
inp_frm.pack(side=tk.RIGHT, padx=10)
inp_frm.configure(style='Dark.TFrame')

# Step 10: Apply dark theme
style = ttk.Style()
style.theme_use('default')
style.configure('Dark.TFrame', background='#1E1E1E')
style.configure('Dark.TLabel', background='#1E1E1E', foreground='white')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#333333', foreground='white')

ttk.Label(inp_frm, text="Pool Balance ($):", style='Dark.TLabel').pack(pady=3)
ent_bal = ttk.Entry(inp_frm); ent_bal.pack(pady=3); ent_bal.insert(0, "1000000")
ttk.Label(inp_frm, text="Rate (%):", style='Dark.TLabel').pack(pady=3)
ent_rt = ttk.Entry(inp_frm); ent_rt.pack(pady=3); ent_rt.insert(0, "5")
ttk.Label(inp_frm, text="Term (months):", style='Dark.TLabel').pack(pady=3)
ent_trm = ttk.Entry(inp_frm); ent_trm.pack(pady=3); ent_trm.insert(0, "360")
ttk.Label(inp_frm, text="Default Rate (%):", style='Dark.TLabel').pack(pady=3)
ent_dr = ttk.Entry(inp_frm); ent_dr.pack(pady=3); ent_dr.insert(0, "1")
ttk.Label(inp_frm, text="Prepay Rate (%):", style='Dark.TLabel').pack(pady=3)
ent_pr = ttk.Entry(inp_frm); ent_pr.pack(pady=3); ent_pr.insert(0, "2")
ttk.Label(inp_frm, text="Tranche Size ($):", style='Dark.TLabel').pack(pady=3)
ent_ts = ttk.Entry(inp_frm); ent_ts.pack(pady=3); ent_ts.insert(0, "5000")

ttk.Button(inp_frm, text="Calculate", command=refresh_output).pack(pady=10)

lbl_tot = ttk.Label(inp_frm, text="Total CF: ", style='Dark.TLabel'); lbl_tot.pack(pady=2)
lbl_avg = ttk.Label(inp_frm, text="Avg CF: ", style='Dark.TLabel'); lbl_avg.pack(pady=2)

# Step 11: Initial run and start GUI
refresh_output()
win.mainloop()
