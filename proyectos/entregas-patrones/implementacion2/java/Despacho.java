/**
 * MALA PRÁCTICA a propósito.
 *
 * Mismo trámite que entregas.Main (registrar pedido, oír a la IA, planear).
 * No hay Strategy, ni Adapter, ni Factory Method.
 *
 * Un solo método conoce route_hint, el XML, los if del medio y los números
 * del plan. Añadir un triciclo o cambiar vehicle por route_hint abre ESTE archivo.
 */
public class Despacho {

    public static void main(String[] args) {
        System.out.println("Plataforma de entregas — SIN patrones (mala práctica)");
        System.out.println("Un solo método: JSON/XML + if de medios + plan. Copiar y rezar.");

        System.out.println("\n=== Pedido ligero + JSON de OpenAI ===");
        registrarPedido("Centro", "Roma Norte", 1.2, 4.0, true, true, false, "openai");

        System.out.println("\n=== Pedido pesado + XML de otro proveedor ===");
        registrarPedido("Bodega Norte", "Iztapalapa", 28.0, 18.0, false, true, false, "xml");
    }

    static void registrarPedido(String origen, String destino, double peso, double distancia,
                                boolean urgente, boolean trafico, boolean lluvia, String proveedor) {
        boolean cabe = false;
        int minutos = 0;
        double costo = 0;
        String detalle = "";
        String medio = "";
        String motivo = "";
        String hint = "";

        if (proveedor.equals("openai")) {
            String why;
            int score;
            if (peso <= 3 && distancia <= 12 && !lluvia) {
                hint = "drone";
                score = 91;
                why = "FASTEST";
            } else if (peso <= 5 && distancia <= 8) {
                hint = "bike";
                score = 80;
                why = "SHORT_HOP";
            } else if (peso <= 15) {
                hint = "moto";
                score = 74;
                why = "CITY";
            } else {
                hint = "van";
                score = 60;
                why = "HEAVY";
            }
            motivo = why + " (score " + score + ")";

            if (hint.equals("drone")) {
                medio = "dron";
                cabe = peso <= 3 && distancia <= 12 && !lluvia;
                minutos = (int) (distancia * 2);
                costo = 70;
                detalle = "rápido; no vuela con lluvia ni con mucho peso";
            } else if (hint.equals("bike")) {
                medio = "bicicleta";
                cabe = peso <= 5 && distancia <= 8;
                minutos = (int) (distancia * 6);
                if (trafico) {
                    minutos = (int) (minutos * 1.1);
                }
                costo = 25;
                detalle = "paquete chico, tramo corto";
            } else if (hint.equals("moto")) {
                medio = "motocicleta";
                cabe = peso <= 15;
                minutos = (int) (distancia * 3);
                if (trafico) {
                    minutos = (int) (minutos * 1.4);
                }
                costo = 45;
                if (urgente) {
                    costo = costo + 20;
                }
                detalle = "ciudad, paquete mediano";
            } else if (hint.equals("van")) {
                medio = "camioneta";
                cabe = true;
                minutos = (int) (distancia * 4.5);
                if (trafico) {
                    minutos = (int) (minutos * 1.6);
                }
                costo = 90 + peso * 2;
                detalle = "carga amplia, más lenta en ciudad";
            } else {
                System.out.println("hint desconocido, toca editar registrarPedido");
            }

        } else if (proveedor.equals("xml")) {
            String xml;
            if (urgente && peso <= 3 && !lluvia) {
                xml = "<reco vehicle=\"drone\"><note>xml-vendor</note></reco>";
            } else if (peso > 15) {
                xml = "<reco vehicle=\"van\"><note>xml-vendor</note></reco>";
            } else {
                xml = "<reco vehicle=\"moto\"><note>xml-vendor</note></reco>";
            }

            if (xml.contains("vehicle=\"drone\"")) {
                hint = "drone";
            } else if (xml.contains("vehicle=\"bike\"")) {
                hint = "bike";
            } else if (xml.contains("vehicle=\"moto\"")) {
                hint = "moto";
            } else if (xml.contains("vehicle=\"van\"")) {
                hint = "van";
            }
            motivo = "proveedor XML (xml-vendor)";

            // Las mismas reglas, copiadas. Un cambio de costo obliga a tocar
            // el bloque de openai Y este.
            if (hint.equals("drone")) {
                medio = "dron";
                cabe = peso <= 3 && distancia <= 12 && !lluvia;
                minutos = (int) (distancia * 2);
                costo = 70;
                detalle = "rápido; no vuela con lluvia ni con mucho peso";
            } else if (hint.equals("bike")) {
                medio = "bicicleta";
                cabe = peso <= 5 && distancia <= 8;
                minutos = (int) (distancia * 6);
                if (trafico) {
                    minutos = (int) (minutos * 1.1);
                }
                costo = 25;
                detalle = "paquete chico, tramo corto";
            } else if (hint.equals("moto")) {
                medio = "motocicleta";
                cabe = peso <= 15;
                minutos = (int) (distancia * 3);
                if (trafico) {
                    minutos = (int) (minutos * 1.4);
                }
                costo = 45;
                if (urgente) {
                    costo = costo + 20;
                }
                detalle = "ciudad, paquete mediano";
            } else if (hint.equals("van")) {
                medio = "camioneta";
                cabe = true;
                minutos = (int) (distancia * 4.5);
                if (trafico) {
                    minutos = (int) (minutos * 1.6);
                }
                costo = 90 + peso * 2;
                detalle = "carga amplia, más lenta en ciudad";
            }
        } else {
            System.out.println("proveedor nuevo: hay que agregar otro else if aquí");
        }

        System.out.println();
        System.out.println("Pedido: " + origen + " → " + destino + " (" + peso + " kg, " + distancia + " km)");
        System.out.println("IA (idioma ajeno, sin traducir del todo): " + motivo);
        System.out.println("Medio: " + medio + "  cabe=" + cabe + "  " + minutos + " min  $" + (int) costo);
        System.out.println("  " + detalle);
        if (!cabe) {
            System.out.println("  El medio no cabe; el if de arriba ya mezcló IA y plan.");
        }
    }
}
