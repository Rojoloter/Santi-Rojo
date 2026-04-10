package LogicaLasers;

import java.util.List;

public interface Bloque {

    List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal);
    TipoBloque getNombreBloque();
}





