package entregas;

import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;
import java.io.StringReader;

public class AdaptadorXml implements RecomendadorIA {
    private final ClienteXml cliente;

    public AdaptadorXml() {
        this(new ClienteXml());
    }

    public AdaptadorXml(ClienteXml cliente) {
        this.cliente = cliente;
    }

    @Override
    public Sugerencia sugerir(Pedido pedido, ContextoViaje ctx) {
        String xml = cliente.consultar(pedido, ctx);
        try {
            Element raiz = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder()
                    .parse(new InputSource(new StringReader(xml)))
                    .getDocumentElement();
            String medio = MapaHints.aDominio(raiz.getAttribute("vehicle"));
            String nota = raiz.getTextContent().trim();
            return new Sugerencia(medio, "proveedor XML (" + nota + ")");
        } catch (Exception e) {
            throw new IllegalStateException("no se pudo leer el XML del proveedor", e);
        }
    }
}
