from src.database.connection import get_connection

def autenticar_usuario(username, senha):
    conn = get_connection()
    query = "SELECT id, nome FROM usuarios WHERE username=%s AND senha=%s"
    cursor = conn.cursor()
    cursor.execute(query, (username, senha))
    result = cursor.fetchone()
    conn.close()
    return result
