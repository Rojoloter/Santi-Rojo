package posts

// Post contiene la informacion de cada posteo
type Post interface {

	//Devuelve el nombre del usuario que posteó la publicación
	NombreUsuario() string

	//Devuelve el mensaje del posteo
	Mensaje() string

	//Devuelve el ID del posteo
	ID() int

	//Agrega un like a la publicacion
	NuevoLike(User *Usuario)

	//Devuelve la cantidad de likes del posteo
	CantidadLikes() int

	//Devuelve, en orden alfabetico, un heap de usuarios que likearon el post, para luego ser utilizado en la impresion
	UsuariosLikes()
}
