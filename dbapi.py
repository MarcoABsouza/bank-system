import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "bank.db")
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row
def create_table_clients(cursor,conexao):
    cursor.execute("CREATE TABLE clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100),email VARCHAR(150))")
    conexao.commit()

def insert_into_clients(conexao, cursor, name, email):    
    data = (name, email)
    cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?)", data)
    conexao.commit()

def update_register(conexao, cursor, name, email, id):
    data = (name, email, id)
    cursor.execute("update clients set name=?, email=? where id=?;", data)
    conexao.commit()

def delete_register(conexao,cursor,id):
    data = (id,)
    cursor.execute("delete from clients where id = ?; ", data)
    conexao.commit()


def insert_many(conexao, cursor, dados):
    cursor.executemany("insert into clients (name, email) values (?, ?)", dados)
    conexao.commit()

dados = [
    ('jessy', 'jessy@gmail.com'),
    ('ton', 'ton@gmail.com'),
    ('jaqueu', 'jaqueu@gmail.com'),
]

def recovery_clients(cursor, id):
    cursor.execute("select * from clients where id=?", (id, ))
    return cursor.fetchone()

def list_clients(cursor):
    return cursor.execute("select * from clients;")

#clients = list_clients(cursor)
#for client in clients:
#    print(dict(client))

#client = recovery_clients(cursor, 5)    
#print(dict(client))
#insert_many(conexao, cursor, dados)
#insert_into_clients(conexao,cursor, 'marco', 'aurelio@gmail.com')
#update_register(conexao, cursor, 'marco aurelio', 'marco@gmail.com', 1)
#delete_register(conexao,cursor, 1)
"""
try:
    cursor.execute("insert into clients (name, email) values (?, ?)", ('teste 1', 'teste1@gmail.com'))
    cursor.execute("insert into clients (id, name, email) values (?, ?, ?)", (6, 'teste 2', 'tes2@gmail.com'))
    conexao.commit()
except Exception as exc:
    print(f"Erro, {exc}")
    conexao.rollback()
"""

cursor.execute("drop table clients")