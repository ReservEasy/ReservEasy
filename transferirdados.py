import sqlite3

try:
    # Conecte-se ao banco de dados SQLite
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Copie os dados da tabela conta_usuario para a tabela usuario_usuario
    cursor.execute('''
    INSERT INTO usuario_usuario
    SELECT * FROM conta_usuario;
    ''')

    # Confirme as alterações
    conn.commit()

except sqlite3.Error as e:
    print(f"Erro ao executar o comando: {e}")

finally:
    # Feche a conexão
    conn.close()
