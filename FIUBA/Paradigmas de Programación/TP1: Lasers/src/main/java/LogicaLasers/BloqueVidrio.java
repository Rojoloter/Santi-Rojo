package LogicaLasers;

import java.util.List;

public class BloqueVidrio implements Bloque {
    Bloque espejo = new BloqueEspejo();
    Bloque vacio = new BloqueVacio();

    //Un bloque de vidrio se comporta como la combinacion de un espejo y un vacio
    @Override
    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * devuelve dos lasers
         * el primero: al siguiente lado en la direccion en la que vino, la direccion se mantiene igual.
         * el segundo: tiene como destino el lado paralelo siguiente al origen con la misma direccion
         */
        List<Laser> l1 = espejo.recibirLaser(filaLado, columnaLado, direccionVertical, direccionHorizontal);
        List<Laser> l2 = vacio.recibirLaser(filaLado, columnaLado, direccionVertical, direccionHorizontal);
        l1.addAll(l2);
        return l1;
    }
    public TipoBloque getNombreBloque() {return TipoBloque.VIDRIO;}
}
