------ Datos iniciales para la tabla Paises y usuarios ------

INSERT INTO Paises (codigo, nombre) VALUES
('AR', 'Argentina'),
('BR', 'Brasil'),
('UY', 'Uruguay'),
('FR', 'Francia'),
('ES', 'España');

INSERT INTO usuarios (
    nombre_de_usuario, password_hash, nombre, apellido, mail,
    fecha_de_nacimiento, fecha_de_registro, cod_nacionalidad
) VALUES
    ('lmessi', 'h001', 'Lionel', 'Messi', 'lmessi@example.com', '1987-06-24', NOW(), 'AR'),
    ('dibu_mtz', 'h002', 'Emiliano', 'Martinez', 'dibu@example.com', '1992-09-02', NOW(), 'AR'),
    ('cuti_r', 'h003', 'Cristian', 'Romero', 'cuti@example.com', '1998-04-27', NOW(), 'AR'),
    ('otamendi30', 'h004', 'Nicolas', 'Otamendi', 'otamendi@example.com', '1988-02-12', NOW(), 'AR'),
    ('tagliafico3', 'h005', 'Nicolas', 'Tagliafico', 'tagliafico@example.com', '1992-08-31', NOW(), 'AR'),
    ('molina26', 'h006', 'Nahuel', 'Molina', 'molina@example.com', '1998-04-06', NOW(), 'AR'),
    ('paredes5', 'h007', 'Leandro', 'Paredes', 'paredes@example.com', '1994-06-29', NOW(), 'AR'),
    ('lmartinez22', 'h008', 'Lautaro', 'Martinez', 'lauta@example.com', '1997-08-22', NOW(), 'AR'),
    ('dpaul7', 'h009', 'Rodrigo', 'De Paul', 'depaul@example.com', '1994-05-24', NOW(), 'AR'),
    ('locelso20', 'h010', 'Giovani', 'Lo Celso', 'locelso@example.com', '1996-04-09', NOW(), 'AR'),
    ('enzof', 'h011', 'Enzo', 'Fernandez', 'enzo@example.com', '2001-01-17', NOW(), 'AR'),
    ('macallister10', 'h012', 'Alexis', 'Mac Allister', 'alexis@example.com', '1998-12-24', NOW(), 'AR'),
    ('alvarez9', 'h013', 'Julian', 'Alvarez', 'alvarez@example.com', '2000-01-31', NOW(), 'AR'),
    ('garnacho17', 'h014', 'Alejandro', 'Garnacho', 'garnacho@example.com', '2004-07-01', NOW(), 'AR'),
    ('buendia16', 'h015', 'Emiliano', 'Buendia', 'buendia@example.com', '1996-12-25', NOW(), 'AR'),
    ('foyth2', 'h016', 'Juan', 'Foyth', 'foyth@example.com', '1998-01-12', NOW(), 'AR'),
    ('lisandro6', 'h017', 'Lisandro', 'Martinez', 'lisandro@example.com', '1998-01-18', NOW(), 'AR'),
    ('senesi25', 'h018', 'Marcos', 'Senesi', 'senesi@example.com', '1997-05-10', NOW(), 'AR'),
    ('rulli12', 'h019', 'Geronimo', 'Rulli', 'rulli@example.com', '1992-05-20', NOW(), 'AR'),
    ('armani1', 'h020', 'Franco', 'Armani', 'armani@example.com', '1986-10-16', NOW(), 'AR'),
    ('montiel4', 'h021', 'Gonzalo', 'Montiel', 'montiel@example.com', '1997-01-01', NOW(), 'AR'),
    ('acuna8', 'h022', 'Marcos', 'Acuña', 'acuna@example.com', '1991-10-28', NOW(), 'AR'),
    ('dybala21', 'h023', 'Paulo', 'Dybala', 'dybala@example.com', '1993-11-15', NOW(), 'AR'),
    ('di_maria11', 'h024', 'Angel', 'Di Maria', 'dimaria@example.com', '1988-02-14', NOW(), 'AR'),
    ('pezzella6', 'h025', 'German', 'Pezzella', 'pezzella@example.com', '1991-06-27', NOW(), 'AR'),
    ('insfran23', 'h026', 'Nelson', 'Insfran', 'insfran@example.com', '1995-06-24', NOW(), 'AR'),
    ('giampaoli4', 'h027', 'Renzo', 'Giampaoli', 'giampaoli@example.com', '2000-01-07', NOW(), 'AR'),
    ('pintado15', 'h028', 'Juan', 'Pintado', 'pintado@example.com', '1997-07-28', NOW(), 'UY'),
    ('suso6', 'h029', 'Gaston', 'Suso', 'suso@example.com', '1991-11-11', NOW(), 'AR'),
    ('corbalan2', 'h030', 'Fabricio', 'Corbalan', 'corbalan@example.com', '2003-04-15', NOW(), 'AR'),
    ('pigretti33', 'h031', 'Ignacio', 'Pigretti', 'pigretti@example.com', '1998-01-19', NOW(), 'AR'),
    ('rojas29', 'h032', 'Yonatthan', 'Rojas', 'rojas@example.com', '2000-02-14', NOW(), 'AR'),
    ('tarzia8', 'h033', 'Nicolas', 'Tarzia', 'tarzia@example.com', '2001-04-03', NOW(), 'AR'),
    ('lescano10', 'h034', 'Matias', 'Lescano', 'lescano@example.com', '2004-09-12', NOW(), 'AR'),
    ('castro11', 'h035', 'Lucas', 'Castro', 'castro@example.com', '2005-03-20', NOW(), 'AR'),
    ('bautista_g', 'h036', 'Bautista', 'Galeano', 'bgaleano@example.com', '2006-02-21', NOW(), 'AR'),
    ('benitez21', 'h037', 'Benjamín', 'Benitez', 'bbenitez@example.com', '2003-10-26', NOW(), 'AR'),
    ('icht_santiago', 'h038', 'Santiago', 'Icht', 'icht@example.com', '2002-02-09', NOW(), 'AR'),
    ('miramon5', 'h039', 'Ignacio', 'Miramon', 'miramon@example.com', '2003-06-12', NOW(), 'AR'),
    ('ramirez9', 'h040', 'Rodrigo', 'Ramirez', 'ramirez@example.com', '2001-09-25', NOW(), 'AR'),
    ('deblas7', 'h041', 'Alan', 'De Blas', 'deblas@example.com', '2000-12-17', NOW(), 'AR'),
    ('cohen1', 'h042', 'Tomas', 'Cohen', 'cohen@example.com', '1999-08-08', NOW(), 'AR'),
    ('dominguez27', 'h043', 'Agustin', 'Dominguez', 'adominguez@example.com', '2004-05-30', NOW(), 'AR'),
    ('solari19', 'h044', 'Felipe', 'Solari', 'solari@example.com', '2002-06-14', NOW(), 'AR'),
    ('cocimano16', 'h045', 'Sebastian', 'Cocimano', 'cocimano@example.com', '2000-09-05', NOW(), 'AR'),
    ('melluso14', 'h046', 'Matias', 'Melluso', 'melluso@example.com', '1998-06-24', NOW(), 'AR'),
    ('sanchez3', 'h047', 'Guillermo', 'Sanchez', 'gsanchez@example.com', '1995-04-11', NOW(), 'UY'),
    ('colazo13', 'h048', 'Nicolas', 'Colazo', 'colazo@example.com', '1990-07-08', NOW(), 'AR'),
    ('soldano9', 'h049', 'Franco', 'Soldano', 'soldano@example.com', '1994-09-14', NOW(), 'AR'),
    ('conti24', 'h050', 'German', 'Conti', 'conti@example.com', '1994-04-03', NOW(), 'AR');


