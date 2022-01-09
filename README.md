### What does it do?
    It gets data from nse site,stores in a mongo database,does analysis on the data and returns to the dash UI.Data is plotted with plotly library. It also does some technical analysis on the data and signals if you should buy or sell the stock.
    It also has a terminal side where output is printed to the terminal.

### Who can use it?
    For them who needs to do technical analysis on stockmarket data

### Installation
    install [mongodb](https://docs.mongodb.com/manual/installation/)
    install [ta-lib](https://ta-lib.org/hdr_dw.html)
    ```Bash
        $sudo apt install python3
        $sudo apt install pip3
        $sudo git clone **reposatoryname**
        $cd **repo folder**
        $sudo pip3 install -r requirements.txt
        $sudo chmod +x index.py
        $python3 index.py 
            or
        $gunicorn index:server
    ```

### HOW IT WORKS
    Gets data from NSE site.
        1. [NSEpy](https://nsepy.xyz/)
        2. [NSEtools](https://nsetools.readthedocs.io/en/latest/)

    Save output to mongo database

    Generate plot and get buy and sell signal
        1. Plot and visualization :    [plotly](https://plotly.com/graphing-libraries/)
        2. App design:   [Dash](https://dash.plotly.com/)

    Analysis by [ta-lib](https://mrjbq7.github.io/ta-lib/)

    Visualization and analysis tools -> tools.py

    Apply machine learning to the data to predict future result

### Status
    Stage 1 is complete and ready to use

### More info
    Still in development process,more to come