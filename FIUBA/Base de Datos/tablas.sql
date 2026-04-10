----- ENTIDADES -----

CREATE TABLE Paises(
   codigo CHAR(2) PRIMARY KEY,
   nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Usuarios(
   nombre_de_usuario  VARCHAR(32) PRIMARY KEY,
   password_hash VARCHAR(128) NOT NULL,
   nombre VARCHAR(100) NOT NULL,
   apellido VARCHAR(100) NOT NULL,
   mail VARCHAR(100) NOT NULL, CHECK(mail LIKE '%@%.%'), -- chequea que haya texto@.texto
   fecha_de_nacimiento DATE,
   fecha_de_registro DATE,
   cod_nacionalidad CHAR(2) NOT NULL REFERENCES Paises(codigo), -- aca se verifica
   cantidad_de_ingresos INT
);

CREATE TABLE Notificaciones(
   id_notificacion SERIAL PRIMARY KEY,
   mensaje VARCHAR(200) NOT NULL,
   fecha TIMESTAMP NOT NULL, -- guarda tambien la hora exacta ademas del dia
   leido BOOLEAN NOT NULL,
   tipo VARCHAR(32) CHECK (tipo IN ('publicacion_grupo', 'solicitud_amistad', 'publicacion_amigo'))
);

CREATE TABLE Grupos(
   id_grupo SERIAL PRIMARY KEY,
   nombre VARCHAR(50) NOT NULL,
   exclusividad VARCHAR(20) CHECK (exclusividad IN ('publico','privado'))
);

CREATE TABLE Mensajes(
   id SERIAL PRIMARY KEY,
   contenido VARCHAR(500) NOT NULL,
   fecha TIMESTAMP NOT NULL
);

CREATE TABLE Publicaciones(
    id_publicacion SERIAL PRIMARY KEY ,
    fecha_publicacion DATE NOT NULL,
    fecha_actualizacion DATE NOT NULL,
    contenido VARCHAR(100),
    tipo VARCHAR(20) CHECK (tipo IN ('Texto','Imagen','Video')) NOT NULL,
    formato VARCHAR(20),
    url VARCHAR(500),
    autor VARCHAR(32) NOT NULL,
    id_grupo int,
    FOREIGN KEY (autor) REFERENCES usuarios(nombre_de_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) ON DELETE CASCADE
);


----- RELACIONES -----

CREATE TABLE Amistades(
   usuario_solicitante VARCHAR(32) REFERENCES Usuarios(nombre_de_usuario) ON DELETE CASCADE,
   usuario_receptor VARCHAR(32) REFERENCES Usuarios(nombre_de_usuario) ON DELETE CASCADE,
   estado VARCHAR(20) CHECK (estado IN ('pendiente', 'aceptada', 'rechazada')),
   PRIMARY KEY (usuario_solicitante, usuario_receptor),
   CHECK (usuario_solicitante != usuario_receptor)
);

CREATE TABLE notificaciones_de_usuarios(
    nombre_de_usuario VARCHAR(32),
    id_notificacion int,
    PRIMARY KEY (nombre_de_usuario, id_notificacion),
    FOREIGN KEY (nombre_de_usuario) REFERENCES usuarios(nombre_de_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_notificacion) REFERENCES notificaciones(id_notificacion) ON DELETE CASCADE

);

CREATE TABLE miembros_de_grupos(
    nombre_usuario VARCHAR(32),
    id_grupo int,
    fecha_desde DATE NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('miembro','administrador')),

    PRIMARY KEY (nombre_usuario, id_grupo),
    FOREIGN KEY (nombre_usuario) REFERENCES usuarios(nombre_de_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo) ON DELETE CASCADE
    
);

CREATE TABLE publicaciones_destacadas_por_usuarios(
    nombre_de_usuario VARCHAR(32),
    id_publicacion int,
    fecha DATE NOT NULL,

    PRIMARY KEY (nombre_de_usuario, id_publicacion),
    FOREIGN KEY (nombre_de_usuario) REFERENCES usuarios(nombre_de_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_publicacion) REFERENCES publicaciones(id_publicacion) ON DELETE CASCADE

);

