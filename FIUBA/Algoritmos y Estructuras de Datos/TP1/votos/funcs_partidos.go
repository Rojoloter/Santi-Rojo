package votos

import (
	"bufio"
	"fmt"
	"os"
	"rerepolez/errores"
	"strings"
)

// Abre un archivo de una ruta seleccionada
func LeerArchivo(ruta string) ([]string, error) {
	var res []string
	archivo, err := os.Open(ruta)
	if err != nil {
		return res, errores.ErrorLeerArchivo{}
	}
	defer archivo.Close()
	scanner := bufio.NewScanner(archivo)
	for scanner.Scan() {
		linea := scanner.Text()
		res = append(res, linea)
	}
	return res, err
}

// Abre los archivos de partidos y padrones
func AbrirPadronYPartidos(argumentos []string) ([]string, []string, error, error) {
	var (
		partido, padron         []string
		err_padron, err_partido error
	)
	if len(argumentos) != 3 {
		err_partido = errores.ErrorParametros{}
	} else {
		partido, err_partido = LeerArchivo(argumentos[1])
		padron, err_padron = LeerArchivo(argumentos[2])
	}
	return partido, padron, err_partido, err_padron
}

// Crea un struct Partido por cada partido leído ??
func CrearPartidos(partidos []string) []Partido {
	var res []Partido
	res = append(res, CrearVotosEnBlanco())
	for i := 0; i < len(partidos); i++ {
		infoPartido := partidos[i]
		split := strings.Split(infoPartido, ",")
		var candidatos []string
		for i := 1; i <= int(CANT_VOTACION); i++ {
			candidatos = append(candidatos, split[i])
		}
		nuevoPartido := CrearPartido(split[0], [CANT_VOTACION]string(candidatos))
		res = append(res, nuevoPartido)
	}
	ListaImpugnada := CrearVotosEnBlanco()
	res = append(res, ListaImpugnada)
	//Este append puede ser confuso.
	//Basicamente el array res esta conformado por [VotosEnBlanco, lista 1, lista 2... lista n, Impugnados].
	//arr[0], esta reservada a los votos en blanco. Despues le siguen las listas cuyo numero para acceder al slice corresponde
	// a su numero de lista (por ej la lista 1 esta en arr[1], la lista 2 en arr[2] etc).
	// Y por ultimo una lista que recopila todos los votos impugnados.
	// Uso una lista de votos en blanco para aprovechar que ya esta creada nomas, todos los votos impugnados van a sumar 1
	// Al presidente de esta pseudolista. Esto es para despues poder imprimir la cantidad de impugnados
	return res
}

// le suma los votos al partido correspondiente
func SumarVotosPartidos(voto Voto, partidos []Partido) {
	if voto.Impugnado {
		partidos[len(partidos)-1].VotadoPara(PRESIDENTE)
	} else {
		for i := 0; i < int(CANT_VOTACION); i++ {
			partidos[voto.VotoPorTipo[i]].VotadoPara(TipoVoto(i))
		}
	}
}

// Imprime la cantidad de votos finales
func Imprimir(partidos []Partido) {
	//Para esta funcion fueron agregadas dos primitivas en partido.go
	for i := 0; i < int(CANT_VOTACION); i++ {
		//Imprime el tipo de voto (Presidente, Gobernador etc)
		fmt.Printf("%s:\n", VotoStringATipo(TipoVoto(i)))
		//Imprime los votos en blanco del tipo
		fmt.Printf("%s: %d %s\n", partidos[0].ObtenerNombre(), partidos[0].ObtenerResultado(TipoVoto(i)), VotoSingular(partidos[0].ObtenerResultado(TipoVoto(i))))
		for j := 1; j < len(partidos)-1; j++ {
			fmt.Printf("%s - %s: %d %s\n", partidos[j].ObtenerNombre(), partidos[j].ObtenerCandidatos(TipoVoto(i)), partidos[j].ObtenerResultado(TipoVoto(i)), VotoSingular(partidos[j].ObtenerResultado(TipoVoto(i))))
		}
		//Deja un renglon en blanco antes de pasar al proximo tipo
		fmt.Print("\n")
	}
	//Imprime los votos impugnados totales
	fmt.Println("Votos Impugnados:", partidos[len(partidos)-1].ObtenerResultado(PRESIDENTE), VotoSingular(partidos[len(partidos)-1].ObtenerResultado(PRESIDENTE)))
}
