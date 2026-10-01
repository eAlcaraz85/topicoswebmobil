package entregas;

/**
 * Factory Method: el oficio es despachar; las subclases fabrican el medio.
 */
public abstract class Logistica {

    protected abstract MedioDeEntrega crearMedio();

    public Plan despachar(Pedido pedido, ContextoViaje ctx) {
        MedioDeEntrega medio = crearMedio();
        return medio.planear(pedido, ctx);
    }

    /** Quién instancia la subclase (configuración). A partir de aquí se habla de Logistica. */
    public static Logistica para(Sugerencia sugerencia) {
        switch (sugerencia.medio) {
            case "camioneta":
                return new LogisticaTerrestre();
            case "motocicleta":
                return new LogisticaUrbana();
            case "bicicleta":
                return new LogisticaCorta();
            case "dron":
                return new LogisticaAerea();
            default:
                throw new IllegalArgumentException("medio: " + sugerencia.medio);
        }
    }
}
