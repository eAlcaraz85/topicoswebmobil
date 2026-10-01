package entregas;

public class Pedido {
    public final String origen;
    public final String destino;
    public final double pesoKg;
    public final double distanciaKm;
    public final boolean urgente;

    public Pedido(String origen, String destino, double pesoKg, double distanciaKm, boolean urgente) {
        this.origen = origen;
        this.destino = destino;
        this.pesoKg = pesoKg;
        this.distanciaKm = distanciaKm;
        this.urgente = urgente;
    }
}
