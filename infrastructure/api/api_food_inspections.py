from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from src.utils.general import get_db_conn_sql_alchemy
from datetime import datetime

db_conn_str = get_db_conn_sql_alchemy('../../conf/local/credentials.yaml')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn_str
api = Api(app)
db = SQLAlchemy(app)


class ScoresPredictions(db.Model):
    __table_args__ = {'schema': 'api'}
    __tablename__ = 'scores'

    id_inspection = db.Column(db.Integer, primary_key=True)
    dba_name = db.Column(db.String)
    license = db.Column(db.Integer)
    inspection_date = db.Column(db.DateTime)
    ground_truth = db.Column(db.Integer)
    score = db.Column(db.Float)
    label = db.Column(db.Integer)
    predictions_date = db.Column(db.DateTime)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


one_prediction = api.model("score_prediction_label", {
    'id_inspection': fields.Integer,
    'dba_name': fields.String,
    'inspection_date': fields.Date,
    'ground_truth': fields.Integer,
    'score': fields.Float,
    'label': fields.Integer,
    'predictions_date': fields.Date
})

one_prediction_list = api.model('score_prediction_label_output', {
    'license': fields.Integer,
    'predictions': fields.Nested(one_prediction)
})


date_prediction = api.model("date_score_prediction_label", {
    'id_inspection': fields.Integer,
    'dba_name': fields.String,
    'license': fields.Integer,
    'inspection_date': fields.Date,
    'ground_truth': fields.Integer,
    'score': fields.Float,
    'label': fields.Integer,
    'predictions_date': fields.Date
})

date_prediction_list = api.model('date_score_prediction_label_output', {
    'predictions_date': fields.Date,
    'predictions': fields.Nested(date_prediction)
})



# endpoints
@api.route('/')
class ApiInfo(Resource):
    def get(self):
        return {'Api_prediction': 'Api of Food Inspections'}


@api.route('/one_prediction/<int:license>')
class OnePrediction(Resource):
    @api.marshal_with(one_prediction_list, as_list=True)
    def get(self, license):
        one_pre = ScoresPredictions.query.filter_by(license=license).order_by(
            ScoresPredictions.score.desc()).all()
        predictions = []
        for element in one_pre:
            predictions.append({
                'id_inspection': element.id_inspection,
                'dba_name': element.dba_name,
                'inspection_date': element.inspection_date,
                'ground_truth': element.ground_truth,
                'score': element.score,
                'label': element.label,
                'predictions_date': element.predictions_date
            })
        return {'license': license, 'predictions': predictions}


@api.route('/date_prediction/<predictions_date>')
class DatePrediction(Resource):
    @api.marshal_with(date_prediction_list, as_list=True)
    def get(self, predictions_date):
        predictions_date = datetime.strptime(predictions_date, "%Y-%m-%d").date()
        date_pre = ScoresPredictions.query.filter_by(predictions_date=predictions_date).order_by(
            ScoresPredictions.score.desc()).all()
        predictions = []
        for element in date_pre:
            predictions.append({
                'id_inspection': element.id_inspection,
                'dba_name': element.dba_name,
                'license': element.license,
                'inspection_date': element.inspection_date,
                'ground_truth': element.ground_truth,
                'score': element.score,
                'label': element.label,
                'predictions_date': element.predictions_date
            })
        return {'predictions_date': predictions_date, 'predictions': predictions}


if __name__ == '__main__':
    app.run(debug=True)
