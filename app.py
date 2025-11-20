\
    # app.py - Aplicación de consola para CRUD sobre la BD 'biblioteca'
    # Requiere: mysql-connector-python
    import os
    import mysql.connector
    from mysql.connector import errorcode
    from getpass import getpass

    # Config: la app lee variables de entorno, si no están las pide al usuario.
    def get_db_config():
        config = {
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'database': os.getenv('DB_NAME', 'biblioteca')
        }
        # Si faltan datos, pedirlos
        if not config['host']:
            config['host'] = input('DB Host: ')
        if not config['user']:
            config['user'] = input('DB User: ')
        if not config['password']:
            config['password'] = getpass('DB Password: ')
        return config

    def connect_db():
        cfg = get_db_config()
        try:
            conn = mysql.connector.connect(**cfg)
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Error de autenticación. Verifique usuario/contraseña.')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Base de datos no existe. Ejecute el script SQL en /db/schema.sql o cree la BD.')
            else:
                print('Error de conexión:', err)
            return None

    # CRUD - Libros
    def listar_libros(conn):
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT l.id, l.titulo, l.autor, l.ano_publicacion, l.estado, u.nombre AS usuario FROM libros l LEFT JOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id;')
        rows = cur.fetchall()
        if not rows:
            print('No hay libros.')
        else:
            for r in rows:
                print(f\"[{r['id']}] {r['titulo']} - {r['autor']} ({r['ano_publicacion']}) Estado: {r['estado']} Usuario: {r['usuario']}\")
        cur.close()

    def agregar_libro(conn):
        titulo = input('Título: ').strip()
        autor = input('Autor: ').strip()
        try:
            ano = int(input('Año de publicación (opcional, dejar en blanco para NULL): ') or 0)
        except ValueError:
            ano = None
        cur = conn.cursor()
        cur.execute('INSERT INTO libros (titulo, autor, ano_publicacion) VALUES (%s,%s,%s);', (titulo, autor, ano or None))
        conn.commit()
        print('Libro agregado con id', cur.lastrowid)
        cur.close()

    def actualizar_estado_libro(conn):
        try:
            id_libro = int(input('ID del libro a actualizar: '))
        except ValueError:
            print('ID inválido.')
            return
        nuevo_estado = input(\"Nuevo estado (disponible/prestado/perdido): \").strip().lower()
        if nuevo_estado not in ('disponible','prestado','perdido'):
            print('Estado inválido.')
            return
        usuario_id = None
        if nuevo_estado == 'prestado':
            try:
                usuario_id = int(input('ID del usuario que toma el préstamo: '))
            except ValueError:
                print('ID usuario inválido.')
                return
        cur = conn.cursor()
        cur.execute('UPDATE libros SET estado=%s, usuario_id=%s WHERE id=%s;', (nuevo_estado, usuario_id, id_libro))
        conn.commit()
        if cur.rowcount == 0:
            print('No se encontró el libro.')
        else:
            print('Estado actualizado.')
        cur.close()

    def eliminar_libro(conn):
        try:
            id_libro = int(input('ID del libro a eliminar: '))
        except ValueError:
            print('ID inválido.')
            return
        cur = conn.cursor()
        cur.execute('DELETE FROM libros WHERE id=%s;', (id_libro,))
        conn.commit()
        if cur.rowcount == 0:
            print('No se encontró el libro.')
        else:
            print('Libro eliminado.')
        cur.close()

    # CRUD - Usuarios
    def listar_usuarios(conn):
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT id, nombre, email, fecha_registro FROM usuarios ORDER BY id;')
        rows = cur.fetchall()
        if not rows:
            print('No hay usuarios.')
        else:
            for r in rows:
                print(f\"[{r['id']}] {r['nombre']} - {r['email']} (registrado: {r['fecha_registro']})\")
        cur.close()

    def agregar_usuario(conn):
        nombre = input('Nombre: ').strip()
        email = input('Email: ').strip()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO usuarios (nombre, email) VALUES (%s,%s);', (nombre, email))
            conn.commit()
            print('Usuario agregado con id', cur.lastrowid)
        except mysql.connector.Error as err:
            print('Error al agregar usuario:', err)
        finally:
            cur.close()

    def actualizar_usuario(conn):
        try:
            id_u = int(input('ID del usuario a actualizar: '))
        except ValueError:
            print('ID inválido.')
            return
        nombre = input('Nuevo nombre (dejar en blanco para no cambiar): ').strip()
        email = input('Nuevo email (dejar en blanco para no cambiar): ').strip()
        cur = conn.cursor()
        if nombre and email:
            cur.execute('UPDATE usuarios SET nombre=%s, email=%s WHERE id=%s;', (nombre, email, id_u))
        elif nombre:
            cur.execute('UPDATE usuarios SET nombre=%s WHERE id=%s;', (nombre, id_u))
        elif email:
            cur.execute('UPDATE usuarios SET email=%s WHERE id=%s;', (email, id_u))
        else:
            print('Nada para actualizar.')
            cur.close()
            return
        conn.commit()
        if cur.rowcount == 0:
            print('No se encontró el usuario.')
        else:
            print('Usuario actualizado.')
        cur.close()

    def eliminar_usuario(conn):
        try:
            id_u = int(input('ID del usuario a eliminar: '))
        except ValueError:
            print('ID inválido.')
            return
        cur = conn.cursor()
        # Si existen libros con usuario_id referenciando este usuario, la FK está ON DELETE SET NULL según schema
        cur.execute('DELETE FROM usuarios WHERE id=%s;', (id_u,))
        conn.commit()
        if cur.rowcount == 0:
            print('No se encontró el usuario.')
        else:
            print('Usuario eliminado.')
        cur.close()

    # Menú principal
    def menu():
        conn = connect_db()
        if conn is None:
            print('No se pudo conectar a la base de datos. Saliendo.')
            return
        try:
            while True:
                print('\\n=== Sistema de Gestión de Biblioteca ===')
                print('1. Listar libros')
                print('2. Agregar libro')
                print('3. Actualizar estado de libro')
                print('4. Eliminar libro')
                print('5. Listar usuarios')
                print('6. Agregar usuario')
                print('7. Actualizar usuario')
                print('8. Eliminar usuario')
                print('0. Salir')
                opt = input('Seleccione una opción: ').strip()
                if opt == '1': listar_libros(conn)
                elif opt == '2': agregar_libro(conn)
                elif opt == '3': actualizar_estado_libro(conn)
                elif opt == '4': eliminar_libro(conn)
                elif opt == '5': listar_usuarios(conn)
                elif opt == '6': agregar_usuario(conn)
                elif opt == '7': actualizar_usuario(conn)
                elif opt == '8': eliminar_usuario(conn)
                elif opt == '0':
                    print('Saliendo...')
                    break
                else:
                    print('Opción inválida.')
        finally:
            conn.close()

    if __name__ == '__main__':
        menu()
