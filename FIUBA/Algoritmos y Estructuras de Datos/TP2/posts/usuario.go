package posts

type Usuario interface {

	//Devuelve el nombre del usuario
	Nombre() string

	//Guarda los posteos de otros usuarios
	NuevoPosteo(post *Post, indice int)

	//Devuelve el indice que tenía en el archivo de entrada
	Indice() int

	//Contiene un Heap de posteos ordenados por la prioridad del usuario
	ProxPost() (*Post, error)
}
