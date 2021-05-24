import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from src.utils.general import get_db_conn

app = dash.Dash(__name__)

conn = get_db_conn('../conf/local/credentials.yaml')

q = """
select
    risk,
    score,
    label,
    ground_truth
from
    monitoring
    """

df = pd.read_sql(q, conn)

#fig = px.bar(df, x = "Indicator", y = "Cases", color = "Country", barmode = "group")
fig = px.histogram(df, x="score")

app.layout = html.Div(style = {
  'backgroundColor': '#111111'
}, children = [
    html.H1(
    children = 'Hello Dash',
    style = {
      'textAlign': 'center',
      'color': '#7FDBFF'
    }
  ),

    html.Div(children = 'Dash: Python based web framework for interactive data visualization.', style = {
    'textAlign': 'center',
    'color': '#7FDBFF'
  }),

    dcc.Graph(
    id = 'example-graph-2',
    figure = fig
  )
])

if __name__ == '__main__':
  app.run_server(debug = True)
