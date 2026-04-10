package posts

import (
	"algogram/errores"
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	TDADiccionario "tdas/diccionario"
)

func CrearUsuarios(ruta []string) (TDADiccionario.Diccionario[string, *Usuario], error) {
	var err error
	res := TDADiccionario.CrearHash[string, *Usuario]()
	if len(ruta) != 2 {
		res = nil
		return res, errores.ErrorParametros{}
	}
	archivo, err := os.Open(ruta[1])
	if err != nil {
		res = nil
		return res, errores.ErrorLeerArchivo{}
	}
	defer archivo.Close()
	scanner := bufio.NewScanner(archivo)
	var cont int
	for scanner.Scan() {
		nombre := scanner.Text()
		nuevoUsuario := CrearUsuario(nombre, cont)
		res.Guardar(nombre, &nuevoUsuario)
		cont++
	}
	return res, err
}

func ImprimirPost(post Post) {
	fmt.Printf("Post ID %d\n", post.ID())
	fmt.Printf("%s dijo: %s\n", post.NombreUsuario(), post.Mensaje())
	fmt.Printf("Likes: %d\n", post.CantidadLikes())
}

func Login(input string, diccUsuarios TDADiccionario.Diccionario[string, *Usuario], yaLoggeado bool, usuarioActual *Usuario) (bool, *Usuario, error) {
	var err error
	if len(strings.Split(input, " ")) < 2 || !diccUsuarios.Pertenece(strings.Join((strings.Split(input, " "))[1:], " ")) {
		err = new(errores.ErrorUsuarioInexistente)
	} else if yaLoggeado {
		err = new(errores.ErrorUsuarioLoggeado)
	} else {
		usuarioActual = diccUsuarios.Obtener(strings.Join((strings.Split(input, " "))[1:], " "))
		yaLoggeado = true
		fmt.Printf("Hola %s\n", (*usuarioActual).Nombre())
	}
	return yaLoggeado, usuarioActual, err
}

func Logout(yaLoggeado bool) (bool, error) {
	var err error
	if !yaLoggeado {
		err = new(errores.ErrorUsuarioNoLoggeado)
	} else {
		yaLoggeado = false
		fmt.Print("Adios\n")
	}
	return yaLoggeado, err
}

func Publicar(yaLoggeado bool, input string, ID int, usuarioActual *Usuario, diccPosts TDADiccionario.Diccionario[int, *Post], diccUsuarios TDADiccionario.Diccionario[string, *Usuario]) (int, error) {
	var err error
	if !yaLoggeado {
		err = new(errores.ErrorUsuarioNoLoggeado)
	} else {
		nuevoMensaje := (strings.Split(input, " "))[1:]
		nuevoPost := CrearPost(strings.Join(nuevoMensaje, " "), ID, (*usuarioActual).Nombre())
		diccPosts.Guardar(ID, &nuevoPost) //La clave del diccionario es un string en vez de un int para que al likear un post no haya que convertir de int a str, que hay que verificar errores
		//Para aclarar un poco la lógica de esto: Todos los usuarios tienen una prioridad de publicaciones distinto,
		//entonces lo que se hace es: Primero, cada usuario esta identificado con el indice que tiene en el archivo de entrada.
		//A su vez, cada usuario tiene un "feed personalizado" que tiene, en orden de prioridad, los posts del resto de usuarios
		//(Si la prioridad es la misma, se ordena por antigüedad utilizando el ID de la publicacion).
		//Cada vez que alguien postea, ese post se le agrega a los feeds del resto de usuarios, junto con el indice del usuario que lo posteó.
		//Esto se hace para que el Heap interno detras de cada feed pueda ir ordenando dependiendo los indices (o IDs) de los usuarios (o posts).
		//Cabe aclarar que esto no tiene nada que ver con el diccPosts.
		//Ese diccionario tiene como clave el ID de cada posteo, y solo se usa para encontrarlo en caso de mostrar_likes.
		diccUsuarios.Iterar(func(clave string, dato *Usuario) bool {
			if (*usuarioActual).Nombre() != clave {
				(*dato).NuevoPosteo(&nuevoPost, (*usuarioActual).Indice())
			}
			return true
		})
		ID++
		fmt.Print("Post publicado\n")
	}
	return ID, err
}

func VerSiguienteFeed(yaLoggeado bool, usuarioActual *Usuario) error {
	var err error
	if !yaLoggeado {
		err = new(errores.ErrorNoLoggeadoOSinPosts)
	} else {
		var proxPost *Post
		proxPost, err = (*usuarioActual).ProxPost()
		if err == nil {
			ImprimirPost(*proxPost)
		}
	}
	return err
}

func LikearPost(yaLoggeado bool, input string, diccPosts TDADiccionario.Diccionario[int, *Post], usuarioActual *Usuario) error {
	var err error
	indice, err := strconv.Atoi(strings.Split(input, " ")[1])
	if !yaLoggeado || len(strings.Split(input, " ")) != 2 || err != nil || !diccPosts.Pertenece(indice) {
		err = new(errores.ErrorNoLoggeadoOInexistente)
	} else {
		posteo := diccPosts.Obtener(indice)
		post := *posteo
		post.NuevoLike(usuarioActual)
		fmt.Print("Post likeado\n")
	}
	return err
}

func MostrarLikes(input string, diccPosts TDADiccionario.Diccionario[int, *Post]) error {
	var err error
	indice, err := strconv.Atoi(strings.Split(input, " ")[1])
	if len(strings.Split(input, " ")) != 2 || err != nil || !diccPosts.Pertenece(indice) {
		err = new(errores.ErrorInexistenteOSinLikes)
	} else {
		posteo := *diccPosts.Obtener(indice)
		if posteo.CantidadLikes() == 0 {
			err = new(errores.ErrorInexistenteOSinLikes)
		} else {
			posteo.UsuariosLikes()

		}
	}
	return err
}
