package AppView;

import LogicaLasers.Juego;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

public class JuegoView{
    JuegoView(Stage stage, Juego juego){
        /**
         * la ventana se divide en 2 secciones
         * del lado izquierdo el seleccionador de niveles
         * del lado derecho se muestra el tablero del nivel seleccionado
         */
        var contenedorGrilla = new Group();
        var contenedorNiveles = View.crearNiveles(juego, contenedorGrilla);

        var root = new HBox(20, contenedorNiveles, contenedorGrilla);
        var scene = new Scene(root,500,500);
        stage.setScene(scene);
        stage.show();
    }
}
