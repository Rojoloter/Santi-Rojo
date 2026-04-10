package posts

import (
	"fmt"
	TDADiccionario "tdas/diccionario"
)

type posteo struct {
	usuario       string
	mensaje       string
	id            int
	usuariosLikes TDADiccionario.DiccionarioOrdenado[*Usuario, bool]
}

func CrearPost(mensaje string, id int, usuario string) Post {
	nuevoPost := new(posteo)
	nuevoPost.usuario = usuario
	nuevoPost.mensaje = mensaje
	nuevoPost.id = id
	nuevoPost.usuariosLikes = TDADiccionario.CrearABB[*Usuario, bool](comp)
	return nuevoPost
}

func (post *posteo) NombreUsuario() string {
	return post.usuario
}

func (post *posteo) Mensaje() string {
	return post.mensaje
}

func (post *posteo) CantidadLikes() int {
	return post.usuariosLikes.Cantidad()
}

func (post *posteo) ID() int {
	return post.id
}

func (post *posteo) NuevoLike(user *Usuario) {
	if !post.usuariosLikes.Pertenece(user) {
		post.usuariosLikes.Guardar(user, true)
	}
}

func comp(a, b *Usuario) int {
	if (*a).Nombre() > (*b).Nombre() {
		return 1
	}
	return -1 //Como es un diccionario no hay claves repetidas y no hace falta el caso a == b
}

func (post *posteo) UsuariosLikes() {
	fmt.Printf("El post tiene %d likes:\n", post.usuariosLikes.Cantidad())
	post.usuariosLikes.Iterar(func(clave *Usuario, dato bool) bool {
		{
			fmt.Printf("	%s\n", (*clave).Nombre())
			return dato
		}
	})
}
