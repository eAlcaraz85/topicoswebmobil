package entregas;

/** Lo que el dominio entiende. El JSON/XML ajeno no entra aquí. */
public class Sugerencia {
    public final String medio;
    public final String motivo;

    public Sugerencia(String medio, String motivo) {
        this.medio = medio;
        this.motivo = motivo;
    }
}
