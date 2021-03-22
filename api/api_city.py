import flask
import requests
import os
from data.__all_models import User
from data import db_session

blueprint = flask.Blueprint(
    'city',
    __name__,
    template_folder='templates'
)


def return_ADDRES(adress):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0" \
                       f"493-4b70-98ba-98533de7710b&geocode={adress}&format=json"

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["Point"]["pos"]
        return ",".join(toponym_address.split())
    else:
        return None


@blueprint.route('/users_show/<int:user_id>')
def show_city(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id).to_dict()
    if not data or "city_from" not in data or data["city_from"] is None:
        return f'<h1>Bad request</h1>'
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={return_ADDRES(data['city_from'])}" \
                  f"&spn=0.1,0.1&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return f'<h2>Http статус: {response.status_code} ({response.reason})</h2>'
    map_file = "static/img/map.png"
    if os.path.exists(map_file):
        os.remove(map_file)
    with open(map_file, "wb") as file:
        file.write(response.content)
    return f"""
    <h1>Nostalgy</h1>
    <h1>{data['name']} {data['surname']}</h1>
    <h2>{data['city_from']}</h2>
    <img src="{flask.url_for('static', filename='img/map.png')}" 
           alt="здесь должна была быть картинка, но не нашлась">
    """


@blueprint.route('/show_city/<string:city>')
def show_city_dop(city):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={return_ADDRES(city)}" \
                  f"&spn=0.1,0.1&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return f'<h2>Http статус: {response.status_code} ({response.reason})</h2>'
    map_file = "static/img/map_1.png"
    if os.path.exists(map_file):
        os.remove(map_file)
    with open(map_file, "wb") as file:
        file.write(response.content)
    return f"""
    <img src="{flask.url_for('static', filename='img/map_1.png')}" 
           alt="здесь должна была быть картинка, но не нашлась">
    """
