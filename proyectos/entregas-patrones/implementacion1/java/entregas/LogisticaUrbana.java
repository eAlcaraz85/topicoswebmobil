package entregas;

public class LogisticaUrbana extends Logistica {
    @Override
    protected MedioDeEntrega crearMedio() {
        return new EntregaMotocicleta();
    }
}
