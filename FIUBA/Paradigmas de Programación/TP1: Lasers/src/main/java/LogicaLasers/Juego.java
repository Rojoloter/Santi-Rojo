package LogicaLasers;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class Juego {
    private final List<Tablero> tableros;
    private Tablero tableroSeleccionado;

    public Juego(){
        /**
         * Constructor del Juego
         * @param tableros Coleccion de tableros, cada uno representa un nivel
         * @param tableroSeleccionado el nivel actual que se esta jugando
         */
        tableros = new ArrayList<>();
        File dir = new File("src/main/resources");
        File[] directoryListing = dir.listFiles();
        if (directoryListing != null) {
            for (File child : directoryListing) {
                tableros.add(new Tablero(child));
            }
        }
    }

    public void play(int nivel){
        /**
         * selecciona un nivel y lo juega.
         */
        tableroSeleccionado = tableros.get(nivel-1);
        tableroSeleccionado.jugar();
    }

    public void moverBloque(int filaOrigen,int columOrigen,int filaDest, int columDest){
        /**
         * mueve bloques dentro del nivel seleccionado.
         */
        if(tableroSeleccionado != null){
            tableroSeleccionado.moverBloq(filaOrigen,columOrigen,filaDest,columDest);
        }
    }

    public int getSizeTableros(){return tableros.size();}
    public Tablero getTablero(){return tableroSeleccionado;}
}
