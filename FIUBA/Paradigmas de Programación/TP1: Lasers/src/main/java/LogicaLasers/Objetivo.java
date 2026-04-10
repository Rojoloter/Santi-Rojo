package LogicaLasers;

public class Objetivo{
    private final int fila;
    private final int columna;
    private boolean activado;

    public Objetivo(int fila,int columna){
        /**
         * constructor de objetivo
         * @param fila
         * @param columna coordenadas donde se encuentra
         * @param activado indica si el objetivo fue activado por un laser
         */
        this.fila = fila;
        this.columna = columna;
        activado = false;
    }

    public boolean isActivado(){
        return activado;
    }

    public void activar(){activado = true;}
    
    public void desactivar(){
        activado = false;
    }

    public int getFila() {
        return fila;
    }

    public int getColumna() {
        return columna;
    }
}
