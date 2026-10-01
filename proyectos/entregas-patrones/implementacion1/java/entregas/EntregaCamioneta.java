package entregas;

public class EntregaCamioneta implements MedioDeEntrega {
    @Override
    public Plan planear(Pedido pedido, ContextoViaje ctx) {
        int minutos = (int) (pedido.distanciaKm * 4.5);
        if (ctx.traficoAlto) {
            minutos = (int) (minutos * 1.6);
        }
        double costo = 90.0 + pedido.pesoKg * 2;
        return new Plan("camioneta", true, minutos, costo, "carga amplia, más lenta en ciudad");
    }
}
