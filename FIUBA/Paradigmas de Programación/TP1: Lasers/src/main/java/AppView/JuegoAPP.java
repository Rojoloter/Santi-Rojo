package AppView;

import LogicaLasers.Juego;
import javafx.application.Application;

import javafx.stage.Stage;


public class JuegoAPP extends Application{

    public static void main(String [] args) {
        launch(args);
    }

    @Override
    public void start(Stage stage) throws Exception {
        var juego = new Juego();
        var view = new JuegoView(stage, juego);
        stage.show();
    }
}
