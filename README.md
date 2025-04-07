# Streamlit App

This is a Streamlit app for displaying the backtest result of a combined ENGULFING and RSI strategy. This is a project that can be conducted on any strategy of choice. This is requested by clients who wants a bird eye view of the performance of their strategy using just a link. 
Disclaimer: The code is hosted on the streamlit cloud (free), which can be extremely slow to load. Upon request, the Heroku cloud can be used; a paid and faster option.

![image](https://github.com/user-attachments/assets/5a58ff20-9111-4234-af27-531bb5927461)



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
