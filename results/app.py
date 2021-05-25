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


c = """
    select
	risk,
    count
        (*)
    from
        monitoring
    group by
        risk
"""

l = """
    select
        facility_type,
    count
        (*)
    from
        monitoring
    group by
        facility_type
"""

df = pd.read_sql(q, conn)
df2 = pd.read_sql(c, conn)
df3 = pd.read_sql(l, conn)

fig2 = px.bar(df2, x = "risk", y = "count", barmode = "group")
fig3 = px.bar(df3, x = "facility_type", y = "count", barmode = "group")
fig = px.histogram(df, x="score")

app.layout = html.Div(children = [
    html.H1(
    children = 'Monitoreo de modelos',
    style = {
      'textAlign': 'center'
    }
  ),

    html.Br(),

    html.Div(children = '1) Histograma de los scores del modelo:'),


    dcc.Graph(
    id = 'example-graph-2',
    figure = fig
  ),

html.Div(children = '2) Conteos por tipo de riesgo:'),


dcc.Graph(
    id = 'example-graph-3',
    figure = fig2
  ),

html.Div(children = '3) Conteos por tipo de establecimiento:'),


dcc.Graph(
    id = 'example-graph-4',
    figure = fig3
  ),

html.Br(),
html.Br(),
html.Br()
])

if __name__ == '__main__':
  app.run_server(debug = True)
