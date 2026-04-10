package votos

type partidoImplementacion struct {
	nombre_partido   string
	candidatos       [CANT_VOTACION]string
	votos_presidente int
	votos_gobernador int
	votos_intendente int
}

type partidoEnBlanco struct {
	presidente_blanco int
	gobernador_blanco int
	intendente_blanco int
}

func CrearPartido(nombre string, candidatos [CANT_VOTACION]string) Partido {
	partido := new(partidoImplementacion)
	partido.nombre_partido = nombre
	partido.candidatos = candidatos
	return partido
}

func CrearVotosEnBlanco() Partido {
	partido := new(partidoEnBlanco)
	return partido
}

func (partido *partidoImplementacion) VotadoPara(tipo TipoVoto) {
	if tipo == 0 {
		partido.votos_presidente++
	} else if tipo == 1 {
		partido.votos_gobernador++
	} else {
		partido.votos_intendente++
	}
}

func (partido partidoImplementacion) ObtenerResultado(tipo TipoVoto) int {
	if tipo == 0 {
		return partido.votos_presidente
	} else if tipo == 1 {
		return partido.votos_gobernador
	} else {
		return partido.votos_intendente
	}
}

func (partido partidoImplementacion) ObtenerNombre() string {
	return partido.nombre_partido
}

func (partido partidoImplementacion) ObtenerCandidatos(tipo TipoVoto) string {
	return partido.candidatos[tipo]
}

func (blanco *partidoEnBlanco) VotadoPara(tipo TipoVoto) {
	if tipo == 0 {
		blanco.presidente_blanco++
	} else if tipo == 1 {
		blanco.gobernador_blanco++
	} else {
		blanco.intendente_blanco++
	}
}

func (blanco partidoEnBlanco) ObtenerResultado(tipo TipoVoto) int {
	if tipo == 0 {
		return blanco.presidente_blanco
	} else if tipo == 1 {
		return blanco.gobernador_blanco
	} else {
		return blanco.intendente_blanco
	}
}

func (partido partidoEnBlanco) ObtenerNombre() string {
	return "Votos en Blanco"
}

func (partido partidoEnBlanco) ObtenerCandidatos(tipo TipoVoto) string {
	return "Blanco"
}
