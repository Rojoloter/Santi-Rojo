package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class BloqueOpaco implements Bloque {

    //No hace nada con el laser que recibe
    @Override
    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * absorbe el laser, devuelve una lista de lasers vacia
         */
        return new ArrayList<>();
    }
    public TipoBloque getNombreBloque() {return TipoBloque.OPACO;}
}