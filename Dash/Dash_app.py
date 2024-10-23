import dash
from dash import dcc, html, Input, Output, State
import configparser
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score



# Конфигурация

config_path = Path(__file__).resolve().parent.parent / 'Tests' / 'config.ini'
filepath = Path(__file__).resolve().parent.parent /'Airflow_Docker'/'scripts'/ 'files_config.ini'

# Инициализация приложения

app = dash.Dash(__name__)

# Загрузка конфигурации из INI файла

def load_config(filename=filepath):
    config = configparser.ConfigParser()
    config.read(filename)
    if 'Sliders' in config:
        return {
            "slider_1": config.getint('Sliders', 'slider_1', fallback=50),
            "slider_2": config.getint('Sliders', 'slider_2', fallback=25),
            "radio_choice_1": config.get('RadioButtons', 'choice_1', fallback='Option 1'),
            "radio_choice_2": config.get('RadioButtons', 'choice_2', fallback='Option A')
        }
    else:
        return {
            "slider_1": 50,
            "slider_2": 25,
            "radio_choice_1": 'Option 1',
            "radio_choice_2": 'Option A'
        }

# Сохранение конфигурации в INI файл

def save_to_config(data, filename=filepath):
    config = configparser.ConfigParser()
    config['Sliders'] = {k: str(v) for k, v in data.items() if k.startswith('slider')}
    config['RadioButtons'] = {k: str(v) for k, v in data.items() if k.startswith('radio')}
    with open(filename, 'w') as configfile:
        config.write(configfile)

# Загрузка данных из базы данных

def load_data():
    config = configparser.ConfigParser()
    config.read(config_path)
    conn_string = config.get('DATABASE', 'connection_url')

    engine = create_engine(conn_string)
    with engine.connect() as conn:
        query = "SELECT * FROM house_prices_fin"
        df = pd.read_sql(query, conn)

    return df

# Функция для создания слайдера

def create_slider(slider_id, value, min_value=0, max_value=100, step=1):
    return html.Div([
        dcc.Slider(
            id=slider_id,
            min=min_value,
            max=max_value,
            step=step,
            value=value,
            marks={i: str(i) for i in range(min_value, max_value + 1, 10)},
        )
    ], style={'width': '50%', 'margin': '20px'})

# Инициализация значений слайдеров и радиокнопок

initial_config = load_config()

# Интерфейс приложения

app.layout = html.Div([
    html.H1('Data Manipulation', style={'textAlign': 'center'}),

    html.Label('Частота запуска дага Airflow в минутах'),
    create_slider('slider-1', initial_config['slider_1']),
    html.Div(id='slider-1-output'),

    html.Label('Кол-во записей которые генерирует генератор синтетических данных'),
    create_slider('slider-2', initial_config['slider_2']),
    html.Div(id='slider-2-output'),

    html.Label('Запустить или нет дообучение'),
    dcc.RadioItems(
        id='radio-choice-1',
        options=[
            {'label': 'Да', 'value': 'Option 1'},
            {'label': 'Нет', 'value': 'Option 2'}
           
        ],
        value=initial_config['radio_choice_1'],  # Начальное значение
        labelStyle={'display': 'block'}  # Каждая опция в новом блоке
    ),
    html.Div(id='radio-choice-1-output'),

    html.Label('Выбор 2 (Radio Button)'),
    dcc.RadioItems(
        id='radio-choice-2',
        options=[
            {'label': 'Option A', 'value': 'Option A'},
            {'label': 'Option B', 'value': 'Option B'}
            
        ],
        value=initial_config['radio_choice_2'],  # Начальное значение
        labelStyle={'display': 'block'}
    ),
    html.Div(id='radio-choice-2-output'),

    html.Button('Save Values', id='save-button', n_clicks=0),
    html.Div(id='save-status'),  # Поле для отображения статуса сохранения

    html.H1('Data Quality Observation', style={'textAlign': 'center'}),
    html.Div(id='graphs-container-1', style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around', 'gap': '40px'}),

    html.H1('Model Quality Observation', style={'textAlign': 'center'}),
    html.Div(id='graphs-container-2', style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around', 'gap': '40px'}),

    html.H1('Feature Quality Observation', style={'textAlign': 'center'}),

    dcc.Interval(id='Interval', interval=10000, n_intervals=0)
])

@app.callback(
    [Output('slider-1-output', 'children'),
     Output('slider-2-output', 'children'),
     Output('radio-choice-1-output', 'children'),
     Output('radio-choice-2-output', 'children')],
    [Input('slider-1', 'value'),
     Input('slider-2', 'value'),
     Input('radio-choice-1', 'value'),
     Input('radio-choice-2', 'value')]
)
def update_output(slider1_value, slider2_value, radio_choice_1, radio_choice_2):
    return (f'Slider 1 Value: {slider1_value}',
            f'Slider 2 Value: {slider2_value}',
            f'Radio Choice 1: {radio_choice_1}',
            f'Radio Choice 2: {radio_choice_2}')

@app.callback(
    Output('save-status', 'children'),
    Input('save-button', 'n_clicks'),
    [State('slider-1', 'value'),
     State('slider-2', 'value'),
     State('radio-choice-1', 'value'),
     State('radio-choice-2', 'value')]
)
def save_values(n_clicks, slider1_value, slider2_value, radio_choice_1, radio_choice_2):
    if n_clicks > 0:
        config_data = {
            "slider_1": slider1_value,
            "slider_2": slider2_value,
            "radio_choice_1": radio_choice_1,
            "radio_choice_2": radio_choice_2
        }
        save_to_config(config_data)
        return 'Values have been saved successfully!'
    return ''

@app.callback(
    [Output('graphs-container-1', 'children'),
     Output('graphs-container-2', 'children')],
    Input('Interval', 'n_intervals')
)
def update_graph(_):
    df = load_data()

    # Обработка данных

    df['new_dt'] = pd.to_datetime(df['dt']).dt.strftime('%d-%m-%Y')
    grouped = df.groupby('dt').agg({'Id': ['count', 'nunique'], 'SalePrice': 'sum'}).reset_index()
    grouped.columns = ['_'.join(col) for col in grouped.columns]

    fig1 = px.line(grouped, x='dt_', y='SalePrice_sum', title='Total Sales Over Time')
    fig2 = px.line(grouped, x='dt_', y='Id_count', title='IDs Over Time')
    fig3 = px.line(grouped, x='dt_', y='Id_nunique', title='Distinct IDs Over Time')

    dt_list, mae_list, mape_list, r2_list = [], [], [], []

    for i in df['dt'].unique():
        train_df = df[df['dt'] == i]
        mae = round(mean_absolute_error(train_df['SalePrice'], train_df['prediction']), 2)
        mape = round(mean_absolute_percentage_error(train_df['SalePrice'], train_df['prediction']), 2)
        r2 = round(r2_score(train_df['SalePrice'], train_df['prediction']), 2)
        dt_list.append(i)
        mae_list.append(mae)
        mape_list.append(mape)
        r2_list.append(r2)

    df_cols = pd.DataFrame({'dt': dt_list, 'mae': mae_list, 'mape': mape_list, 'R2': r2_list})

    fig4 = px.line(df_cols, x='dt', y='mae', title='Mean Absolute Error Over Time')
    fig5 = px.line(df_cols, x='dt', y='mape', title='Mean Absolute Percentage Error Over Time')
    fig6 = px.line(df_cols, x='dt', y='R2', title='R2 Score Over Time')

    return [dcc.Graph(figure=fig) for fig in [fig1, fig2, fig3]], [dcc.Graph(figure=fig) for fig in [fig4, fig5, fig6]]

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
