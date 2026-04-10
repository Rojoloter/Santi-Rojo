package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class BloqueEspejo implements Bloque {

    @Override
    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * devuelve un laser cuyo destino es igual al origen.
         * en el caso de un lado horizontal invierte la direccion vertical.
         * en el caso de un lado vertical invierte la direccion horizontal
         */
        Laser l;
        if (filaLado % 2 == 0 && columnaLado % 2 == 1) {//El laser lo recibió un lado horizontal
            l = new Laser(filaLado,columnaLado,filaLado,columnaLado,-direccionVertical,direccionHorizontal); //Sur se convierte a Norte y viceversa
        } else { //El laser lo recibió un lado vertical
            l = new Laser(filaLado,columnaLado,filaLado,columnaLado,direccionVertical,-direccionHorizontal); //Este se convierte en Oeste y viceversa
        }
        List<Laser> laser = new ArrayList<Laser>();
        laser.add(l);
        return laser;
    }
    public TipoBloque getNombreBloque() {return TipoBloque.ESPEJO;}
}
