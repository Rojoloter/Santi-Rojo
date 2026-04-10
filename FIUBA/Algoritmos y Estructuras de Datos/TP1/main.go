package main

import (
	"bufio"
	"fmt"
	"os"
	"rerepolez/errores"
	"rerepolez/votos"
	"sort"
	"strconv"
	"strings"
	"tdas/cola"
	"tdas/pila"
)

// Convierte un slice de string a un slice de int
func SliceStringAInt(str []string) []int {
	res := make([]int, len(str))
	for i, s := range str {
		res[i], _ = strconv.Atoi(s)
	}
	return res
}

// Lee el input del usuario
func LeerInput() string {
	input := bufio.NewScanner(os.Stdin)
	input.Scan()
	res := input.Text()
	err := input.Err()
	if err != nil {
		fmt.Println(err)
	}
	return res
}

func AsignarInputs(input string, padrones []int, boletas []votos.Partido, fila cola.Cola[votos.Votante], cuarto_ocupado bool, votante votos.Votante, personas_votadas pila.Pila[votos.Votante]) (bool, votos.Votante) {
	var err error
	comando := (strings.Split(input, " "))[0]
	if comando == "ingresar" {
		err = votos.IngresarVotantes(input, padrones, fila)
		if err == nil {
			fmt.Print("OK\n")
		}
	} else if comando == "votar" {
		if fila.EstaVacia() && !cuarto_ocupado {
			err = errores.FilaVacia{}
		} else {
			if !cuarto_ocupado {
				cuarto_ocupado = true
				votante = votos.YaVoto(fila.Desencolar(), personas_votadas)
			}
			err = votos.NuevoVoto(input, votante, boletas)
			if err == nil {
				fmt.Print("OK\n")
			} else if err.Error() == votos.MensajeFraudulento(votante.LeerDNI()) {
				cuarto_ocupado = false
			}
		}
	} else if input == "fin-votar" {
		if fila.EstaVacia() && !cuarto_ocupado {
			err = errores.FilaVacia{}
		} else {
			var voto votos.Voto
			var errorVotando error
			if !cuarto_ocupado {
				votante = votos.YaVoto(fila.Desencolar(), personas_votadas)
			}
			voto, errorVotando = votos.VotarAlternativas(input, votante)
			cuarto_ocupado = false
			personas_votadas.Apilar(votante)

			if errorVotando == nil {
				votos.SumarVotosPartidos(voto, boletas)

				fmt.Print("OK\n")
			} else {
				err = errorVotando
			}
		}
	} else if input == "deshacer" {
		if fila.EstaVacia() && !cuarto_ocupado {
			err = errores.FilaVacia{}
		} else {
			if !cuarto_ocupado {
				votante = votos.YaVoto(fila.Desencolar(), personas_votadas)
				cuarto_ocupado = true
			}
			err = votante.Deshacer()
		}
		if err == nil {

			fmt.Print("OK\n")
		} else if err.Error() == votos.MensajeFraudulento(votante.LeerDNI()) {
			cuarto_ocupado = false
		}
	}
	if err != nil {
		fmt.Println(err.Error())
	}
	return cuarto_ocupado, votante
}

func main() {
	archivos := os.Args
	partidos, padrones_str, err_partido, err_padron := votos.AbrirPadronYPartidos(archivos)
	padrones_int := SliceStringAInt(padrones_str)
	sort.Ints(padrones_int)
	if err_partido != nil || err_padron != nil {
		if err_padron != nil {
			fmt.Println(err_padron.Error())
		} else if err_partido != nil {
			fmt.Println(err_partido.Error())
		}
	} else {
		var cuarto_ocupado bool
		boletas := votos.CrearPartidos(partidos)
		fila := cola.CrearColaEnlazada[votos.Votante]()
		input := bufio.NewScanner(os.Stdin)
		var votante votos.Votante
		personas_votadas := pila.CrearPilaDinamica[votos.Votante]()
		for input.Scan() {
			cuarto_ocupado, votante = AsignarInputs(input.Text(), padrones_int, boletas, fila, cuarto_ocupado, votante, personas_votadas)
		}
		if !fila.EstaVacia() {
			fmt.Println(errores.ErrorCiudadanosSinVotar{}.Error())
		}
		votos.Imprimir(boletas)
	}
}
