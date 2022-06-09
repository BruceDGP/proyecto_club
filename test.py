import psycopg2

conexion = psycopg2.connect(host="192.168.100.19", database="authenticator", user="postgres", password="admin")

cur = conexion.cursor()

cur.execute("SELECT * FROM usuarios")

for id_value, surename, lastname, email, code, username, password, birthday in cur.fetchall():
    print(id_value, surename, lastname, email, code, username, password, birthday)

conexion.close()