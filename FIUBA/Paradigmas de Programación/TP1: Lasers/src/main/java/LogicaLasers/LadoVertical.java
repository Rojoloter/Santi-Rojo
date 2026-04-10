package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class LadoVertical implements Lado {
    private final int fila;
    private final int columna;
    private final Celda izquierda;
    private final Celda derecha;
    private Objetivo objetivo;

    public LadoVertical(int fil, int colum, List<List<Celda>> celdas){
        /**
         * @param fila
         * @param columna  coordenadas donde se encuentra el lado
         * @param izquierda Celda que se encuentra izquierda del Lado
         * @param derecha Celda que se encuentra derecha del Lado
         * @param objetivo Objetivo que se contiene el lado (puede no contener ninguno)
         */
        fila = fil;
        columna = colum;
        objetivo = null;

        if(columna!=0){
            this.izquierda = celdas.get(fila/2).get((columna-1)/2); //[x/2][(y-1)/2];
        }else{
            this.izquierda = null;
        }

        if(columna != (celdas.getFirst().size())*2){
            this.derecha = celdas.get(fila/2).get((columna)/2); //[x/2][(y+1)/2];
        }else{
            derecha = null;
        }
    }

    @Override
    public List<Laser> interactuarLaser(int direccionVertical, int direccionHorizontal) {
        /**
         * metodo que a partir de la direccion de un laser, calcula si impacta con su celda de izquierda o derecha, la cual debe recibir el laser.
         * @return una lista de lasers para ser enviados en el tablero
         */
        if (objetivo != null){
            objetivo.activar();
        }

        if(direccionHorizontal == 1){
           if(derecha != null) {
               return derecha.recibirLaser(fila, columna, direccionVertical, direccionHorizontal);
           }
        }else if (izquierda != null){
            return izquierda.recibirLaser(fila, columna, direccionVertical, direccionHorizontal);
        }
        return new ArrayList<>();
    }

    public void setObjetivo(Objetivo obj){
        objetivo = obj;
    }
}
