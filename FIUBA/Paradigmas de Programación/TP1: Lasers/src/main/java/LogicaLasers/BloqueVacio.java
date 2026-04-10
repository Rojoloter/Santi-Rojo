package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class BloqueVacio implements Bloque {
    @Override
    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * devuelve un laser al siguiente lado en la direccion en la que vino, la direccion se mantiene igual.
         */
        Laser l = new Laser(filaLado,columnaLado,filaLado + direccionVertical, columnaLado + direccionHorizontal,direccionVertical,direccionHorizontal);
        List<Laser> laser = new ArrayList<Laser>();
        laser.add(l);
        return laser;
    }
    public TipoBloque getNombreBloque() {return TipoBloque.VACIO;}
}
