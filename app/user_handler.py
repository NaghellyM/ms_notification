import json
from flask import jsonify

# Funciones para cargar y guardar usuarios
def load_users():
    #'r' modo lectura
    with open('usuarios.json', 'r') as file:
        return json.load(file)

    # 'w' modo escritura
def save_users(users): #escribe la informacion
    with open('usuarios.json', 'w') as file:
        # se transforma en un json y lo guardo en unn archvo file
        json.dump(users, file, indent=4)

# Crear usuarios
def create_user(data):
    users = load_users()
    for user in users:
        if 'id' not in user:
            return {"message": "Error"}, 400

    if len(users) > 0:
        last_user = max(users, key=lambda x: x['id'])
        new_id = last_user['id'] + 1
    else:
        new_id = 1

    
    new_user = {
        "id": new_id,
        "name": data['name'],
        "password": data['password'],
        "email": data['email'],
        "nickname": data['nickname']
    }
    users.append(new_user)
    save_users(users)
    return {"message": "Creado con exito"}, 200

#Obtener todos  los usuarios 
def get_all_users():
    users = load_users()
    return users

#Obtener usuario por ID
def get_user_id(userId):
    users = load_users()
    user = next((u for u in users if u['id'] == userId), None)
    return user

# Actualizar usuario
def update_user(user_id, data):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)

    if user:
        user['name'] = data.get('name', user['name'])
        user['password'] = data.get('password', user['password'])
        user['email'] = data.get('email', user['email'])
        user['nickname'] = data.get('nickname', user['nickname'])
        save_users(users)
        return {"message": "Usuario actualizado con exito"}, 200
    else:
        return {"error": "Usuario no encontrado"}, 404

# Eliminar usuario
def delete_user(user_id):
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)

    if user:
        users.remove(user)
        save_users(users)
        return {"message": "Usuario eliminado con exito"}, 202
    else:
        return {"error": "Usuario no encontrado"}, 404