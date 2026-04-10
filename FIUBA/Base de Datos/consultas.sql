--- REGISTRAR UN USUARIO ----

INSERT INTO usuarios (nombre_de_usuario, password_hash, nombre, apellido, mail, 
fecha_de_nacimiento, fecha_de_registro, cod_nacionalidad) VALUES
('BrianR', 'h123', 'Braian', 'Romero', 'brianr@example.com', '1991-06-15', NOW(), 'AR');

--- LISTAR TODOS LOS USUARIOS DE LA RED SOCIAL----

SELECT 
   nombre_de_usuario,
   nombre,
   apellido,
   mail,
   fecha_de_nacimiento,
   fecha_de_registro,
   cod_nacionalidad
FROM usuarios;

--- LISTAR TODAS LAS AMISTADES DE LA RED SOCIAL ---

SELECT
   A.usuario_solicitante,
   A.usuario_receptor
FROM Amistades A
WHERE A.estado = 'aceptada';

--- LISTAR LOS AMIGOS DE UN USUARIO PARTICULAR DE LA RED SOCIAL ----

SELECT A.usuario_receptor AS amigo
FROM Amistades A
WHERE A.estado = 'aceptada'
 AND A.usuario_solicitante = 'rulli12'
UNION
SELECT A.usuario_solicitante AS amigo
FROM Amistades A
WHERE A.estado = 'aceptada'
 AND A.usuario_receptor = 'rulli12';

--- LISTAR TODOS LOS MENSAJES DE LA RED SOCIAL ---

SELECT
   M.id,
   M.contenido,
   M.fecha,
   ME.usuario_emisor,
   ME.usuario_receptor
FROM Mensajes M
JOIN Mensajes_Entre_Usuarios ME ON M.id = ME.id_mensaje;

--- CONTABILIZAR LA CANTIDAD DE USUARIOS, AGRUPADOS POR PAIS ---

SELECT
   p.nombre,
   COUNT(u.nombre_de_usuario) AS cantidad
FROM paises AS p
LEFT JOIN usuarios AS u ON u.cod_nacionalidad = p.codigo
WHERE u.nombre_de_usuario IS NOT NULL
GROUP BY p.nombre
ORDER BY cantidad DESC;

--- REALIZAR UNA PUBLICACIÓN (DAR UN EJEMPLO DE CADA TIPO) ---

/*TEXTO*/
INSERT INTO publicaciones (fecha_publicacion, fecha_actualizacion, contenido, tipo, formato, url, autor, id_grupo)
VALUES (NOW(), NOW(), 'Yendo a la cancha a alentar a Vélez', 'Texto', NULL, NULL, 'BrianR', NULL);



/*IMAGEN*/
INSERT INTO publicaciones (fecha_publicacion, fecha_actualizacion, contenido, tipo, formato, url, autor, id_grupo)
VALUES (NOW(), NOW(), 'Fotito en el Amalfitani', 'Imagen', 'JPG',
 'https://upload.wikimedia.org/wikipedia/commons/6/6b/Estadio_Jos%C3%A9_Amalfitani_2025.jpg', 'BrianR', NULL);



/*VIDEO*/
INSERT INTO publicaciones (fecha_publicacion, fecha_actualizacion, contenido, tipo, formato, url, autor, id_grupo)
VALUES (NOW(), NOW(), 'Golazo del Tanque Silva', 'Video', 'MP4',
 'https://www.youtube.com/watch?v=AOkV00hGplc', 'BrianR', NULL);

--- ACTUALIZAR UNA PUBLICACIÓN (DAR UN EJEMPLO DE CADA TIPO) ---

/*TEXTO*/
UPDATE publicaciones
SET
   contenido = 'La dirigencia tiene que traer refuerzos!',
   fecha_actualizacion = NOW()
WHERE id_publicacion = 10;

/*IMAGEN*/
UPDATE publicaciones
SET
   contenido = 'Desde este ángulo se ve mejor el Amalfitani',
   fecha_actualizacion = NOW(),
   url = 'https://estadiosdb.com/pictures/stadiums/arg/el_fortin/el_fortin24.jpg',
   formato = 'JPG'
WHERE id_publicacion = 11;

/*VIDEO*/
UPDATE publicaciones
SET
   contenido = 'Golazo del burrito Martinez',
   fecha_actualizacion = NOW(),
   URL = 'https://www.youtube.com/watch?v=GDXnhMXKzEo',
   formato = 'WAV'
WHERE id_publicacion = 12;

--- ELIMINAR UNA PUBLICACIÓN (DAR UN EJEMPLO DE CADA TIPO) ---

DELETE FROM Publicaciones WHERE id_publicacion = 10 AND tipo='Texto';
DELETE FROM Publicaciones WHERE id_publicacion = 11 AND tipo='Imagen';
DELETE FROM Publicaciones WHERE id_publicacion = 12 AND tipo='Video';

--- DESREGISTRAR A UN USUARIO DE LA APLICACIÓN (DAR UN EJEMPLO) ---

DELETE FROM Usuarios WHERE nombre_de_usuario = 'insfran23';

--- MOSTRAR LAS PUBLICACIONES MAS POPULARES ORDENADAS POR CANTIDAD DE "FAVORITOS" QUE POSEEN ---

SELECT P.*
FROM Publicaciones P
JOIN (
   SELECT id_publicacion, COUNT(*) AS cantidad_destacados
   FROM Publicaciones_destacadas_por_usuarios
   GROUP BY id_publicacion
   ORDER BY cantidad_destacados DESC
   LIMIT 5
) AS topPublicacion ON P.id_publicacion=topPublicacion.id_publicacion;

--- MOSTRAR LOS USUARIOS MAS POPULARES BASANDOSE EN LA CANTIDAD DE PUBLICACIONES "FAVORITAS" 
--- QUE POSEEN SUS PUBLICACIONES ---

SELECT U.nombre_de_usuario, COUNT(UDP.id_publicacion) AS cantidad_destacados
FROM usuarios U
JOIN publicaciones P ON P.autor=U.nombre_de_usuario
JOIN Publicaciones_destacadas_por_usuarios UDP ON P.id_publicacion=UDP.id_publicacion
GROUP BY U.nombre_de_usuario
ORDER BY cantidad_destacados DESC
LIMIT 5;
