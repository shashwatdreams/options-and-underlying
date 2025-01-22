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


detailed_explanation = """
Options are financial instruments that give their holders the right, but not the obligation, to buy or sell a stock at a predetermined price, called the **strike price**, on or before a specified date. The value of an option is closely tied to the behavior of its underlying stock. This value depends on several factors, including the stock price, the strike price, the time left until the option expires, the stock's volatility, and the prevailing interest rates. Understanding how these factors interact can explain why options derive their value from the stock they are based on.

---

### Intrinsic Value

The first and most straightforward way options derive value is through **intrinsic value**, which depends on the relationship between the stock price and the strike price.

- For a **call option**, which is the right to buy the stock, the intrinsic value is the difference between the stock price and the strike price, if the stock price is higher. If the stock price is lower than the strike price, the option has no intrinsic value because it would be cheaper to buy the stock on the open market.
  - Example: If the stock price is \$120 and the strike price is \$100, the call option has an intrinsic value of \$20.
  
- For a **put option**, which is the right to sell the stock, the intrinsic value is the difference between the strike price and the stock price, if the stock price is lower. If the stock price is higher, the option has no intrinsic value because it would be better to sell the stock on the market.
  - Example: If the stock price is \$80 and the strike price is \$100, the put option has an intrinsic value of \$20.

Options with intrinsic value are called **in-the-money** options. Those without intrinsic value are **out-of-the-money**, and their price comes entirely from other factors.

---

### Time Value

Options have value beyond intrinsic value because of the potential for the stock price to move favorably before the option expires. This is called **time value**, and it reflects the uncertainty about where the stock price will go in the future. 

- A longer time to expiration increases the option’s time value because there is more time for the stock price to make a significant move.
- For example, if a stock is trading at $100 and a call option has a strike price of $110, the option might currently have no intrinsic value. However, if there are six months until expiration, the stock has time to rise above $110, giving the option potential future value.

As the expiration date approaches, the time value decreases because there is less opportunity for the stock price to move. This is known as **time decay** and accelerates as the option nears its expiration date. By expiration, the option’s value will be entirely based on its intrinsic value.

---

### Volatility

Another critical factor in determining an option’s value is **volatility**, which measures how much the stock price is expected to fluctuate over time. Higher volatility increases the value of an option because it means there is a greater chance of large price swings that could make the option profitable.

- For a call option, high volatility increases the likelihood that the stock price will rise well above the strike price.
- For a put option, high volatility increases the likelihood that the stock price will drop far below the strike price.

Even if the stock price is currently close to the strike price, higher volatility adds value to the option because it increases the range of possible outcomes. This is why options on more volatile stocks are generally more expensive than those on stable stocks.

---

### Risk-Free Rate

The **risk-free interest rate** is another factor that affects option prices. It represents the theoretical return on an investment with no risk, typically US treasury bonds. Since options involve cash flows in the future, interest rates affect their value.

- For call options, a higher interest rate increases the price. This is because the present value of the strike price is lower when interest rates are higher.
- For put options, a higher interest rate decreases the price. This is because the present value of receiving the strike price is lower with higher interest rates.

While interest rates have a smaller effect on options compared to other factors like stock price and volatility, they still play a role in determining their value.

---

### Probability

Options are probabilistic instruments, meaning their value reflects the likelihood that the stock price will move in a way that makes the option profitable. The Black-Scholes model and other pricing methods calculate the fair value of an option by estimating the probabilities of different outcomes. These probabilities are based on:
- The stock price relative to the strike price.
- The stock's volatility, which affects the range of possible price movements.
- The time remaining until expiration, which affects how much time the stock has to move.

For example:
- If a stock is trading at $95 and a call option has a strike price of $100, the option might still have value because there is a chance the stock price could rise above $100 before expiration.
- The further away the stock price is from the strike price, the lower the probability of the option being profitable, and thus the lower its value.

---

### Leverage

Options provide leverage, allowing investors to control more shares of a stock with less money than buying the stock outright. This amplifies the sensitivity of an option’s price to changes in the stock price. For example:
- If a stock’s price increases by 5%, the price of a call option might increase by 20 percent or more, depending on the option's characteristics.
- Similarly, a decrease in the stock price can cause a sharp drop in the price of the option.

This leverage makes options highly responsive to changes in the stock price, which is why the stock price is the most important factor in determining an option’s value.

---

Options derive their value from the underlying stock because their profitability depends entirely on how the stock price behaves relative to the strike price. Intrinsic value reflects the current profitability of exercising the option, while time value and volatility account for the potential for future price movements. Factors like interest rates and probability models further refine the option’s price to reflect real-world financial behavior. Together, these factors explain why options are such versatile and dynamic financial instruments, closely tied to the underlying stock price.
"""

st.markdown(detailed_explanation)

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
