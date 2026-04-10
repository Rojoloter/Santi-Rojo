-- Usuario administrador
CREATE ROLE administrador
   WITH LOGIN
   SUPERUSER
   PASSWORD 'admin123';


-- Usuario normal
CREATE ROLE usuario_redsocial
   WITH LOGIN
   NOSUPERUSER
   PASSWORD 'usuario123';

-- Permisos al usuario para poder realizar inserciones en las sig. tablas.
GRANT SELECT, INSERT, UPDATE, DELETE ON Publicaciones TO usuario_redsocial;
GRANT SELECT, INSERT, UPDATE, DELETE ON Grupos TO usuario_redsocial;
GRANT SELECT, INSERT, UPDATE, DELETE ON Mensajes TO usuario_redsocial;

GRANT SELECT, INSERT, UPDATE, DELETE ON Mensajes_Entre_Usuarios TO usuario_redsocial;
GRANT SELECT, INSERT, UPDATE, DELETE ON miembros_de_grupos TO usuario_redsocial;
GRANT SELECT, INSERT, UPDATE, DELETE ON publicaciones_destacadas_por_usuarios TO usuario_redsocial;