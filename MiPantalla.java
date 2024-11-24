import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField; // Importar TextField
import javafx.scene.control.Tooltip;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class MiPantalla extends Application {
    
    @Override
    public void start(Stage stage) {

        // aquí comienza la pantalla 
        Label label = new Label("Ingrese su nombre:");

        // un campo de texto
        TextField campoTexto = new TextField(); // Cambiar Textfield a TextField

        // botón
        Button boton = new Button("Aceptar");
        boton.setOnAction(e -> {
            String nombre = campoTexto.getText();
            System.out.println(nombre);
        });

        Tooltip tooltip = new Tooltip("Mensaje que pongo al boton");
        boton.setTooltip(tooltip);
        DropShadow sombra = new DropShadow();
        boton.setEffect(sombra);
        boton.setOnMouseEntered(e -> {
            boton.setStyle("-fx-background-color:#ff0000");
        });
        boton.setOnMouseExited(e -> {
            boton.setStyle("-fx-background-color:#ffffff");
        });



        VBox layout = new VBox(10);
        layout.getChildren().addAll(label, campoTexto, boton);

        // crear escena
        Scene escena = new Scene(layout, 300, 200);
        stage.setScene(escena);
        stage.setTitle("Mi pantalla");
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
