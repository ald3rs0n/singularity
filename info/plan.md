

1. Get data from NSE site.
    from 1. NSEpy lib         2. NSEtools lib

2. Generate plot and get buy and sell signal
    to plot:        plotly
    to visualize:   dash
    visualization and alalysis tools -> tools.py

3. Save output to database
    saving in mongo singularity database

4. Apply machine learning to the data to predict future result
    Not sure how to do this

## TODO:
    Multipage application
    Database connection
    ML application

###
    getdata.py -- will handle getting data from nse site
        ||
    analysis.py -- wil do all the analysis and send data for rendering,and saves in csv/json file
        ||                                                                            ||
    layout.py -- will handle rendering layout all the Dash thing           terminal.py -- will print to terminal
        ||
    app.py -- will render the dash app
###



# analysis.py
    doing all the analysis and returning a list of buy/sell advice
    save analyzed data in file
    make rendering data for layout.py
    have to change basic functions of this file and redesign it. analyze function will analyze only one function,and return it. That will reduce unnecessary complexity of the porgram. To analyze all the stocks make different function. --  Done
    doing analysis on all the dataframes and returing a list of dataframes
    todo:
        passing function as function argument ?
        Do all analysis on less data to improve speed

# index.py
    for now ready to use...good to go
    takes input from user and do callback according to the input
    @app.callback have to shift to layout file -- done
    todo:
        filtering user input and showing suggestions
        taking start_date and end_date argument from IU for SAT and VT functions


# app.py
    serve for the app
    todo:
        designing multi page
        app.py
        index.py
        pages/
            |->page1.py
            |->page2.py
        static/
        backend/
            |--getdata.py
            |--analysis.py
            |--tools.py
            |--dbconnect.py
        info/
            |--readme.md
            |--lisence
            |--plan.md

# layout.py
    navbar is rendering from layout file
    dcc.Graph is rendering from layout file
    improve layout -- Done
    list buy/sell according to date,now it is in reverse order. -- done
    dynmic rendring of graphs,those are hardcoded for now -- done
    colors of figure and legends -- done
    plot buy sell data point on candlestick graph  -- done

    todo:
        add list of functions to apply on data -- doing
        add color band to bollinger bands 
        Date silder ?
        improve search functionality,suggest options
        show names fo stocks from stock list


# table.py
    Rendering table of all the stocks buy/sell recomendation data
    todo:
        adding watchlist
        make faster by reducing calculation


# main.py
    gets data from nse site
    looks for upcoming dividend
    stores data in a file with dividend > 2
    gives terminal output of the data
    todo:
        redesign it to send output to terminal,file and app

# test.py
    for testing purpose

# getdata.py
    gets data from nse site and stores in a list of dataframe
    creates a output .csv file
    decide return type - list of dataframe
    online functionality of getData function to be tasted - still not working for app -- fixed temporarily
    todo:
    coclusion:
        Ready for use at this point

# tools.py
    plot MACD,RSI,SMA,EMA,Bollinger Bands,stock,Stochastic done
    analyze RSI,Stochastic done
    analyze MACD -- done
    variables of all analysis functions are set to a dictionary
    return type of buy and sell signal -- dataframe
    todo:
        add more indiactors
        add pattern
        customizing all the plots
        adding more types of indicators
        adding chart pattern
        find highly flactuating stocks (flactuation > 20%)
        ploting macdhist
    conclusion:
        for now it is fully ready to use

# dbconnect.py
    serving data from mongo database
    save data has to be modified to add updated data
    prevent adding duplicate data
    todo:
        add a database to add analyzed data ?? 
        _id: should be the date column


# tiralAndError.py
    for testing purpose



##
    NOTE: after extensive research can not understand why dataframe directly from site is not working whereas from csv file it is fine. Now going with file,but have to address it later.Same problem happening to the dataframe from database,normally dataframe is working but if it is passed with a quary then it is getting a empty dataframe,that is not rendering.
        Thoughts:
            Normally calling dbconnect.py returning dataframe but not with dash,may be it is interfearing with this process
        Fix:
            Saving data temporarily in .csv file will solve the problem --  have to find a better solution
            ? pickle

    have to implement database to store raw data and analyzed data.
##