# TP3 — Implementación de Base de Datos y Aplicación de Consola


## Resumen
Proyecto individual: implementar una base de datos MySQL y desarrollar una
aplicación de consola en Python que realice operaciones CRUD sobre la BD.

## Estructura del repositorio
```
tp3-biblioteca/
├── src/
│   └── app.py
├── db/
│   └── schema.sql
├── requirements.txt
└── README.md
```

## Requisitos
- Python 3.8+
- mysql-connector-python

## Instalación
1. Clonar el repositorio.
2. Crear un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configurar la base de datos en Clever Cloud
1. Crear una nueva base de datos MySQL en Clever Cloud (seguir guía de la plataforma).
2. Obtener credenciales: host, port, user, password y nombre de la base de datos.
3. Conectar por cliente MySQL (o usar la interfaz de Clever Cloud) y ejecutar `db/schema.sql` para crear tablas y datos de prueba.

## Variables de entorno
Configure las siguientes variables (o la app pedirá los datos al iniciar):
- DB_HOST
- DB_PORT (opcional, por defecto 3306)
- DB_USER
- DB_PASS
- DB_NAME (opcional, por defecto 'biblioteca')

## Uso
Ejecutar la aplicación:
```bash
python src/app.py
```

Ejemplo de opciones del menú:
- 1: Listar libros
- 2: Agregar libro
- 3: Actualizar estado de libro (prestado, disponible, perdido)
- 4: Eliminar libro
- 5: Listar usuarios
- 6: Agregar usuario
- 7: Actualizar usuario
- 8: Eliminar usuario

## Sugerencias para entrega en GitHub
- Subir el repositorio con la estructura indicada.
- Incluir capturas de pantalla en el README (en la sección de ejemplos de uso).
- Enviar el enlace por Classroom antes de la fecha de entrega.
