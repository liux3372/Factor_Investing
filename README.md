Selecting and back testing factor selection model in equity investing based on four factors. Two are value factors PB and PEG, two are growth factors the earnings growth and cash flow growth. 
Rebalancing every May, September and December. 

Procedures:
•	testing the validation of the four single factors

•	run double selection model which is in each sector to choose 6 stocks with the best factor values then choose 3 of the 6 with another factor value. The two factors should be in different categories (value+growth or growth+value)

•	Then pick the two set of factors with the best performance and do out of sample test

In sample test is from May 2005 to April 2014, the out of sample test is from May 2014 to August 2017. Stocks are selected from A-share stocks in China, factor values are from Wind database. 



%_selectionN.py (step1, select N stocks with the best factor values)
double_factors_selectionN.py (step2)
preparingData.py (For each rebalancing period, construct a folder with selected stocks.) 
backtesting_driver.py (run backtesting with given stocks in each rebalancing period)
backtesting_driver_with_timing_and_commision.py (run backtesting with a timing strategy to reduce variance and added commission fees for transaction costs)

 

