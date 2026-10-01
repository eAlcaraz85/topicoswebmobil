package entregas;

public class Plan {
    public final String medio;
    public final boolean cabe;
    public final int minutos;
    public final double costo;
    public final String detalle;

    public Plan(String medio, boolean cabe, int minutos, double costo, String detalle) {
        this.medio = medio;
        this.cabe = cabe;
        this.minutos = minutos;
        this.costo = costo;
        this.detalle = detalle;
    }
}
