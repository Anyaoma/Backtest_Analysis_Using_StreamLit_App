FEATURES

Signal Application: Apply trading signals (BUY, SELL, NONE) to historical Forex data.

Risk Management: Calculate position sizes based on risk percentage and stop-loss levels.

Trade Simulation: Simulate trades with take-profit and stop-loss levels.

Performance Metrics: Track realized and unrealized PnL, account balance, and returns.

Flexible Strategy Testing: Easily integrate custom trading strategies.


CODE STRUCTURE: The code is organized into the following components:

Signal Application:Functions like apply_takeprofit, apply_gain, apply_loss, and apply_stoploss calculate take-profit, stop-loss, and position sizing based on trading signals.

Trade Class:The Trade class represents a single trade, tracking its status (open/closed), PnL, and execution details.

GuruTester Class:The GuruTester class is the core of the backtesting framework. It:Prepares data for backtesting and Simulates trades based on signals.



DATA PREPARATION

Functions like apply_signal_hour and create_changes preprocess the data and generate trading signals.


CONTRIBUTION
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


LICENSE
This project is licensed under the MIT License. See the LICENSE file for details.


CONTACT
For questions or feedback, please contact [Gift Anyaoma] at [anyaomagiftndidi@gmail.com].
