# Projects Portfolio

## Project 1 - [Monte Carlo Risk Model](https://github.com/sjfollett/portfolio/tree/main/monte_carlo)
- Utilizes pandas datareader to gather stock data 
- Looking at daily close price, calulates average daily move & standard deviation of average daily move
- Applies a random walk starting at current price and then applying a random variable to average daily move and standard deviation
- Scalable timeframes and number of simulations 
- Aggregates results from multiple random walks and visualizes the result 

![](https://github.com/sjfollett/portfolio/blob/main/images/Spy%2060%20Day%20Outlook.png?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/Spy%20Outlook%20v%20Actual.png?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/Spy%20Monte%20Carlo%201.png?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/Spy%20Histogram.png?raw=true)

## Project 2 - Linear Regression 
- Examined relationship between Oil price and USD/RUB FX conversion price
- Trained model on 2014-2016 data 
- Regressed on 2016-2018 data utilizing Sk_learn Package & calculated R2 
- Visualized result

![](https://github.com/sjfollett/portfolio/blob/main/images/Oil%20to%20Rubles.png?raw=true)

## Project 3 - Logistic Regression (Classification Alogrithm)
- Looked at portfolio of 150k loan applications to determine which items on the loan application are most sensitive to determinig default
- Found the best correlated indicators and assigned weights to them 
- Ran logisitc regression with 70/30 test train split 
- Analyzed results 

![](https://github.com/sjfollett/portfolio/blob/main/images/Logisitic%20Regression.JPG)
![](https://github.com/sjfollett/portfolio/blob/main/images/Correlation%20Matrix.JPG)

## Project 4 - CAPM and Efficient Frontier 
- Analyzed Monthly return data of AAPL, PG, GE, SPY and T-Bills
- Built 10 simulated portfolios utilizing various weights 
- Utilized data analysis toolpack to create covariance matrix and find efficient protfoilios using excel solver
- Made linear combinations of efficient portfolios to graph the efficient frontier
- Utilized risk free rate and sharpe ratio to graph tangent line
- Regressed beta 
- Utilized CAPM to create CML and see which portfolios were overvalued/undervalued for their level of risk and return

![](https://github.com/sjfollett/portfolio/blob/main/images/EffecientFrontier.JPG?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/Beta%20Regression.JPG?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/SML.JPG?raw=true)

## Project 5 - 3 Financial Statement Model
- Created 3 Financial Statement Excel Model for restaurant franchise 
- Account roll-ups from individual stores to enterprise level
- Forecasted sales & expense growth for 5 years 
- Linked entire spreasheed to one inputs tab for assumptions
- Aggregate sheets are linked to individual store sheets 

![](https://github.com/sjfollett/portfolio/blob/main/images/P%26L.JPG)
![](https://github.com/sjfollett/portfolio/blob/main/images/Balance%20Sheet.JPG)
![](https://github.com/sjfollett/portfolio/blob/main/images/CashFlow.JPG)

## Project 6 - Kellog Valuation
- Analyzed 10k to divide balance sheet and income statement items into operating and financing items
- Caluculated NOPAT and NOA 
- Grossed up balance sheet 
- Adjusted for Stock Based Compensation overhang and Capital Leases
- Created common sized income statement and balance sheets
- Estimated WACC 
- Applied DCF, ROPI and Abnormal Income Growth models to fundamentally value company
- Adjusted for date of valuation

![](https://github.com/sjfollett/portfolio/blob/main/images/DCF.JPG?raw=true)

## Project 7 - SQLite Database Manager 
- Created SQLite database browser in python
- Perform basic CRUD (create, read, update, delete) operations through python function  
- Utilized principles of object oriented programming to create a simple family tree structure that can be managed via the database browser 

![](https://github.com/sjfollett/portfolio/blob/main/images/Database%20browser.JPG)

## Project 8 - AZDPS Web Scraper 
- Utilized Selenium python package to automate process of checking employees & potential employees criminal record with local Police Department for a pre-school with 15 employees
- Exports results to pre school owners and facilitates compliance with inspections for business 

## Project 9 - PyBaseball Pitching Charts 
- Retrived statcast data and visualized time-series results for pitchers in python 
- Manipulated data to show horizontal and vertical movement by pitch type

![](https://github.com/sjfollett/portfolio/blob/main/images/Mayers2020.png?raw=true)
![](https://github.com/sjfollett/portfolio/blob/main/images/Mayers2021.png?raw=true)
