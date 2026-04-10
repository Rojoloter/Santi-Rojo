package main

import (
	"algogram/posts"
	"bufio"
	"fmt"
	"os"
	"strings"
	TDADiccionario "tdas/diccionario"
)

func AsignarInputs(input string, diccUsuarios TDADiccionario.Diccionario[string, *posts.Usuario], yaLoggeado bool, usuarioActual *posts.Usuario, ID int, diccPosts TDADiccionario.Diccionario[int, *posts.Post]) (bool, *posts.Usuario, int) {
	var err error
	comando := (strings.Split(input, " "))[0]
	if comando == "login" {
		yaLoggeado, usuarioActual, err = posts.Login(input, diccUsuarios, yaLoggeado, usuarioActual)
	} else if comando == "logout" {
		yaLoggeado, err = posts.Logout(yaLoggeado)
	} else if comando == "publicar" {
		ID, err = posts.Publicar(yaLoggeado, input, ID, usuarioActual, diccPosts, diccUsuarios)
	} else if comando == "ver_siguiente_feed" {
		err = posts.VerSiguienteFeed(yaLoggeado, usuarioActual)
	} else if comando == "likear_post" {
		err = posts.LikearPost(yaLoggeado, input, diccPosts, usuarioActual)
	} else if comando == "mostrar_likes" {
		err = posts.MostrarLikes(input, diccPosts)
	}
	if err != nil {
		fmt.Println(err.Error())
	}
	return yaLoggeado, usuarioActual, ID
}

func main() {
	archivoUsuarios := os.Args
	diccUsuarios, err := posts.CrearUsuarios(archivoUsuarios)
	diccPosts := TDADiccionario.CrearHash[int, *posts.Post]()
	if err != nil {
		fmt.Println(err.Error())
		diccUsuarios = nil
	} else {
		var yaLoggeado bool
		var ID int
		var usuarioActual *posts.Usuario
		input := bufio.NewScanner(os.Stdin)
		for input.Scan() {
			yaLoggeado, usuarioActual, ID = AsignarInputs(input.Text(), diccUsuarios, yaLoggeado, usuarioActual, ID, diccPosts)
		}
	}
}
