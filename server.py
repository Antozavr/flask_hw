import flask
import pydantic
import schema
from flask import jsonify
from flask import request
from flask.views import MethodView
from models import Session, Announcement
from schema import CreateAd

app = flask.Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message


def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({'status': 'error', 'description': er.message})
    response.status_code = er.status_code
    return response


def get_ad(session, ad_id):
    ad = session.get(Announcement, ad_id)
    if ad is None:
        raise HttpError(status_code=404, message='ad not found')
    return ad


class AdView(MethodView):

    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return jsonify(
                {
                    'id': ad.id,
                    'header': ad.header,
                    'description': ad.description,
                    'creation_date': ad.creation_date.isoformat(),
                    'owner': ad.owner
                }
            )

    def post(self):
        json_data = dict(request.json)
        try:
            json_data_validate = CreateAd(**json_data).dict()
        except pydantic.ValidationError as er:
            raise HttpError(400, 'error')

        with Session() as session:
            ad = Announcement(**json_data_validate)
            session.add(ad)
            session.commit()
            return jsonify({
                'id': ad.id,
                'header': ad.header,
                'owner': ad.owner,
                'description': ad.description,
            })

    def patch(self, ad_id):
        validated_json = validate(schema.UpdateAd, request.json)
        with Session() as session:
            ad = get_ad(session, ad_id)
        for field, value in validated_json.items():
            setattr(ad, field, value)
        session.add(ad)
        session.commit()
        return jsonify({
            'status': 'success'
        })

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
        session.delete(ad)
        session.commit()
        return jsonify({
            'status': 'success'
        })


ad_view = AdView.as_view('AdvertisementsView')
app.add_url_rule('/ad/', view_func=ad_view, methods=['POST'])
app.add_url_rule('/ad/<int:ad_id>/', view_func=ad_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run()
