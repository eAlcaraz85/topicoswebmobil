package entregas;

public class LogisticaCorta extends Logistica {
    @Override
    protected MedioDeEntrega crearMedio() {
        return new EntregaBicicleta();
    }
}