--- Datos para grupos, miembros de grupos, mensajes entre usuarios, publicaciones y publicaciones destacadas ---

INSERT INTO Grupos (nombre, exclusividad) VALUES
('Selección Argentina AFA', 'publico'),
('Club Atlético Vélez Sarsfield', 'publico'),
('Gimnasia y Esgrima La Plata', 'publico'),
('Fans del Futbol Argentino', 'publico'),
('Grupo Privado AFA', 'privado');

INSERT INTO miembros_de_grupos (nombre_usuario, id_grupo, fecha_desde, rol) VALUES
('lmessi', 1, '2020-01-01', 'administrador'),
('dibu_mtz', 1, '2020-01-01', 'miembro'),
('cuti_r', 1, '2020-01-01', 'miembro'),
('otamendi30', 1, '2020-01-01', 'miembro'),
('tagliafico3', 1, '2020-01-01', 'miembro'),
('molina26', 1, '2020-01-01', 'miembro'),
('paredes5', 1, '2020-01-01', 'miembro'),
('lmartinez22', 1, '2020-01-01', 'miembro'),
('dpaul7', 1, '2020-01-01', 'miembro'),
('locelso20', 1, '2020-01-01', 'miembro'),
('enzof', 1, '2020-01-01', 'miembro'),
('macallister10', 1, '2020-01-01', 'miembro'),
('alvarez9', 1, '2020-01-01', 'miembro'),
('garnacho17', 1, '2020-01-01', 'miembro'),
('buendia16', 1, '2020-01-01', 'miembro'),
('foyth2', 1, '2020-01-01', 'miembro'),
('lisandro6', 1, '2020-01-01', 'miembro'),
('senesi25', 1, '2020-01-01', 'miembro'),
('rulli12', 1, '2020-01-01', 'miembro'),
('armani1', 1, '2020-01-01', 'miembro'),
('montiel4', 1, '2020-01-01', 'miembro'),
('acuna8', 1, '2020-01-01', 'miembro'),
('dybala21', 1, '2020-01-01', 'miembro'),
('di_maria11', 1, '2020-01-01', 'miembro'),
('pezzella6', 1, '2020-01-01', 'miembro'),
('insfran23', 3, '2020-01-01', 'administrador'),
('giampaoli4', 3, '2020-01-01', 'miembro'),
('pintado15', 3, '2020-01-01', 'miembro'),
('suso6', 3, '2020-01-01', 'miembro'),
('corbalan2', 3, '2020-01-01', 'miembro'),
('pigretti33', 3, '2020-01-01', 'miembro'),
('rojas29', 3, '2020-01-01', 'miembro'),
('tarzia8', 3, '2020-01-01', 'miembro'),
('lescano10', 3, '2020-01-01', 'miembro'),
('castro11', 3, '2020-01-01', 'miembro'),
('bautista_g', 3, '2020-01-01', 'miembro'),
('benitez21', 3, '2020-01-01', 'miembro'),
('icht_santiago', 3, '2020-01-01', 'miembro'),
('miramon5', 3, '2020-01-01', 'miembro'),
('ramirez9', 3, '2020-01-01', 'miembro'),
('deblas7', 3, '2020-01-01', 'miembro'),
('cohen1', 3, '2020-01-01', 'miembro');

