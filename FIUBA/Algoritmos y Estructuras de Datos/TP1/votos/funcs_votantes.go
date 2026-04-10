package votos

import (
	"rerepolez/errores"
	"strconv"
	"strings"
	"tdas/cola"
	"tdas/pila"
)

// Verifica que el DNI se encuentra en el padrón
func DNIEnPadron(arr []int, dni int) bool {
	piso := 0
	techo := len(arr) - 1
	for piso <= techo {
		medio := (piso + techo) / 2
		dni_medio := arr[medio]
		if dni_medio == dni {
			return true
		}
		if dni_medio > dni {
			techo = medio - 1
		} else {
			piso = medio + 1
		}

	}
	return false
}

// Verifica que el tipo de voto sea válido
func ValidezTipoVoto(voto string) bool {
	if voto != "Presidente" && voto != "Gobernador" && voto != "Intendente" {
		return false
	}
	return true
}

// Convierte un string a su correspondiente tipo de voto
func VotoTipoAString(voto string) TipoVoto {
	if voto == "Presidente" {
		return PRESIDENTE
	} else if voto == "Gobernador" {
		return GOBERNADOR
	}
	return INTENDENTE
}

// Convierte un tipo de voto a su correspondiente string
func VotoStringATipo(voto TipoVoto) string {
	if voto == PRESIDENTE {
		return "Presidente"
	} else if voto == GOBERNADOR {
		return "Gobernador"
	}
	return "Intendente"
}

// Permite ingresar a los votantes en la fila
func IngresarVotantes(input string, padrones []int, cola cola.Cola[Votante]) error {
	var err error
	var dni int
	split := strings.Split(input, " ")
	if len(split) != 2 {
		err = errores.DNIError{}
	} else {
		dni, err = strconv.Atoi(split[1])
		if err != nil {
			err = errores.DNIError{}
		} else if !DNIEnPadron(padrones, dni) {
			err = errores.DNIFueraPadron{}
		} else {
			nuevo_votante := CrearVotante(dni)
			cola.Encolar(nuevo_votante)
		}
	}
	return err
}

// Verifica que un string sea numerico
func EsNumerico(s string) bool {
	_, err := strconv.Atoi(s)
	return err == nil
}

// Verifica y guarda un nuevo voto individual
func NuevoVoto(input string, votante Votante, boletas []Partido) error {
	split := strings.Split(input, " ")
	var err error
	if len(split) == 3 {
		lista, _ := strconv.Atoi(split[2])
		if !ValidezTipoVoto(split[1]) {
			err = errores.ErrorTipoVoto{}
		} else if !EsNumerico(split[2]) || lista < 0 || lista >= len(boletas)-1 {
			err = errores.ErrorAlternativaInvalida{}
		} else {
			err = votante.Votar(VotoTipoAString(split[1]), lista)
		}
	}
	return err
}

// Guarda todos los votos del votante actual. Deberia ser llamado con el comando "fin-votar"
func VotarAlternativas(input string, votante Votante) (Voto, error) {
	voto, err := votante.FinVoto()
	return voto, err
}

// Decide si usar el string "voto" o "votos"
func VotoSingular(cant int) string {
	if cant == 1 {
		return "voto"
	}
	return "votos"
}

// Verifica que el nuevo votante no haya votado con anterioridad
func YaVoto(votante_nuevo Votante, pila_votados pila.Pila[Votante]) Votante {
	res := votante_nuevo
	pila_aux := pila.CrearPilaDinamica[Votante]()
	for !pila_votados.EstaVacia() {
		votado_viejo := pila_votados.Desapilar()
		if votado_viejo.LeerDNI() == votante_nuevo.LeerDNI() {
			res = votado_viejo
		}
		pila_aux.Apilar(votado_viejo)
	}
	for !pila_aux.EstaVacia() {
		pila_votados.Apilar(pila_aux.Desapilar())
	}
	return res
}

func MensajeFraudulento(dni int) string {
	chequeo_fraudulento := new(errores.ErrorVotanteFraudulento)
	chequeo_fraudulento.Dni = dni
	return chequeo_fraudulento.Error()
}
