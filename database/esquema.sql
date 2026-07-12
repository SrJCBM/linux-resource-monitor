PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS capturas (
    id_captura       INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    etiqueta         VARCHAR(50),
    comentario       TEXT,
    usuario_registro VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS cpu_metricas (
    id_captura           INTEGER PRIMARY KEY,
    modelo_procesador    VARCHAR(255),
    procesadores_logicos INTEGER NOT NULL,
    frecuencia_mhz       FLOAT,
    carga_promedio_1m    FLOAT,
    carga_promedio_5m    FLOAT,
    carga_promedio_15m   FLOAT,
    porcentaje_uso       FLOAT NOT NULL,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS memoria_metricas (
    id_captura        INTEGER PRIMARY KEY,
    mem_total_mb      FLOAT NOT NULL,
    mem_usada_mb      FLOAT NOT NULL,
    mem_libre_mb      FLOAT NOT NULL,
    mem_disponible_mb FLOAT NOT NULL,
    swap_total_mb     FLOAT,
    swap_usada_mb     FLOAT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS disco_metricas (
    id_disco_metrica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura       INTEGER NOT NULL,
    sistema_archivos VARCHAR(100) NOT NULL,
    punto_montaje    VARCHAR(255) NOT NULL,
    espacio_total_gb FLOAT NOT NULL,
    espacio_usado_gb FLOAT NOT NULL,
    espacio_libre_gb FLOAT NOT NULL,
    porcentaje_uso   FLOAT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS procesos_metricas (
    id_proceso_metrica  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura          INTEGER NOT NULL,
    pid                 INTEGER NOT NULL,
    nombre_proceso      VARCHAR(100) NOT NULL,
    estado              VARCHAR(20),
    usuario_propietario VARCHAR(50),
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS red_metricas (
    id_red_metrica     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura         INTEGER NOT NULL,
    interfaz           VARCHAR(20) NOT NULL,
    direccion_ip       VARCHAR(45),
    bytes_recibidos    BIGINT,
    bytes_enviados     BIGINT,
    paquetes_recibidos BIGINT,
    paquetes_enviados  BIGINT,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuarios_metricas (
    id_usuario_metrica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_captura         INTEGER NOT NULL,
    nombre_usuario     VARCHAR(50) NOT NULL,
    terminal           VARCHAR(20),
    inicio_sesion      DATETIME,
    FOREIGN KEY (id_captura) REFERENCES capturas(id_captura) ON DELETE CASCADE
);
