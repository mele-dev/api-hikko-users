import random
import sys
from flask import Flask, jsonify, request
from db.services.users import users

app= Flask(__name__)

# metodo para obtener todos los usuarios. A este le calculamos cuantos followers tiene cada uno de ellos y se lo agregamos a su objeto antes de retornarlo
@app.route('/')
def find_all():
    for user in users:
        followers = []
        for u in users:
            if user["user_id"] in u.get("users_following", []):
                followers.append(u["user_id"])
        user["followers"] = followers

    if users:
        return jsonify(users), 200

# en este otro metodo obtenemos un usuario por su id, en este tambien msotramos sus followers...
@app.route('/users/<user_id>')
def find_user_by_id(user_id):
    # Este metodo va a mostrar los datos del usuario o sea su id y sus segudores
    user = next((user for user in users if user["user_id"] == user_id), None)
    if user:
        followers = []
        for u in users:
            if user_id in u.get("users_following", []):
                followers.append(u["user_id"])

        user["followers"] = followers

        return jsonify(user), 200
    else:
        return 'Usuario no encontrado', 404
    
# en este ultimo metodo recorremos los usuarios y vamos almacenando su cantidad de seguidores como la menos, luego con el siguiente follower; si este tiene menos, establecemos la variable min_followers como su cantidad de seguidores, y asi sucesivamente hasta el ultimo. Esta variable almacenara y retornara al usuario con menos cantidad de followers
@app.route('/user_with_least_followers')
def user_with_least_followers():
    if not users:
        return 'No hay usuarios', 404

    min_followers = sys.maxsize
    users_with_least_followers = []

    for user in users:
        followers_count = len(user.get("followers", []))
        if followers_count < min_followers:
            min_followers = followers_count
            users_with_least_followers = [user]
        elif followers_count == min_followers:
            users_with_least_followers.append(user)

    chosen_user = random.choice(users_with_least_followers)
    result = {
        "user_id": chosen_user["user_id"],
        "amount_of_followers": min_followers
    }

    return jsonify(result), 200

if __name__=='__main__':
    app.run(debug=True)