CREATE TABLE Mensajes_Entre_Usuarios(
   id_mensaje INT REFERENCES Mensajes(id),
   usuario_emisor VARCHAR(32) REFERENCES Usuarios(nombre_de_usuario) ON DELETE CASCADE,
   usuario_receptor VARCHAR(32) REFERENCES Usuarios(nombre_de_usuario) ON DELETE CASCADE,
   PRIMARY KEY (id_mensaje)
);


----- TRIGGERS -----

--- Notificar a los miembros de un grupo cuando alguien publica en él -----
CREATE OR REPLACE FUNCTION notificar_publicacion_grupo()
RETURNS trigger AS $$
DECLARE
    miembro VARCHAR(32);
    nuevo_id INT;
BEGIN
    IF NEW.id_grupo IS NULL THEN
        RETURN NEW;
    END IF;

    FOR miembro IN
        SELECT nombre_usuario
        FROM miembros_de_grupos
        WHERE id_grupo = NEW.id_grupo
          AND nombre_usuario <> NEW.autor
    LOOP
        INSERT INTO notificaciones (mensaje, fecha, leido, tipo)
        VALUES (
            NEW.autor || ' publicó algo en un grupo al que perteneces.',
            CURRENT_TIMESTAMP,
            FALSE,
            'publicacion_grupo'
        )
        RETURNING id_notificacion INTO nuevo_id;

        INSERT INTO notificaciones_de_usuarios (nombre_de_usuario, id_notificacion)
        VALUES (miembro, nuevo_id);
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notificar_publicacion_grupo
AFTER INSERT ON publicaciones
FOR EACH ROW
EXECUTE FUNCTION notificar_publicacion_grupo();



--- Notificar solicitud de amistad -----
CREATE FUNCTION notificar_solicitud_amistad()
RETURNS trigger AS $$
DECLARE
    nuevo_id int;
BEGIN

    INSERT INTO notificaciones (mensaje, fecha, tipo, leido)
    VALUES (
        'El usuario ' || NEW.usuario_solicitante || ' te ha enviado una solicitud de amistad.',
        CURRENT_TIMESTAMP,
        'solicitud_amistad',
        FALSE
    )
    RETURNING id_notificacion INTO nuevo_id;

    INSERT INTO notificaciones_de_usuarios (nombre_de_usuario, id_notificacion)
    VALUES (NEW.usuario_receptor, nuevo_id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_solicitud_amistad
AFTER INSERT ON amistades
FOR EACH ROW
EXECUTE FUNCTION notificar_solicitud_amistad();



--- Notificar a los amigos cuando alguien publica algo -----
CREATE OR REPLACE FUNCTION notificar_publicacion_amigos()
RETURNS trigger AS $$
DECLARE
    amigo VARCHAR(100);
    nuevo_id INT;
BEGIN
    IF NEW.id_grupo IS NOT NULL THEN
        RETURN NEW;
    END IF;

    FOR amigo IN
        (
            SELECT usuario_receptor AS amigo
            FROM amistades
            WHERE usuario_solicitante = NEW.autor AND estado = 'aceptada'
            
            UNION
            
            SELECT usuario_solicitante AS amigo
            FROM amistades
            WHERE usuario_receptor = NEW.autor AND estado = 'aceptada'
        )
    LOOP
        INSERT INTO notificaciones (mensaje, fecha, leido, tipo)
        VALUES (
            NEW.autor || ' ha realizado una nueva publicación.',
            CURRENT_TIMESTAMP,
            FALSE,
            'publicacion_amigo'
        )
        RETURNING id_notificacion INTO nuevo_id;

        INSERT INTO notificaciones_de_usuarios (nombre_de_usuario, id_notificacion)
        VALUES (amigo, nuevo_id);
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_notificar_publicacion_amigos
AFTER INSERT ON publicaciones
FOR EACH ROW
EXECUTE FUNCTION notificar_publicacion_amigos();