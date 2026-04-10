package LogicaLasers;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

public class Tablero {
    private Lado[][] lados;
    private List<List<Celda>> celdas;
    private List<Emisor> emisores;
    private List<Objetivo> objetivos;
    private final List<Laser> lasers;

    Tablero(File nivel){
        /**
         * Constructor de tablero a partir de un archivo con el formato de un nivel.
         * @param lados matriz donde se encuentran un Lado en las coordenadas par-impar(horizontal) o impar-par (vertical).
         * @param celdas matriz de Celda, usa un sistema distinto de coordenadas donde cada celda mide 1x1 en lugar de 2x2.
         * @param emisores lista de Emisor, se utiliza para enviar los lasers al inicio del nivel.
         * @param objetivos lista de Objetivo, se utiliza para verificar si el jugador consiguio la victoria.
         * @param lasers lista de Laser, permite tener un registro del trazado que hizo el laser en el nivel.
         */
        leerArchivo(nivel);
        armarLados(celdas.size() , celdas.getFirst().size());
        setObjetivos();
        lasers = new ArrayList<>();
    }

    private void leerArchivo(File nivel){
        /**
         * funcion para leer el archivo y separarlo entre seccion celdas y objetivosYEmisores
         */
        try {
            List<String> lineas = Files.readAllLines(nivel.toPath());
            boolean lineaVaciaEncontrada = false;
            ArrayList<String> primeraSeccion = new ArrayList<>();
            ArrayList<String> segundaSeccion = new ArrayList<>();
            for (String linea : lineas){
                if(linea.isEmpty()){
                    lineaVaciaEncontrada = true;
                    continue;
                }
                if (!lineaVaciaEncontrada){
                    if (!primeraSeccion.isEmpty() && linea.length() < primeraSeccion.getFirst().length()) { //Hay niveles que terminan en espacio (celda sin piso) y no se estaban agregando
                        for (int i = 0; i < primeraSeccion.getFirst().length() - linea.length(); i++) {
                            linea = linea.concat(" ");
                        }
                    }
                    primeraSeccion.add(linea);
                }else{
                    segundaSeccion.add(linea);
                }
            }
            cargarNivel(primeraSeccion,segundaSeccion);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    private void cargarNivel(List<String> primeraSeccion, List<String> segundaSeccion){
        armarCeldas(primeraSeccion);
        objetivosYemisores(segundaSeccion);
    }
    private void armarCeldas(List<String> lineas){
        /**
         * metodo que instancia las celdas y forma la matriz celdas.
         * a cada celda se le asigna su bloque correspondiente (VACIO, OPACO, ESPEJO, VIDRIO O CRISTAL) y se declara como movil o inmovil
         */
        celdas = new ArrayList<>();
        for (String linea : lineas){
            var fila = new ArrayList<Celda>();
            for (char c : linea.toCharArray()){

                switch (c){
                    case ' '-> fila.add(new Celda(new BloqueVacio(), false));
                    case '.'-> fila.add(new Celda(new BloqueVacio(), true));
                    case 'F'-> fila.add(new Celda(new BloqueOpaco(), false));
                    case 'B'-> fila.add(new Celda(new BloqueOpaco(), true));
                    case 'R'-> fila.add(new Celda(new BloqueEspejo(), true));
                    case 'G'-> fila.add(new Celda(new BloqueVidrio(), true));
                    case 'C'-> fila.add(new Celda(new BloqueCristal(), true));
                }
            }
            celdas.add(fila);
        }
    }
    private void objetivosYemisores(List<String> lineas){
        /**
         * metodo que instancia los emisores y objetivos
         */
        emisores = new ArrayList<>();
        objetivos = new ArrayList<>();

        for (String linea : lineas){
            var parametros = linea.split(" ");
            int fila = Integer.parseInt(parametros[2]);
            int columna = Integer.parseInt(parametros[1]);
            switch (parametros[0]){
                case "E" -> emisores.add(new Emisor(fila,columna,parametros[3]));
                case "G" -> objetivos.add(new Objetivo(fila, columna));
            }
        }
    }
    private void armarLados(int mFilas,int nColumnas){
        /**
         * metodo que instancia los lados en la matriz
         * se pasa por parametro la matriz de celdas para que puedan asignar sus celdas asociadas
         */
        lados = new Lado[2*mFilas + 1] [2*nColumnas + 1];
        for (int fila = 0; fila < lados.length; fila++){
            for (int columna = 0;columna < lados[0].length;columna++){
                if((fila % 2 == 0) && (columna % 2 == 1)){
                    lados[fila][columna] = new LadoHorizontal(fila,columna,celdas);
                }else if((fila % 2 == 1) && (columna % 2 == 0)){
                    lados[fila][columna] = new LadoVertical(fila,columna,celdas);
                }
            }
        }
    }

   public void jugar(){
       /**
        * metodo que recarga el nivel
        * primero desactiva todos los objetivos
        * luego reinicia la coleccion de lasers
        * envia lasers de nuevo a partir de todos los emisores
        */
       for(Objetivo obj: objetivos){
            obj.desactivar();
        }
       lasers.clear();

       for(Emisor emisor : emisores){
            Laser laser = emisor.EnviarLaser();
            this.enviarLaser(laser);
       }
   }

    public void enviarLaser(Laser laser){
        /**
         * recibe un laser ya sea que inicia en un emisor o en un lado.
         * añade este laser al registro de lasers.
         * envia el laser al lado destino.
         * el lado destino devuelve una lista de lasers que seran enviados luego.
         * el proceso continua iterativamente hasta que un lado devuelva una lista de lasers vacia.
         */
        lasers.add(laser);
        var laserList = lados[laser.getFilaFin()][laser.getColumFin()].interactuarLaser(laser.getDirectV(),laser.getDirectH());
        for(Laser l : laserList){
            this.enviarLaser(l);
        }
    }

   public void moverBloq(int filaOrigen, int columOrigen, int filaDest, int columDest){
       /**
        * dado dos coordenadas de celdas, si es posible intercambia sus bloques.
        * luego recarga el nivel con la nueva ubicacion de bloques.
        */
       boolean esFilaInicialValida = filaOrigen >= 0 && filaOrigen <= nroFilas() - 1;
       boolean esColumnaInicialValida = columOrigen >= 0 && columOrigen <= nroColumnas() - 1;
       boolean esFilaFinalValida = filaDest >= 0 && filaDest <= nroFilas() - 1;
       boolean esColumnaFinalValida = columDest >= 0 && columDest <= nroColumnas() - 1;

       if (esFilaInicialValida && esColumnaInicialValida && esFilaFinalValida && esColumnaFinalValida) {
           Celda celdaOrigen = celdas.get(filaOrigen).get(columOrigen);
           Celda celdaDestino = celdas.get(filaDest).get(columDest);

           celdaDestino.ponerBloque(celdaOrigen);
           this.jugar();
       }
   }

   public Boolean victoria(){
       /**
        * comprueba que todos los objetivos fueron activados.
        */
       for(Objetivo obj:objetivos){
            if(!obj.isActivado()){
                return false;
            }
        }
        return true;
   }

   private void setObjetivos(){
       /**
        * asigna cada objetivo al lado en el que se ubica
        */
       for(Objetivo obj : objetivos){
            lados[obj.getFila()][obj.getColumna()].setObjetivo(obj);
        }
   }

    /**
     * getters para utilizar en la parte grafica.
     */
    public int nroFilas(){ return celdas.size();}
    public int nroColumnas(){return celdas.getFirst().size();}

    public List<Objetivo> getObjetivos() {
        return objetivos;
   }
    public List<Emisor> getEmisores() {
        return emisores;
   }
    public List<Laser> getLasers(){
        return lasers;
   }
    public Celda getCelda(int fila,int columna) {return celdas.get(fila).get(columna);}

}
