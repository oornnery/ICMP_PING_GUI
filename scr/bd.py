import sqlite3

local = ".//dados//bd.db"

conexao = sqlite3.connect(local)
cursor = conexao.cursor()

# Cria a tabela no bd
cursor.execute('CREATE TABLE IF NOT EXISTS mtr_ativos ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'address TEXT,'
                'times TEXT,'
                'rtts TEXT,'
                'ttl TEXT'
                ')')


cursor.execute('CREATE TABLE IF NOT EXISTS mtr_historico ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'address TEXT,'
                'times TEXT,'
                'rtts TEXT,'
                'ttr TEXT'
                ')')

# Add values from bd
cursor.execute('INSERT INTO mtr_ativos (address, times, rtts, ttl) VALUES ("1.1.1.1", "09:31.02:", "12", "126")')
cursor.execute('INSERT INTO mtr_ativos (address, times, rtts, ttl) VALUES ("8.8.8.8", "09:32.02:", "15", "146")')

conexao.commit()

cursor.execute('SELECT * FROM mtr_ativos')

for linha in cursor.fetchall():
    print(linha)

cursor.close()
conexao.close()