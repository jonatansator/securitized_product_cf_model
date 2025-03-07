# Securitized Product Cash Flow Model

- This project models cash flows for a tranche of securitized products (e.g., mortgage-backed securities), accounting for defaults and prepayments.
- It features an interactive GUI built with Tkinter to input parameters and visualize cash flow waterfalls in real-time.

---

## Files
- `securitized_cash_flow.py`: Main script for calculating tranche cash flows and displaying the GUI with a dynamic plot.
- `output.png`: Plot.

---

## Libraries Used
- `numpy`
- `pandas`
- `plotly` (imported but not used in this version; matplotlib used instead)
- `tkinter`
- `matplotlib`
- `matplotlib.backends.backend_tkagg`

---

## Features
- **Input**: User specifies pool balance, interest rate, term, default rate, prepayment rate, and tranche size via a GUI.
- **Cash Flow Calculation**: Computes monthly cash flows with adjustable default and prepayment rates, capped by tranche size.
- **Visualization**: Displays a real-time cash flow waterfall plot with tranche size reference line.
- **Metrics**: Shows total and average cash flows for the tranche.

