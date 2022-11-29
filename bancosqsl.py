import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `filmesdb`;")

cursor.execute("CREATE DATABASE `filmesdb`;")

cursor.execute("USE `filmesdb`;")

# criando tabelas
TABLES = {}
TABLES['filmes'] = ('''
      CREATE TABLE `filmes` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `avaliacao` int(10) NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')


# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Rafael", "Rafa", generate_password_hash("senha@123").decode('utf-8')),
    
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from filmesdb.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo filmes
filmes_sql = 'INSERT INTO filmes (nome, categoria, avaliacao) VALUES (%s, %s, %s)'
filmes = [
      ('Em busca do calice sagrado', 'Comedia', '10'),
      ('A vida de Brian', 'Comedia', '10'),
      ('O Sentido da vida', 'Comedia', '7'),
      ('BRAZIL: O FILME', 'Drama', '0'),
      ('O Incrivel Bulk', 'Acao', '0'),
      ('Birdemic: Choque e Terror', 'Terror', '0'),
]
cursor.executemany(filmes_sql, filmes)

cursor.execute('select * from filmesdb.filmes')
print(' -------------  filmes:  -------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()