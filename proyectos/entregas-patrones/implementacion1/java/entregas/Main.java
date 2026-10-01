package entregas;

public class Main {

    public static void main(String[] args) {
        System.out.println("Plataforma de entregas");
        System.out.println("Adapter traduce la IA. Factory Method crea el medio. Strategy planea.");

        Pedido ligero = new Pedido("Centro", "Roma Norte", 1.2, 4.0, true);
        Pedido pesado = new Pedido("Bodega Norte", "Iztapalapa", 28.0, 18.0, false);
        ContextoViaje ciudad = new ContextoViaje(true, false);

        mostrar("Pedido ligero + JSON de OpenAI", ligero,
                RegistrarPedido.registrar(ligero, ciudad, new AdaptadorOpenAI()));
        mostrar("Pedido pesado + XML de otro proveedor", pesado,
                RegistrarPedido.registrar(pesado, ciudad, new AdaptadorXml()));
    }

    private static void mostrar(String titulo, Pedido pedido, RegistrarPedido.Resultado r) {
        Plan plan = r.plan;
        System.out.println();
        System.out.println("=== " + titulo + " ===");
        System.out.println("Pedido: " + pedido.origen + " → " + pedido.destino
                + " (" + pedido.pesoKg + " kg, " + pedido.distanciaKm + " km)");
        System.out.println("IA (ya traducida): " + r.motivoIa);
        System.out.println("Strategy (" + plan.medio + "): cabe=" + plan.cabe
                + "  " + plan.minutos + " min  $" + (int) plan.costo);
        System.out.println("  " + plan.detalle);
        if (!plan.cabe) {
            System.out.println("  El medio sugerido no cabe; habría que pedir otra sugerencia o otro medio.");
        }
    }
}
