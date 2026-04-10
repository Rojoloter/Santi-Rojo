package LogicaLasers;

public class Laser {
    private final int filaInicio;
    private final int columInicio;
    private final int filaFin;
    private final int columFin;
    private final int directV;
    private final int directH;

    public Laser(int inicioFila,int inicioCol,int finFila, int finCol,int directVertical,int directHorizontal){
        /**
         * constructor Laser
         * @param Inicio indican coordenas de origen del laser
         * @param Fin indican coordenadas destino del laser
         * @param directVertical indica la direccion en la que se desplaza el laser verticalmente (1 = South, -1 = North)
         * @param directHorizontal indica la direccion en la que se desplaza el laser horizontalmente (1 = East, -1 = West)
         */
        filaInicio = inicioFila;
        columInicio = inicioCol;
        filaFin = finFila;
        columFin = finCol;
        directV = directVertical;
        directH = directHorizontal;
    }

    public int getFilaInicio() { return filaInicio; }

    public int getColumInicio() {
        return columInicio;
    }

    public int getFilaFin() {
        return filaFin;
    }

    public int getColumFin() {return columFin;}

    public int getDirectV() {
        return directV;
    }

    public int getDirectH() {
        return directH;
    }
}
