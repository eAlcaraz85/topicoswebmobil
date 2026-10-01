package entregas;

public final class RegistrarPedido {
    private RegistrarPedido() {}

    /** Orquesta Adapter → Factory Method → Strategy. No nombra EntregaDron. */
    public static Resultado registrar(Pedido pedido, ContextoViaje ctx, RecomendadorIA recomendador) {
        Sugerencia sugerencia = recomendador.sugerir(pedido, ctx);
        Logistica logistica = Logistica.para(sugerencia);
        Plan plan = logistica.despachar(pedido, ctx);
        return new Resultado(plan, sugerencia.motivo);
    }

    public static final class Resultado {
        public final Plan plan;
        public final String motivoIa;

        public Resultado(Plan plan, String motivoIa) {
            this.plan = plan;
            this.motivoIa = motivoIa;
        }
    }
}
