package entregas;

/** Strategy: varias formas de planear la misma entrega. */
public interface MedioDeEntrega {
    Plan planear(Pedido pedido, ContextoViaje ctx);
}
