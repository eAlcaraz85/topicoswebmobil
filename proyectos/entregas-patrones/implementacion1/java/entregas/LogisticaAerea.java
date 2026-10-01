package entregas;

public class LogisticaAerea extends Logistica {
    @Override
    protected MedioDeEntrega crearMedio() {
        return new EntregaDron();
    }
}
