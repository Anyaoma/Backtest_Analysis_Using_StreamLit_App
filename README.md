# PERFORMANCE ANALYSIS OF THE ENGULFING AND RSI STRATEGY, USING STREAMLIT 
A Streamlit-based application for backtesting trading strategies, providing a bird's-eye view of performance metrics, trade outcomes, and risk management insights. The strategy is the combination of ENGULFING price pattern, and the RSI indicator. This is a personal project undertaken to have a bird's-eye view of the performance of this strategy using just a link. A little disclaimer- the strategy code is hosted on the Streamlit Cloud (free), which can be extremely slow to load. An alternative option is the Heroku cloud- a paid and faster option.


![image](https://github.com/user-attachments/assets/5a58ff20-9111-4234-af27-531bb5927461)


## 1. PROJECT OVERVIEW
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

## On the interface, you can:

*Select any of the currencies that is a component of EUR_USD, GBP_JPY, GBP_USD

*Change the RSI components or levels

*Apply risk management by selecting the risk amount per trade

*Download the selected data as a CSV file

The link to the dashboard on streamlit is: https://backtestanalysis-n.streamlit.app/

## How to Run
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the app: `streamlit run app.py`.
