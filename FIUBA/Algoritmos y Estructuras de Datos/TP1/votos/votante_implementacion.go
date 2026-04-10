package votos

import (
	"rerepolez/errores"
	"tdas/pila"
)

type boleta struct {
	tipo        TipoVoto
	alternativa int
}

type votanteImplementacion struct {
	dni    int
	votos  Voto
	pila   pila.Pila[boleta]
	votado bool //verifica que no haya votado con anterioridad
}

func CrearVotante(dni int) Votante {
	votante := new(votanteImplementacion)
	votante.dni = dni
	votante.pila = pila.CrearPilaDinamica[boleta]()
	return votante
}

func (votante votanteImplementacion) LeerDNI() int {
	return votante.dni
}

func (votante *votanteImplementacion) Votar(tipo TipoVoto, alternativa int) error {
	if votante.votado {
		error_fraudulento := new(errores.ErrorVotanteFraudulento)
		error_fraudulento.Dni = votante.dni
		return error_fraudulento
	}

	if alternativa == 0 {
		votante.votos.Impugnado = true
	}
	var voto boleta
	voto.tipo = tipo
	voto.alternativa = alternativa
	votante.pila.Apilar(voto)
	return nil
}

// Devuelve true si hay mas impugnaciones en los votos
func verificarImpugnaciones(pila_original pila.Pila[boleta]) bool {
	pila_aux := pila.CrearPilaDinamica[boleta]()
	var res bool
	for !pila_original.EstaVacia() {
		voto := pila_original.Desapilar()
		if voto.alternativa == 0 {
			res = true
		}
		pila_aux.Apilar(voto)
	}
	for !pila_aux.EstaVacia() {
		pila_original.Apilar(pila_aux.Desapilar())
	}
	return res
}

func (votante *votanteImplementacion) Deshacer() error {
	if votante.votado {
		error_fraudulento := new(errores.ErrorVotanteFraudulento)
		error_fraudulento.Dni = votante.dni
		return error_fraudulento
	}
	if votante.pila.EstaVacia() {
		return errores.ErrorNoHayVotosAnteriores{}
	}
	if votante.votado {
		return errores.ErrorVotanteFraudulento{}
	}

	voto := votante.pila.Desapilar()
	if voto.alternativa == 0 && !verificarImpugnaciones(votante.pila) {
		votante.votos.Impugnado = false
	}
	return nil
}

func (votante *votanteImplementacion) FinVoto() (Voto, error) {
	if votante.votado {
		error_fraudulento := new(errores.ErrorVotanteFraudulento)
		error_fraudulento.Dni = votante.dni
		return votante.votos, error_fraudulento
	}
	for !votante.pila.EstaVacia() && !votante.votos.Impugnado {
		voto := votante.pila.Desapilar()
		if votante.votos.VotoPorTipo[voto.tipo] != 0 {
			continue
		}
		votante.votos.VotoPorTipo[voto.tipo] = voto.alternativa
	}
	votante.votado = true
	return votante.votos, nil
}
