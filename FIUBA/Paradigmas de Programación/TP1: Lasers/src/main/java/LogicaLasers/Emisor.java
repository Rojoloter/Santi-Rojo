package LogicaLasers;

public class Emisor{
    private final int filaOrigen;
    private final int columnaOrigen;
    private int direccionVertical;
    private int direccionHorizontal;



    public Emisor(int filaOrigen,int columnaOrigen,String direccion){
        /**
         * constructor de Emisor
         * @param Origen coordenada donde se encuentra el emisor
         *@param direccionVertical indica la direccion en la que se desplazara el laser a enviar verticalmente (1 = South, -1 = North)
         *@param direccionHorizontal indica la direccion en la que se desplazara el laser a enviar horizontalmente (1 = East, -1 = West)
         */
        this.filaOrigen = filaOrigen;
        this.columnaOrigen = columnaOrigen;

        direccionVertical = 1;
        if(direccion.toCharArray()[0] == 'N'){
            direccionVertical = -1;
        }

        direccionHorizontal = 1;
        if(direccion.toCharArray()[1] == 'W'){
            direccionHorizontal = -1;
        }
    }

    public Laser EnviarLaser(){
        return new Laser(filaOrigen,columnaOrigen,filaOrigen,columnaOrigen,direccionVertical,direccionHorizontal);
    }

    public int getColumna() {
        return columnaOrigen;
    }

    public int getFila() {
        return filaOrigen;
    }
}
