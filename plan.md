

Get data from NSE site.
    from 1. NSEpy lib         2. NSEtools lib

Generate plot and get buy and sell signal
    to plot:        plotly
    to visualize:   dash
    visualization and alalysis tools -> tools.py

Save output to file
    .csv / .json for later analysis

Apply machine learning to the data to predict future result
    Not sure how to do this




getdata.py -- will handle getting data from nse site
    ||
analysis.py -- wil do all the analysis and send data for rendering,and saves in csv/json file
    ||                                                                            ||
layout.py -- will handle rendering layout all the Dash thing           terminal.py -- will print to terminal
    ||
app.py -- will render the dash app




analysis.py
    doing all the analysis and returning a list of buy/sell advice
    save analyzed data in file
    make rendering data for layout.py
    todo:
        have to change basic functions of this file and redesign it. analyze function will analyze only one function,and return it. That will reduce unnecessary complexity of the porgram. To analyze all the stocks make different function.
app.py
    for now ready to use...good to go
    takes input from user and do callback according to the input
    todo:
        @app.callback have to shift to layout file
        fintering user input and showing suggestions

layout.py
    navbar is rendering from layout file
    dcc.Graph is rendering from layout file
    improve layout -- Done

    todo:
        dynmic rendring of graphs,those are herdcoded for now
        list buy/sell according to date,now it is in reverse order.
        add list of functions to apply on data
        plot buy sell data on graph

main.py
    gets data from nse site
    looks for upcoming dividend
    stores data in a file with dividend > 2
    gives terminal output of the data

test.py
    for testing purpose

getdata.py
    gets data from nse site and stores in a list of dataframe
    creates a output .csv file
    decide return type - list of dataframe
    todo:
        online functionality of getData function to be tasted
    coclusion:
        Ready for use at this point

tools.py
    plot MACD,RSI,SMA,EMA,Bollinger Bands,stock,Stochastic done
    analyze RSI,Stochastic done
    todo:
        add more indiactors
        add pattern
        analyze MACD
        return type of buy and sell signal
        customizing all the plots
        adding more types of indicators
        adding chart pattern
        find highly flactuating stocks (flactuation > 20%)
    conclusion:
        for now it is fully ready to use



tiralAndError.py
    for testing purpose

try.py
    for Dash testing purpose



NOTE: after extensive research can not understand why dataframe directly from site is not working whereas from csv file it is fine. Now going with file,but have to address it later.

have to implement database to store raw data and analyzed data.