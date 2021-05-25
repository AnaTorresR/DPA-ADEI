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
        label,
    count
        (*)
    from
        monitoring
    group by
        risk, label
"""

l = """
    select
        facility_type,
        label,
    count
        (*)
    from
        monitoring
    group by
        facility_type, label
"""

i = """
    select
       inspection_type,
       label,
       count(*)
    from
       monitoring
    group by
       inspection_type, label
"""

df = pd.read_sql(q, conn)
df2 = pd.read_sql(c, conn)
df3 = pd.read_sql(l, conn)
df4 = pd.read_sql(i, conn)

df2['label'] = df2['label'].astype('str')
df3['label'] = df3['label'].astype('str')
df4['label'] = df4['label'].astype('str')

fig2 = px.bar(df2, x = "risk", y = "count", color = "label", barmode = "group")
fig3 = px.bar(df3, x = "facility_type", y = "count", color = "label", barmode = "group")
fig4 = px.bar(df4, x= "inspection_type", y="count", color = "label", barmode = "group")
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

html.Div(children = '4) Conteos por tipo de inspección:'),

dcc.Graph(
    id = 'example-graph-5',
    figure = fig4
  ),

html.Br(),
html.Br(),
html.Br()
])

if __name__ == '__main__':
  app.run_server(debug = True)

