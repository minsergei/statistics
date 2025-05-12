from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc

from folder import input_match
from parser import open_csv, parser_data_of_time, parser_data_of_sectors
# from dash_auth import BasicAuth
import plotly.express as px
import pandas as pd


app = Dash(__name__, title="Statistic Stadium", external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Авторизация простая
# USER_PWD = {"user": "123",
#             "user2": "useSomethingMoreSecurePlease",}
# BasicAuth(app, USER_PWD)

# Вывод таблицы
table1 = dash_table.DataTable(id='table_data', sort_action='native', style_table={'height': '700px', 'overflowY': 'auto'}, style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'})

# Вывод дашборда
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
                 table1], width=3, style={'border': '2px solid', 'border-radius': '20px'}),
        # dbc.Col(width=1),
        dbc.Col([dcc.Graph(id='output_graph1', config={'displayModeBar': False}), dcc.Graph(id='output_graph2')], width=7, style={"margin-left": "2px", 'border': '2px solid', 'border-radius': '20px'}),
        dbc.Col(width=1),
    ]),
    html.Br(),
    html.H4('Статистика по секторам', style={'color': 'darkblue',
                   'text-align': 'center',
                   'padding': '20px 20px 20px 20px'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='output_graph3'), width=6),
        dbc.Col(id='several_graph', width=6),
    ]),
    html.Br(),


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
              Output('output_graph3', 'figure'),
              Output('several_graph', 'children'),
              Input('select_match', 'value'))

def display_graph(match):
    if match is None:
        fig = px.bar()
        fig2 = px.bar()
        fig.layout.title = f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ'
        title_page = f'Статистика по матчу'
        number_of_passes = 'Всего проходов по билетам: 0'
        table_data = pd.DataFrame.from_dict({})

        fig3 = px.bar()
        fig4 = dcc.Graph()
        return fig, fig2, title_page, number_of_passes, table_data.to_dict('records'), fig3, fig4
    else:
        data_to_fig = parser_data_of_time(open_csv(match)[0][3:])

        df = pd.DataFrame.from_dict(data_to_fig[1])

        fig = px.line(x=data_to_fig[1]['Время проходов'], y=data_to_fig[1]['Количество проходов'], height=400, title=f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ {match}')
        fig2 = px.bar(x=data_to_fig[1]['Время проходов'], y=data_to_fig[1]['Количество проходов'], height=400, text=data_to_fig[1]['В %'])
        fig.layout.xaxis.title = 'Время проходов'
        fig.layout.yaxis.title = 'Количество проходов'
        fig2.layout.xaxis.title = 'Время проходов'
        fig2.layout.yaxis.title = 'Количество проходов'
        title_page = f'Статистика по матчу {match}'
        number_of_passes =  f'Всего количество проходов: {data_to_fig[0][1]}'

        to_several_graph = parser_data_of_sectors(open_csv(match))
        x_to_data_sectors = [i[0] for i in to_several_graph[0]]
        y_to_data_sectors = [int(i[2]) for i in to_several_graph[0]]

        fig3_several = px.bar(x=x_to_data_sectors, y=y_to_data_sectors, height=400, title=f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО СЕКТОРАМ {match}', text=y_to_data_sectors)
        several_graph = []
        for i in to_several_graph[1]:
            figure = px.bar(x=[0], y=[1], title=str(i))
            several_graph.append(dcc.Graph(figure=figure))

        return fig, fig2, title_page, number_of_passes, df.to_dict('records'), fig3_several, several_graph


if __name__ == '__main__':
    app.run(debug=True)