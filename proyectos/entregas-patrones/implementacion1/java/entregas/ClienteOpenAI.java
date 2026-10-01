package entregas;

/** Simula un proveedor que responde JSON propio (route_hint, score). */
public class ClienteOpenAI {
    public OpenAiRespuesta completar(Pedido pedido, ContextoViaje ctx) {
        if (pedido.pesoKg <= 3 && pedido.distanciaKm <= 12 && !ctx.lluvia) {
            return new OpenAiRespuesta("drone", 91, "FASTEST");
        }
        if (pedido.pesoKg <= 5 && pedido.distanciaKm <= 8) {
            return new OpenAiRespuesta("bike", 80, "SHORT_HOP");
        }
        if (pedido.pesoKg <= 15) {
            return new OpenAiRespuesta("moto", 74, "CITY");
        }
        return new OpenAiRespuesta("van", 60, "HEAVY");
    }
}
