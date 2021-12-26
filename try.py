import dash_bootstrap_components as dbc
from dash import Input, Output, html

switches = html.Div(
    [
        dbc.Label("Toggle a bunch"),
        dbc.Checklist(
            options=[
                {"label": "MACD", "value": 'macd'},
                {"label": "RSI", "value": 'rsi'},
                {"label": "STOCH", "value": 'stoch', "disabled": True},
            ],
            value=['macd'],
            id="switches-input",
            switch=True,
        ),
    ]
)

@app.callback(
    Output("radioitems-checklist-output", "children"),
    Input("switches-input", "value"),
)
def on_form_change(radio_items_value, checklist_value, switches_value):
    template = "Radio button {}, {} checklist item{} and {} switch{} selected."

    n_checkboxes = len(checklist_value)
    n_switches = len(switches_value)

    output_string = template.format(
        radio_items_value,
        n_checkboxes,
        "s" if n_checkboxes != 1 else "",
        n_switches,
        "es" if n_switches != 1 else "",
    )
    return output_string