from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from folder import input_match
from parser import open_csv, parser_data_of_time, parser_data_of_sectors
# from dash_auth import BasicAuth
import plotly.express as px
import pandas as pd


app = Dash(__name__, title="Statistic Stadium", suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Авторизация простая
# USER_PWD = {"user": "123",
#             "user2": "useSomethingMoreSecurePlease",}
# BasicAuth(app, USER_PWD)

# Вывод таблицы
table1 = dash_table.DataTable(id='table_data', sort_action='native',
                              style_table={'height': '700px', 'overflowY': 'auto'},
                              style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
                              style_data_conditional=[
                                  {
                                      'if': {
                                          'filter_query': '{Количество проходов} > 100',
                                          # 'filter_query': '{{Население (млн)}} = {}'.format(min_population),
                                          'column_id': 'Количество проходов'
                                      },
                                      'backgroundColor': 'blue',
                                      'color': 'white'
                                  },
{
                                      'if': {
                                          'filter_query': '{Количество проходов} < 5',
                                          'column_id': 'Количество проходов'
                                      },
                                      'backgroundColor': 'red',
                                      'color': 'white'
                                  }
                              ],
                              )

# Вывод дашборда
app.layout = html.Div([
    html.H2(style={'color': 'darkblue',
                   'text-align': 'center',
                   'padding': '20px 20px 20px 20px'},
                   id='title'),
    html.Br(),
    dbc.Row([
        dbc.Col(width=1),
        dbc.Col(dcc.Dropdown(input_match(), placeholder='Выберите матч', style={'color': 'darkblue'}, id='select_match'), width=5),
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
    dcc.Graph(id='output_graph4'),
    dbc.Row([
        dbc.Col(width=6),
        dbc.Col(dcc.Dropdown(placeholder='Выберите сектор', style={'color': 'darkblue'}, id='select_sectors')),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='output_graph3'), width=6),
        dbc.Col(dcc.Graph(id='output_graph5'), width=6),
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
              Output('output_graph4', 'figure'),
              Output('select_sectors', 'options'),
              Input('select_match', 'value'))

def display_graph(match):
    if match is None:
        raise PreventUpdate
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
        y_two_to_data_sectors = [int(i[4]) for i in to_several_graph[0]]

        fig3_several = px.bar(x=x_to_data_sectors, y=[y_to_data_sectors, y_two_to_data_sectors], barmode='group', height=400, title=f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО СЕКТОРАМ {match}')

        headers_to_fig4 = ['Сектор', 'Точка доступа', 'Проходы', 'Проценты пр', 'Отменены', 'Процент отм']
        rows = to_several_graph[2]
        df_to_fig4 = pd.DataFrame(rows, columns=headers_to_fig4)
        # data_sectors = df_to_fig4.query("Сектор == 'SMR.G1/КПП G1'")
        fig4_several = px.bar(df_to_fig4, x='Точка доступа', y=['Проходы', 'Отменены'], barmode="stack", color='Сектор' , height=600,)

        # several_graph = []
        # for i in to_several_graph[1]:
        #     figure = px.bar(x=[0], y=[1], title=str(i))
        #     several_graph.append(dcc.Graph(figure=figure))
        group_by_data_sectors = []
        for i in to_several_graph[0]:
            group_by_data_sectors.append(i[0])
        select_sectors = group_by_data_sectors

        return fig, fig2, title_page, number_of_passes, df.to_dict('records'), fig3_several, fig4_several, select_sectors

@app.callback(Output('output_graph5', 'figure'),
              Input('select_match', 'value'),
              Input('select_sectors', 'value'))

def display_sectors_graph(match, sectors):
    if match is None or sectors is None:
        raise PreventUpdate
        # fig4_several = px.bar()
        # return fig4_several
    else:
        to_several_graph = parser_data_of_sectors(open_csv(match))
        headers_to_fig4 = ['Сектор', 'Точка доступа', 'Проходы', 'Проценты пр', 'Отменены', 'Процент отм']
        rows = to_several_graph[2]
        df_to_fig4 = pd.DataFrame(rows, columns=headers_to_fig4)
        data_sectors = df_to_fig4.query(f"Сектор == '{sectors}'")
        fig4_several = px.bar(data_sectors, x='Точка доступа', y=['Проходы', 'Отменены'], title=f'РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО КОНКРЕТНОМУ СЕКТОРУ', barmode='group', height=400, )

        return fig4_several

if __name__ == '__main__':
    app.run(debug=True)
