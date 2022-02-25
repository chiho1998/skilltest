from flask import Flask,request, render_template ,jsonify,redirect,url_for,send_from_directory
import dash
import dash_core_components as dcc                  
import dash_html_components as html                 
from dash.dependencies import Input, Output,State
import plotly.express as px
import pymongo


mongo = pymongo.MongoClient ("mongodb://127.0.0.1:27017/")
data1 = mongo['database']['news'].aggregate([
        {"$match": {"newsfrom": {"$exists": True}}},
        {"$group":
            {"_id":{
                'newsfrom': '$newsfrom'
            },"count":{"$sum":1}}
        },
        {
            "$project": {
                'newsfrom': '$_id.newsfrom',
                'count': '$count'
            }
        }
    ]
)
data3 = mongo['database']['news'].aggregate([
        {"$match": {"newsfrom": {"$exists": True}}},
        {"$group":
            {"_id":{
                'type': "$type",
                'newsfrom': '$newsfrom'
            },"count":{"$sum":1}}
        },
        {
            "$project": {
                'type': "$_id.type",
                'newsfrom': '$_id.newsfrom',
                'count': '$count'
            }
        }
    ]
)
data2 = mongo['database']['news'].aggregate([
        {"$match": {"newsfrom": {"$exists": True}}},
        {"$group":
            {
                "_id":"$type",
                "count":{"$sum":1}
            }
        }
    ]
)

#-----------


server = Flask(__name__)

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/'
)

app.layout =  html.Div(
    children = [
        html.H1('News Dashboard'),
        html.Div(children = 'abc',id ='abc'),
        html.Div(children = [
            dcc.Graph(
                id='example-graph1',
                figure = px.bar(data1, x="newsfrom", y="count", title="test"),
                style = {
                    'width': '50%',
                    'display': 'inline-block'
                }
            ),
            dcc.Graph(
                id='example-graph2',
                figure = px.pie(data2, values='count', names='_id',labels={'_id':'Type'}, color_discrete_sequence=px.colors.sequential.RdBu),
                style = {
                    'width': '50%',
                    'display': 'inline-block'
                }
            ),
            dcc.Graph(
                id='example-graph3',
                figure = px.treemap(data3, path=['newsfrom', 'type'], values='count',
                  color='type',
                  ),
                style = {
                    'width': '50%',
                    'display': 'inline-block'
                }
            )
        ],id ='container'),
    ]
)


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000,debug=True)