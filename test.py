import dash_bootstrap_components as dbc
from dash import Input, Output, html, Dash
table_header = [html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]
color_selector = html.Div(
    [
        html.Div("Select a colour theme:"),
        dbc.Select(
            id="change-table-color",
            options=[
                {"label": "primary", "value": "primary"},
                {"label": "secondary", "value": "secondary"},
                {"label": "success", "value": "success"},
                {"label": "danger", "value": "danger"},
                {"label": "warning", "value": "warning"},
                {"label": "info", "value": "info"},
                {"label": "light", "value": "light"},
                {"label": "dark", "value": "dark"},
            ],
            value="primary",
        ),
    ],
    className="p-3 m-2 border",
)

table = html.Div(
    [
        color_selector,
        dbc.Table(
            # using the same table as in the above example
            table_header + table_body,
            id="table-color",
            color="primary",
        ),
    ]
)
app = Dash(__name__, title="Statistic Stadium", external_stylesheets=[dbc.themes.LUX])
app.layout = html.Div([dbc.Col(table, width=4)])
#
#
@app.callback(Output("table-color", "color"), Input("change-table-color", "value"))
def change_table_colour(color):
    return color


if __name__ == '__main__':
    app.run(debug=True)