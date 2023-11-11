from flask import Flask, jsonify, request
import cx_Oracle

app = Flask(__name__)

def get_db_connection():
    connection = cx_Oracle.connect('rm89162/280400@oracle.fiap.com.br:1521/orcl')
    return connection

@app.route('/registros', methods=['GET'])
def listar_registros():
    try: 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Matrizes")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(registros)
    except Exception as e:
        return jsonify({'error': f'Erro ao acessar o banco de dados: {str(e)}'}, 500)

@app.route('/registros', methods=['POST'])
def adicionar_registro():
    data = request.get_json()
    node_id = data.get('node_id')
    centroide = data.get('centroide')
    uf = data.get('uf')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Matrizes (Node_ID, Centroide, UF) VALUES (:node_id, :centroide, :uf)",
                       node_id=node_id, centroide=centroide, uf=uf)
        conn.commit()
        return jsonify({'message': 'Registro adicionado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': f'Erro ao adicionar registro: {str(e)}'}), 500


@app.route('/registros/<node_id>', methods=['DELETE'])
def deletar_registro(node_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Matrizes WHERE Node_ID = :node_id", {'node_id': node_id})
        conn.commit()
        return jsonify({'message': 'Registro deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao deletar registro: {str(e)}'}), 500

@app.route('/registros/<node_id>', methods=['PUT'])
def atualizar_registro(node_id):
    data = request.get_json()
    novo_centroide = data.get('centroide')
    nova_uf = data.get('uf')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Matrizes SET Centroide = :centroide, UF = :uf WHERE Node_ID = :node_id",
                       {'centroide': novo_centroide, 'uf': nova_uf, 'node_id': node_id})
        conn.commit()
        return jsonify({'message': 'Registro atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao atualizar registro: {str(e)}'}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Página não encontrada"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    app.run(debug=False)
