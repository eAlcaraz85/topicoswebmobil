package entregas;

public class EntregaBicicleta implements MedioDeEntrega {
    @Override
    public Plan planear(Pedido pedido, ContextoViaje ctx) {
        boolean cabe = pedido.pesoKg <= 5 && pedido.distanciaKm <= 8;
        int minutos = (int) (pedido.distanciaKm * 6);
        if (ctx.traficoAlto) {
            minutos = (int) (minutos * 1.1);
        }
        return new Plan("bicicleta", cabe, minutos, 25.0, "paquete chico, tramo corto");
    }
}
