package entregas;

public class EntregaMotocicleta implements MedioDeEntrega {
    @Override
    public Plan planear(Pedido pedido, ContextoViaje ctx) {
        boolean cabe = pedido.pesoKg <= 15;
        int minutos = (int) (pedido.distanciaKm * 3);
        if (ctx.traficoAlto) {
            minutos = (int) (minutos * 1.4);
        }
        double costo = 45.0 + (pedido.urgente ? 20.0 : 0.0);
        return new Plan("motocicleta", cabe, minutos, costo, "ciudad, paquete mediano");
    }
}
