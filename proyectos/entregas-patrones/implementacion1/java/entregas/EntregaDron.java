package entregas;

public class EntregaDron implements MedioDeEntrega {
    @Override
    public Plan planear(Pedido pedido, ContextoViaje ctx) {
        boolean cabe = pedido.pesoKg <= 3 && pedido.distanciaKm <= 12 && !ctx.lluvia;
        int minutos = (int) (pedido.distanciaKm * 2);
        return new Plan("dron", cabe, minutos, 70.0, "rápido; no vuela con lluvia ni con mucho peso");
    }
}
