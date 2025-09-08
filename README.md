# PERFORMANCE ANALYSIS OF THE ENGULFING AND RSI STRATEGY, USING STREAMLIT 
A Streamlit-based application for backtesting trading strategies, providing a bird's-eye view of performance metrics, trade outcomes, and risk management insights. The strategy is the combination of ENGULFING price pattern, and the RSI indicator. This is a personal project undertaken to have a bird's-eye view of the performance of this strategy using just a link. A little disclaimer- the strategy code is hosted on the Streamlit Cloud (free), which can be extremely slow to load. An alternative option is the Heroku cloud- a paid and faster option.


<img width="1918" height="968" alt="image" src="https://github.com/user-attachments/assets/3dbd8fcb-af57-4e83-b336-875c21bc1261" />




## 1. Project Overview
This project implements an interactive backtesting dashboard for analyzing trading strategies. 
It enables traders and analysts to:
- Backtest strategies on historical data
- Visualize performance and risk metrics in real time
- Explore trade-by-trade analysis through an interactive Streamlit app

---

## 2. Motivation
Backtesting is essential for validating trading strategies before deploying them in live markets. 
However, running tests in static notebooks makes it difficult to quickly explore results, compare strategies, 
or adjust parameters interactively.  
This project solves that by creating a **user-friendly dashboard** that gives a high-level and detailed view of backtest results.

---

## 3. Features
- 📈 Interactive charts of currency curves, drawdowns, and returns
- ⚖️ Risk management metrics (Sharpe ratio, max drawdown)
- 🔎 Trade-by-trade analysis table (an exhaustive downloadable CSV file of trade result)
- ⚙️ User inputs to adjust risk amount per trade, currency, and RSI levels
- 📊 Summary statistics panel for quick insights
- 🖥️ Built entirely with **Streamlit** for ease of use
- 
<img width="1919" height="888" alt="image" src="https://github.com/user-attachments/assets/e261e6f7-8eea-4251-926d-27fe8b019452" />

<img width="1911" height="907" alt="image" src="https://github.com/user-attachments/assets/a6304270-2c6e-4cf6-a0de-347c02048d14" />




---

## 4. Methodology
1. Load historical asset price data (Forex).  
2. Apply the selected trading strategy with configurable parameters.  
3. Compute key metrics:
   - Annualized return
   - Sharpe ratio
   - Maximum drawdown
   - Win/loss rate  
4. Display results interactively through Streamlit components.

5. The link to the dashboard on streamlit is: https://backtest-analysis-1.streamlit.app/


---


## How to Run
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the app: `streamlit run app.py`.
