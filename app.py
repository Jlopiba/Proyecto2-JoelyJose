from flask import Flask, request, jsonify
import Database

app = Flask(__name__)

@app.route('/robots/add', methods=['POST'])
def add_robot():
    try:
        data = request.get_json()
        robot = Database.addrobot(data)
        return jsonify(robot), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots', methods=['GET'])
def list_robots():
    try:
        robots = Database.listrobots()
        return jsonify(robots), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/<string:name>/medidas', methods=['PUT'])
def set_medidas(name):
    try:
        data = request.get_json()
        ecinta = data.get('ecinta')
        esensor = data.get('esensor')
        epinza = data.get('epinza')
        # Llamamos a la función para actualizar las medidas
        Database.setmedidas(name, ecinta, esensor, epinza)
        return jsonify({"message": f"Medidas para el robot '{name}' actualizadas."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/<string:name>/medidas', methods=['GET'])
def get_medidas(name):
    try:
        medidas = Database.get_medidas(name)
        return jsonify(medidas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/instruccion', methods=['POST'])
def add_instruccion():
    try:
        data = request.get_json()
        instruccion = data.get('instruccion')
        robot_name = data.get('robot_name')
        Database.instruccion(instruccion, robot_name)
        return jsonify({"message": f"Instrucción '{instruccion}' añadida para el robot '{robot_name}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/instruccionrobot', methods=['POST'])
def add_instruccionrobot():
    try:
        data = request.get_json()
        instruccion = data.get('instruccion')
        robot_name = data.get('robot_name')
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        Database.instruccionrobot(instruccion, robot_name, x, y, z)
        return jsonify({"message": f"Instrucción '{instruccion}' añadida para el robot '{robot_name}' con coordenadas ({x}, {y}, {z})."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/<string:name>/instrucciones', methods=['GET'])
def get_instrucciones(name):
    try:
        instrucciones = Database.get_instruccion(name)
        return jsonify({"instrucciones": instrucciones}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/historial', methods=['GET'])
def get_historial():
    try:
        historial = Database.get_historial()  # Aquí se llama a la función correcta
        return jsonify(historial), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/robots/removerobot/<string:name>', methods=['DELETE'])
def remove_robot(name):
    try:
        Database.removerobot(name)
        return jsonify({"message": f"Robot '{name}' eliminado."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
