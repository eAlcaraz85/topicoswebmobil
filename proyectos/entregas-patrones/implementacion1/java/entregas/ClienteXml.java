package entregas;

/** Otro proveedor: XML con atributo vehicle. */
public class ClienteXml {
    public String consultar(Pedido pedido, ContextoViaje ctx) {
        String vehicle;
        if (pedido.urgente && pedido.pesoKg <= 3 && !ctx.lluvia) {
            vehicle = "drone";
        } else if (pedido.pesoKg > 15) {
            vehicle = "van";
        } else {
            vehicle = "moto";
        }
        return "<reco vehicle=\"" + vehicle + "\"><note>xml-vendor</note></reco>";
    }
}
