package AppView;

import LogicaLasers.*;
import javafx.scene.Group;
import javafx.scene.layout.Background;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.scene.control.Button;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;
import javafx.scene.shape.Rectangle;
import java.util.List;

public class View{
    private static final int TAM_CELDAS = 60; //numero de px que ocupa cada celda
    private static final int BORDE_IZQUIERDO_GRILLA = 83; //numero de px que hay a la izquierda de la grilla

    public static VBox crearNiveles(Juego juego,Group contenedorGrilla){
        /**
         * seleccionador de niveles
         * cada nivel se representa con un boton
         * los botones se colocan verticalmente
         */
        int nivel = 1;
        var contenedor = new VBox(10);
        while (nivel <= juego.getSizeTableros()){
            Button btn = new Button(String.format("Nivel %d", nivel));
            contenedor.getChildren().add(btn);

            int finalNivel = nivel;
            btn.setOnMouseClicked(e -> {
                juego.play(finalNivel);
                View.cargarTablero(juego.getTablero(), contenedorGrilla,juego);
            });
            nivel++;
        }


        return contenedor;
    }

    public static void cargarTablero(Tablero tablero, Group contenedor, Juego juego){
        /**
         * el tablero es un Group donde se colocan todos los elementos que lo forman (Celdas, Emisores, Objetivos y Lasers)
         * en caso de victoria el fondo cambia color verde y se desactiva la interaccion para evitar seguir jugando
         */
        contenedor.setDisable(false);
        contenedor.getChildren().clear();

        dibujarGrilla(tablero, contenedor,juego);
        dibujarEmisores(tablero.getEmisores(),contenedor);
        dibujarObjetivos(tablero.getObjetivos(),contenedor);
        dibujarLaser(tablero.getLasers(),contenedor);

        if (tablero.victoria()) {
            GridPane background = (GridPane) contenedor.getChildren().getFirst();
            background.setBackground(Background.fill(Color.PALEGREEN));
            contenedor.setDisable(true);
        }
    }

    private static void dibujarGrilla(Tablero tablero, Group contenedor,Juego juego){
        /**
         * la grilla contiene las celdas y las contiene en forma de matriz
         */
        GridPane grilla = new GridPane();
        int filas = tablero.nroFilas();
        int columnas = tablero.nroColumnas();
        grilla.setMaxSize(filas * TAM_CELDAS, columnas * TAM_CELDAS);
        for(int i = 0; i < filas; i++){
            for(int j = 0; j < columnas; j++ ){
                dibujarCelda(tablero.getCelda(i,j), grilla, i, j, contenedor, juego);
            }
        }
        contenedor.getChildren().add(grilla);
    }

    private static void dibujarCelda(Celda celda, GridPane grilla, int fila, int columna, Group contenedorGrilla, Juego juego){
        /**
         * Las celdas se representan con cuadrados
         * el color de la celda indica el tipo de bloque que contiene
         */
        var celdaPintada = new Rectangle(TAM_CELDAS, TAM_CELDAS, Color.BLACK);
        TipoBloque nombreBloque = celda.getNombreBloque();
        celdaPintada.setStroke(Color.BLACK);
        switch (nombreBloque) {
            case CRISTAL:
                celdaPintada.setFill(Color.SKYBLUE);
                break;
            case ESPEJO:
                celdaPintada.setFill(Color.CADETBLUE);
                break;
            case OPACO:
                if (celda.esMovil()) {
                    celdaPintada.setFill(Color.DARKGREY);
                } else {
                    celdaPintada.setFill(Color.BLACK);
                }
                break;
            case VIDRIO:
                celdaPintada.setFill(Color.AQUAMARINE);
                break;
            default:
                celdaPintada.setFill(Color.TRANSPARENT);
                if (!celda.esMovil()) {
                    celdaPintada.setStrokeWidth(0);
                }
        }

        setDragDrop(celdaPintada, contenedorGrilla, fila, columna, juego);

        grilla.add(celdaPintada,columna,fila);
    }

