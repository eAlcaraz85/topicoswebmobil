package entregas;

/** Respuesta cruda del proveedor. El dominio no debería ver estos nombres. */
public class OpenAiRespuesta {
    public final String routeHint;
    public final int score;
    public final String why;

    public OpenAiRespuesta(String routeHint, int score, String why) {
        this.routeHint = routeHint;
        this.score = score;
        this.why = why;
    }
}
