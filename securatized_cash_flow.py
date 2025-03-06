import numpy as np
import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Step 1: Define cash flow calculation function
def calc_tranche_cf(balance, rate, term, def_rate, prepay_rate, tranche_size):
    monthly_rate = rate / 12
    payment = balance * monthly_rate / (1 - (1 + monthly_rate) ** -term)
    remaining = balance
    cf = []
    for t in range(1, term + 1):
        interest = remaining * monthly_rate
        principal = payment - interest
        prepay = remaining * prepay_rate
        default = remaining * def_rate
        total_principal = min(principal + prepay, remaining)
        remaining -= (total_principal + default)
        cf.append(min(total_principal + interest, tranche_size))
        if remaining <= 0:
            break
    return cf[:term] if len(cf) < term else cf

# Step 2: Define plotting and update logic
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
        cash_flows = calc_tranche_cf(bal, rt, trm, dr, pr, ts)
        months = np.arange(1, len(cash_flows) + 1)
        total_cf = sum(cash_flows)

        # Step 5: Update display labels
        lbl_tot.config(text=f"Total CF: ${total_cf:.2f}")
        lbl_avg.config(text=f"Avg CF: ${total_cf / len(cash_flows):.2f}")

        # Step 6: Generate and update plot
        ax.clear()
        ax.plot(months, cash_flows, color='#FF6B6B', lw=2, label='Cash Flow')
        ax.axhline(ts, color='#888888', ls='--', alpha=0.6, label=f'Tranche Size={ts}')
        ax.set_xlabel('Month', color='white')
        ax.set_ylabel('Cash Flow', color='white')
        ax.set_title('Tranche Cash Flow Waterfall', color='white')
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.5)
        ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
        ax.tick_params(colors='white')
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