import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

st.title("How Option Prices Derive Their Value from the Underlying Stock Price")

# Sidebar for user inputs
st.sidebar.header("Model Parameters")
K = st.sidebar.slider("Strike Price (K)", 50, 150, 100)
T = st.sidebar.slider("Time to Maturity (T, in years)", 0.1, 2.0, 1.0, step=0.1)
r = st.sidebar.slider("Risk-Free Interest Rate (r, in %)", 0.0, 10.0, 5.0, step=0.1) / 100
sigma = st.sidebar.slider("Volatility (sigma, in %)", 10.0, 50.0, 20.0, step=0.1) / 100

S = np.linspace(50, 150, 100)
call_prices = [black_scholes(s, K, T, r, sigma, "call") for s in S]
put_prices = [black_scholes(s, K, T, r, sigma, "put") for s in S]

st.markdown("### Option Prices vs. Underlying Stock Price")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(S, call_prices, label="Call Option Price", linewidth=2)
ax.plot(S, put_prices, label="Put Option Price", linewidth=2)
ax.axvline(x=K, color='gray', linestyle='--', label="Strike Price")
ax.set_xlabel("Underlying Stock Price (S)")
ax.set_ylabel("Option Price")
ax.set_title("Option Prices vs. Underlying Stock Price (Black-Scholes Model)")
ax.legend()
ax.grid(True)
st.pyplot(fig)