    private static void setDragDrop(Rectangle celda, Group contenedorGrilla, int fila, int columna, Juego juego) {
        int[] coordsIniciales = new int[2];
        coordsIniciales[0] = fila;
        coordsIniciales[1] = columna;
        var celdaPlaceholder = new Rectangle(TAM_CELDAS, TAM_CELDAS); //Copia que aparece cada vez que arrastramos el mouse
        celdaPlaceholder.setFill(celda.getFill());
        celdaPlaceholder.setStroke(Color.BLACK);

        //Si detecta drag, mete a la copia del bloque que se activó en el orden más arriba del contenedor
        celda.setOnDragDetected(e -> contenedorGrilla.getChildren().add(celdaPlaceholder));

        //Mueve la copia del bloque siguiendo al mouse
        celda.setOnMouseDragged(e -> {
            celdaPlaceholder.setTranslateX(e.getSceneX() - BORDE_IZQUIERDO_GRILLA - (double) TAM_CELDAS / 2);
            celdaPlaceholder.setTranslateY(e.getSceneY() - (double) TAM_CELDAS / 2);
        });

        //Una vez que el mouse se suelta, hace la logica correspondiente
        celda.setOnMouseReleased(e -> {
            double[] coordsFinales = new double[2];
            coordsFinales[0] = e.getSceneX();
            coordsFinales[1] = e.getSceneY();
            swapBloques(juego, coordsIniciales, coordsFinales, contenedorGrilla);

            contenedorGrilla.getChildren().removeAll(celdaPlaceholder);
        });

    }

    private static void swapBloques(Juego juego, int[] coordsIniciales, double[] coordsFinales, Group contenedorGrilla) {
        int columnaFinal = (int) ((coordsFinales[0] - BORDE_IZQUIERDO_GRILLA) / TAM_CELDAS);
        int filaFinal = (int) (coordsFinales[1] / TAM_CELDAS);
        juego.moverBloque(coordsIniciales[0], coordsIniciales[1], filaFinal, columnaFinal);
        cargarTablero(juego.getTablero(), contenedorGrilla,juego);
    }

    private static void dibujarEmisores(List<Emisor> emisores, Group contenedor){
        for(Emisor emisor: emisores){
            var dibujo = new Circle((double) emisor.getColumna() * TAM_CELDAS /2,(double) emisor.getFila() * TAM_CELDAS /2 ,4);
            dibujo.setStroke(Color.RED);
            dibujo.setStrokeWidth(2);
            dibujo.setFill(Color.RED);
            contenedor.getChildren().add(dibujo);
        }
    }
    private static void dibujarObjetivos(List<Objetivo> objetivos, Group contenedor){
        /**
         * Los objetivos son circulos de borde rojo
         * en su interior son blancos, en caso de activarlos pasa a verde
         */
        for(Objetivo obj : objetivos ){
            var dibujo = new Circle((double) obj.getColumna() * TAM_CELDAS /2,(double) obj.getFila() * TAM_CELDAS /2 ,4);
            dibujo.setStroke(Color.RED);
            dibujo.setStrokeWidth(2);

            if (obj.isActivado()){
                dibujo.setFill(Color.LIGHTGREEN);
            }else{
                dibujo.setFill(Color.WHITE);
            }
            contenedor.getChildren().add(dibujo);
        }
    }
    private static void dibujarLaser(List<Laser> lasers, Group contenedor){
        /**
         * El laser del nivel se forma al unir todos los lasers de la lista de lasers del tablero
         * cada laser se representa con una linea desde el punto de origen al punto de destino.
         */
        for(Laser las: lasers){
            var l = new Line();
            l.setStartX((double)las.getColumInicio()*TAM_CELDAS /2);
            l.setStartY((double)las.getFilaInicio()*TAM_CELDAS/2);
            l.setEndX((double) las.getColumFin()*TAM_CELDAS/2);
            l.setEndY((double) las.getFilaFin()*TAM_CELDAS/2);
            l.setStroke(Color.RED);
            contenedor.getChildren().add(l);
        }
    }
}
