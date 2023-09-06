# Este script debe ejecutarse para crear la base de datos y las tablas desde cero, en caso de que se desee
# restablecer las tablas. Si ya existe alguna de las tablas, sqlite dara un error referido a eso.

#! DESCOMENTAR LAS LINEAS c.execute(...) PARA CREAR LAS TABLAS !!!
import sqlite3
# Crea una base de datos para conectarse
conn = sqlite3.connect('Reportes_vibraciones')

# Crea un cursor
c = conn.cursor()

# Crea las tablas
c.execute("""CREATE TABLE empresas_nueva (
    nombre TEXT NOT NULL,
    direccion TEXT,
    localidad TEXT,
    provincia TEXT
)
""")
c.execute("""CREATE TABLE instrumentos (
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    nro_serie INT NOT NULL,
    fecha TEXT,
    certificado_nro, INT)
    """)
# c.execute("""CREATE TABLE informes (
#     nro_informe TEXT,
#     titulo TEXT,
#     empleado TEXT,
#     fecha TEXT,
#     id_empresa INTEGER,
#     id_instrumento INTEGER,
#     archivo_descarga BLOB,
#     FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
#     FOREIGN KEY (id_instrumento) REFERENCES instrumentos (id_instrumento)
# )""")

# Commitear los cambios en la base de datos
conn.commit()

# Cerrar conexion en la base de datos
conn.close()