package posts

import (
	"algogram/errores"
	TDAHeap "tdas/heap/cola_prioridad"
)

type postPrioridad struct {
	prioridad int
	post      *Post
}

type user struct {
	nombre string
	indice int
	feed   TDAHeap.ColaPrioridad[postPrioridad]
}

func CrearUsuario(nombre string, indice int) Usuario {
	nuevoUser := new(user)
	nuevoUser.nombre = nombre
	nuevoUser.indice = indice
	nuevoUser.feed = TDAHeap.CrearHeap[postPrioridad](cmp)
	return nuevoUser
}

// En caso de que las prioridades sean iguales, el heap va a ordenar por ID,
// ya que el ID mas pequeño corresponde al post mas antiguo
func cmp(a, b postPrioridad) int {
	if a.prioridad != b.prioridad {
		return int(b.prioridad - a.prioridad)
	}
	return (*b.post).ID() - (*a.post).ID()
}

func (usuario *user) Nombre() string {
	return usuario.nombre
}

func absInt(a, b int) int { //Creamos nuestra propia funcion de modulo en vez de usar math.Abs, porque esa funcion utiliza float64, que ocupa mas memoria que int
	if a > b {
		return a - b
	}
	return b - a
}

func (usuario *user) NuevoPosteo(post *Post, indice int) {
	var nuevoPost postPrioridad
	nuevoPost.prioridad = absInt(usuario.indice, indice)
	nuevoPost.post = post
	usuario.feed.Encolar(nuevoPost)
}

func (usuario *user) Indice() int {
	return usuario.indice
}

func (usuario *user) ProxPost() (*Post, error) {
	if usuario.feed.EstaVacia() {
		err := new(errores.ErrorNoLoggeadoOSinPosts)
		return nil, err
	}
	res := usuario.feed.Desencolar().post
	return res, nil
}
