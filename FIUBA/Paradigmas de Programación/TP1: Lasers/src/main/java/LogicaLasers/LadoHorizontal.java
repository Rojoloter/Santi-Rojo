package LogicaLasers;

import java.util.ArrayList;
import java.util.List;

public class LadoHorizontal implements Lado {
    private final int fila;
    private final int columna;
    private final Celda arriba;
    private final Celda abajo;
    private Objetivo objetivo;

    public LadoHorizontal(int fil, int colum, List<List<Celda>> celdas){
        /**
         * @param fila
         * @param columna  coordenadas donde se encuentra el lado
         * @param arriba Celda que se encuentra arriba del Lado
         * @param abajo Celda que se encuentra abajo del Lado
         * @param objetivo Objetivo que se contiene el lado (puede no contener ninguno)
         */
        this.fila = fil;
        this.columna = colum;
        objetivo = null;

        if(fila != 0){
            this.arriba = celdas.get((fila-1)/2).get(columna/2);
        }else{
            this.arriba = null;
        }

        if(fila != celdas.toArray().length*2){
            this.abajo = celdas.get(fila/2).get(columna/2);
        }else{
            this.abajo = null;
        }
    }

    @Override
    public List<Laser> interactuarLaser(int direccionVertical, int direccionHorizontal) {
        /**
         * metodo que a partir de la direccion de un laser, calcula si impacta con su celda de arriba o abajo, la cual debe recibir el laser
         * @return una lista de lasers para ser enviados en el tablero
         */
        if (objetivo != null){
            objetivo.activar();
        }

        if(direccionVertical == 1){
            if(abajo != null) {
                return abajo.recibirLaser(fila, columna, direccionVertical, direccionHorizontal);
            }
        }else if(arriba != null){
            return arriba.recibirLaser(fila, columna, direccionVertical, direccionHorizontal);
        }
        return new ArrayList<>();
    }

    public void setObjetivo(Objetivo obj){
        objetivo = obj;
    }
}
