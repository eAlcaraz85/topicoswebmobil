package entregas;

public class LogisticaTerrestre extends Logistica {
    @Override
    protected MedioDeEntrega crearMedio() {
        return new EntregaCamioneta();
    }
}
