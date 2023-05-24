"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET

@app.route('/user', methods=['GET'])
def get_users():

    # obtiene todos los objetos de usuario de la base de datos
    users = User.query.all()

    # crea una lista de diccionarios con la información de cada usuario
    user_list = [element.serialize() for element in users]

    return jsonify(user_list), 200


@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User noy found', 404
    favorites = [favorite.serialize() for favorite in user.favorites]
    return jsonify(favorites), 200


@app.route('/planet', methods=['GET'])
def get_planets():
    allPlanets = Planet.query.all()
    result = [element.serialize() for element in allPlanets]
    return jsonify(result), 200


@app.route('/planet/int:planet_id', methods=['GET'])
def get_one_planet(planet_id):
    onePlanet = Planet.query.get(planet_id)
    if onePlanet is None:
        return 'Planet not found', 404
    return jsonify(onePlanet.serialize()), 200


@app.route('/people', methods=['GET'])
def get_people():
    allPeople = People.query.all()
    result = [element.serialize() for element in allPeople]
    return jsonify(result), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    onePeople = People.query.get(people_id)
    if onePeople is None:
        return 'People not found', 404
    return jsonify(onePeople.serialize()), 200


# POST

@app.route('/planet', methods=['POST'])
def post_planet():
    data = request.get_json()
    planet = Planet(
        name=data['name'], description=data['description'], population=data['population'])
    db.session.add(planet)
    db.session.commit()
    inserted_planet_data = planet.serialize()

    return jsonify(inserted_planet_data),200

@app.route('/people', methods=['POST'])
def post_people():
    data = request.get_json()
    people = People(
        name=data['name'], hair_color=data['hair_color'], gender=data['gender'])
    db.session.add(people)
    db.session.commit()
    inserted_people_data = people.serialize()

    return jsonify(inserted_people_data),200

@app.route('/favorite/user/planet', methods=['POST'])
def add_favorite_planet():
    data = request.get_json()
    planet_id = data['planet_id']
    user_id =data['user_id']

    user=User.query.get(user_id)
    planet=Planet.query.get(planet_id)
    new_favorite = Favorite(user= user, planet=planet)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {'msg' : 'Su planeta favorito ha sido agregado correctamente'}    

    return jsonify(response_body),200

@app.route('/favorite/user/people', methods=['POST'])
def add_favorite_people():
    data = request.get_json()
    people_id = data['people_id']
    user_id =data['user_id']

    user=User.query.get(user_id)
    people=People.query.get(people_id)
    new_favorite = Favorite(user= user, people=people)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {'msg' : 'Su planeta favorito ha sido agregado correctamente'}    

    return jsonify(response_body),200
  
# DELETE
@app.route('/favorite/user/people', methods= ['DELETE'])
def delete_favorite_people():

     data = request.get_json()
     people_id = data['people_id']
     user_id = data['user_id']

     user = User.query.get(user_id)
     people = People.query.get(people_id)
     
     delete_favorite = Favorite.query.filter_by(user=user, people=people).first()
     
     if delete_favorite is None:
        return jsonify({'msg' : 'No favourite found'}), 404
     
     db.session.delete(delete_favorite)
     db.session.commit()
     
     response_body = {'msg' : 'Su personaje favorito ha sido eliminado'}, 200
     return jsonify(response_body)

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id,user_id):

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    delete_favorite = Favorite.query.filter_by(user=user, planet=planet).first()

    if delete_favorite is None :
        return jsonify({'msg' : 'No favorite found'}), 404
    
    db.session.delete(delete_favorite)
    db.session.commit()

    response_body = {'msg' : 'Su planeta favorito ha sido eliminado'} , 200
    return jsonify(response_body)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
