package LogicaLasers;

import java.util.List;

public class Celda {
    private Bloque bloque;
    private final boolean esMovil;

    public Celda (Bloque bloque, boolean esMovil) {
        /**
         * constructor de Celda
         * @param bloque Contiene un bloque el cual se utiliza para interactuar con el laser
         * @param esMovil boolean que indica si la celda puede cambiar su bloque
         */
        this.bloque = bloque;
        this.esMovil = esMovil;
    }

    public List<Laser> recibirLaser(int filaLado, int columnaLado, int direccionVertical, int direccionHorizontal) {
        /**
         * este metodo se llama a traves de la clase Lado.
         * @return una lista de Laser enviados por su bloque contenido.
         */
        return bloque.recibirLaser(filaLado, columnaLado, direccionVertical, direccionHorizontal);
    }

    public void ponerBloque(Celda celdaOrigen) {
        if (celdaOrigen.esMovil && esMovil) { //Solo se puede mover un bloque de una celda movil a otra celda movil
            Bloque bloqueOrigen = celdaOrigen.getBloque();
            Bloque bloqueActual = this.bloque;
            this.bloque = bloqueOrigen;
            celdaOrigen.setBloque(bloqueActual);
        }
    }

    public Bloque getBloque() {
        return this.bloque;
    }

    private void setBloque(Bloque nuevoBloque) {
        this.bloque = nuevoBloque;
    }

    public boolean esMovil() {
        return esMovil;
    }

    public TipoBloque getNombreBloque(){return bloque.getNombreBloque();}
}




