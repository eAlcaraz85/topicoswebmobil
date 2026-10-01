package entregas;

public class AdaptadorOpenAI implements RecomendadorIA {
    private final ClienteOpenAI cliente;

    public AdaptadorOpenAI() {
        this(new ClienteOpenAI());
    }

    public AdaptadorOpenAI(ClienteOpenAI cliente) {
        this.cliente = cliente;
    }

    @Override
    public Sugerencia sugerir(Pedido pedido, ContextoViaje ctx) {
        OpenAiRespuesta crudo = cliente.completar(pedido, ctx);
        String medio = MapaHints.aDominio(crudo.routeHint);
        String motivo = crudo.why + " (score " + crudo.score + ")";
        return new Sugerencia(medio, motivo);
    }
}
