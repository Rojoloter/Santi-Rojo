package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class BloqueCristal implements Bloque {

    @Override
    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * devuelve un laser que tiene como destino el lado paralelo siguiente al origen con la misma direccion
         */
        Laser l;

        //El laser lo recibió un lado horizontal
        if (filaLado % 2 == 0 && columnaLado % 2 == 1) {
            l = new Laser(filaLado,columnaLado,filaLado + direccionVertical *2, columnaLado,direccionVertical,direccionHorizontal);
        //El laser lo recibió un lado vertical
        } else {
            l = new Laser(filaLado,columnaLado,filaLado,columnaLado +direccionHorizontal*2,direccionVertical,direccionHorizontal);
        }

        List<Laser> laser = new ArrayList<Laser>();
        laser.add(l);
        return laser;
    }

    @Override
    public TipoBloque getNombreBloque() {return TipoBloque.CRISTAL;}
}
