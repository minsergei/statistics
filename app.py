from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from matplotlib.pyplot import title

from folder import input_match
from parser import open_csv, parser_data_of_time
# from dash_auth import BasicAuth
import plotly.express as px
import pandas as pd


test = {'a':[1, 2, 3], 'b':[1, 2, 3]}
df = pd.DataFrame.from_dict(test)

app = Dash(__name__, title="Statistic Stadium", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# USER_PWD = {"user": "123",
#             "user2": "useSomethingMoreSecurePlease",}
# BasicAuth(app, USER_PWD)

app.layout = html.Div([
    html.H2(style={'color': 'darkblue',
                   'text-align': 'center',
                   'padding': '20px 20px 20px 20px'},
                   id='title'),
    html.Br(),
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dcc.Dropdown(input_match(), style={'color': 'darkblue'}, id='select_match'), width=5),
        dbc.Col(width=1),
        dbc.Col(html.Div(style={'color': 'darkblue',
                   'fontSize': '20px',
                   }, id='number_of_passes'), width=5),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(width=0),
        dbc.Col([html.H6('Время проходов по времени', style={'padding': '5px'}),
                 dash_table.DataTable(id='table_data', sort_action='native', style_table={'height': '700px', 'overflowY': 'auto'})], width=3),
        dbc.Col(width=1),
        dbc.Col([dcc.Graph(id='output_graph1', config={'displayModeBar': False}), dcc.Graph(id='output_graph2')], width=7),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col(dcc.Graph(id='output_graph3'), width=6),

    ]),
    html.Br(),
    # dash_table.DataTable(data=df.to_dict('records')),

#     html.H2('The World Bank'),
#     html.P('Key Facts:', style={'color': 'blue', 'fontSize': '20px'}),
#     html.Ul([
#         html.Li('Number of Economies: 170'),
#         html.Li('Temporal Coverage: 1974 - 2019'),
#         html.Li('Update Frequency: Quarterly'),
#         html.Li('Last Updated: March 18, 2000'),
#         html.Li([
#             'Source: ',
#             html.A('https://datacatalog.worldbank.org/dataset/poverty-andequity-database', href='https://ya.ru')
#         ])
#     ], style={'color': 'red'})
])
@app.callback(Output('output_graph1', 'figure'),
              Output('output_graph2', 'figure'),
              Output('title', 'children'),
              Output('number_of_passes', 'children'),
              Output('table_data', 'data'),
              Input('select_match', 'value'))

def display_graph(match):
    if match is None:
        fig = px.bar()
        fig2 = px.bar()
        fig.layout.title = f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ'
        title_page = f'Статистика по матчу'
        number_of_passes = 'Всего проходов по билетам: 0'
        table_data = pd.DataFrame.from_dict({})
        return fig, fig2, title_page, number_of_passes, table_data.to_dict('records')
    else:
        data_to_fig = parser_data_of_time(open_csv(match)[3:])
        fig = px.line(x=data_to_fig[0], y=data_to_fig[1], height=400, title=f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ {match}')
        fig2 = px.bar(x=data_to_fig[0], y=data_to_fig[1], height=400, text=data_to_fig[2])
        fig.layout.xaxis.title = 'Время'
        fig.layout.yaxis.title = 'Входы по билетам'
        fig2.layout.xaxis.title = 'Время'
        fig2.layout.yaxis.title = 'Входы по билетам'
        title_page = f'Статистика по матчу {match}'
        number_of_passes =  f'Всего проходов по билетам: {data_to_fig[3][1]}'
        table_data = pd.DataFrame.from_dict(data_to_fig[4])

        return fig, fig2, title_page, number_of_passes, table_data.to_dict('records')


if __name__ == '__main__':
    app.run(debug=True)
