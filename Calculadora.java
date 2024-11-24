import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;
 
public class Calculadora extends Application {
    @Override
    public void start(Stage stage) {
        Label label1 = new Label("Numero 1");
        Label label2 = new Label("Numero 2");
        TextField numero1_text = new TextField();
        TextField numero2_text = new TextField();
        Button sumar = new Button("Sumar");
        Button restar = new Button("Restar");
        Button multiplicar = new Button("Multiplicar");
        Button dividir = new Button("Dividir");
        Label label3 = new Label("Resultado");
        TextField resultado = new TextField();
        resultado.setEditable(false);
 
        GridPane grid = new GridPane();
        grid.setVgap(10);
        grid.setHgap(10);
 
        grid.add(label1, 0, 0);
        grid.add(label2, 0, 1);
        grid.add(numero1_text, 1, 0);
        grid.add(numero2_text, 1, 1);
        grid.add(sumar, 0, 2);
        grid.add(restar, 1, 2);
        grid.add(multiplicar, 2, 2);
        grid.add(dividir, 3, 2);
        grid.add(label3, 0, 3);
        grid.add(resultado, 1, 3);
        sumar.setOnAction(e -> {
            try {
                double num1 = Double.parseDouble(numero1_text.getText());
                double num2 = Double.parseDouble(numero2_text.getText());
                double suma = num1 + num2;
                resultado.setText(String.valueOf(suma));
            } catch (NumberFormatException ex) {
                resultado.setText("Introduzca 2 números");
            }
        });
        restar.setOnAction(e -> {
            try {
                double num1 = Double.parseDouble(numero1_text.getText());
                double num2 = Double.parseDouble(numero2_text.getText());
                double resta = num1 - num2;
                resultado.setText(String.valueOf(resta));
            } catch (NumberFormatException ex) {
                resultado.setText("Introduzca 2 números");
            }
        });
        multiplicar.setOnAction(e -> {
            try {
                double num1 = Double.parseDouble(numero1_text.getText());
                double num2 = Double.parseDouble(numero2_text.getText());
                double producto = num1 * num2;
                resultado.setText(String.valueOf(producto));
            } catch (NumberFormatException ex) {
                resultado.setText("Introduzca 2 números");
            }
        });

        dividir.setOnAction(e -> {
            try {
                double num1 = Double.parseDouble(numero1_text.getText());
                double num2 = Double.parseDouble(numero2_text.getText());
                double division = num1 / num2;
                resultado.setText(String.valueOf(division));
            } catch (NumberFormatException ex) {
                resultado.setText("Introduzca 2 números");
            }
        });
        Scene escena = new Scene(grid, 400, 250);
        stage.setScene(escena);
        stage.setTitle("Calculadora");
        stage.show();
    }
 
    public static void main(String[] args) {
        launch(args);
    }
}