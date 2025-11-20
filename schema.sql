-- schema.sql
-- Base de datos: biblioteca
-- Tablas: usuarios, libros
-- Ejecutar este script en la instancia MySQL (Clever Cloud, local, etc.)

CREATE DATABASE IF NOT EXISTS biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE biblioteca;

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabla libros
CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    ano_publicacion INT,
    estado ENUM('disponible','prestado','perdido') DEFAULT 'disponible',
    usuario_id INT NULL,
    fecha_ingreso DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Datos de prueba: usuarios
INSERT INTO usuarios (nombre, email) VALUES
('Ana Perez', 'ana@example.com'),
('Luis Gómez', 'luis@example.com');

-- Datos de prueba: libros
INSERT INTO libros (titulo, autor, ano_publicacion) VALUES
('Cien Años de Soledad', 'Gabriel García Márquez', 1967),
('El Aleph', 'Jorge Luis Borges', 1949),
('Introducción a Python', 'Autor Ejemplo', 2021);