--- Amistades entre usuarios ---

INSERT INTO Amistades (usuario_solicitante, usuario_receptor, estado) VALUES
('lmessi', 'dibu_mtz', 'aceptada'),
('dibu_mtz', 'cuti_r', 'aceptada'),
('cuti_r', 'otamendi30', 'aceptada'),
('otamendi30', 'tagliafico3', 'aceptada'),
('tagliafico3', 'molina26', 'aceptada'),
('molina26', 'paredes5', 'aceptada'),
('paredes5', 'lmartinez22', 'aceptada'),
('lmartinez22', 'dpaul7', 'aceptada'),
('dpaul7', 'locelso20', 'aceptada'),
('locelso20', 'enzof', 'aceptada'),
('enzof', 'macallister10', 'aceptada'),
('macallister10', 'alvarez9', 'aceptada'),
('alvarez9', 'garnacho17', 'aceptada'),
('garnacho17', 'buendia16', 'aceptada'),
('buendia16', 'foyth2', 'aceptada'),
('foyth2', 'lisandro6', 'aceptada'),
('lisandro6', 'senesi25', 'aceptada'),
('senesi25', 'rulli12', 'aceptada'),
('rulli12', 'armani1', 'aceptada'),
('armani1', 'montiel4', 'aceptada'),
('montiel4', 'acuna8', 'aceptada'),
('acuna8', 'dybala21', 'aceptada'),
('dybala21', 'di_maria11', 'aceptada'),
('di_maria11', 'pezzella6', 'aceptada');

---- Mensajes entre usuarios ----

INSERT INTO Mensajes (contenido, fecha) VALUES
('Hola, ¿cómo estás?', NOW()),
('¿Viste el partido de anoche?', NOW()),
('¡Feliz cumpleaños!', NOW()),
('¿Quieres unirte a nuestro grupo?', NOW()),
('Nos vemos mañana en el entrenamiento.', NOW());

INSERT INTO Mensajes_Entre_Usuarios (id_mensaje, usuario_emisor, usuario_receptor) VALUES
(1, 'lmessi', 'dibu_mtz'),
(2, 'dibu_mtz', 'lmessi'),
(3, 'cuti_r', 'otamendi30'),
(4, 'otamendi30', 'tagliafico3'),
(5, 'tagliafico3', 'molina26');

---- Publicaciones en grupos y publicas -----

INSERT INTO publicaciones (autor, contenido, fecha_publicacion, fecha_actualizacion, tipo, id_grupo) VALUES
('lmessi', '¡Vamos Argentina!', NOW(), NOW(), 'Texto', 1),
('dibu_mtz', 'Gran atajada hoy.', NOW(), NOW(), 'Texto', 1),
('insfran23', 'Preparándonos para el próximo partido.', NOW(), NOW(), 'Texto', 3);

INSERT INTO publicaciones (autor, contenido, fecha_publicacion, fecha_actualizacion, tipo) VALUES
('pintado15', 'Orgulloso de representar a Uruguay.', NOW(), NOW(), 'Texto'),
('suso6', 'Disfrutando del fútbol en La Plata.', NOW(), NOW(), 'Texto'),
('corbalan2', 'Listo para dar lo mejor en la cancha.', NOW(), NOW(), 'Texto'),
('pigretti33', 'Trabajando duro cada día.', NOW(), NOW(), 'Texto'),
('rojas29', 'Feliz de estar en este equipo.', NOW(), NOW(), 'Texto');

INSERT INTO publicaciones_destacadas_por_usuarios (nombre_de_usuario, id_publicacion, fecha) VALUES
('lmessi', 1, NOW()),
('dibu_mtz', 2, NOW()),
('insfran23', 3, NOW()),
('pintado15', 4, NOW()),
('suso6', 5, NOW());


