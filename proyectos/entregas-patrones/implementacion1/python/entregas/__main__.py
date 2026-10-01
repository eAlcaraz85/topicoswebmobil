from .dominio import ContextoViaje, Pedido
from .ia import AdaptadorOpenAI, AdaptadorXml
from .registrar import registrar_pedido


def mostrar(titulo: str, pedido: Pedido, plan, motivo: str) -> None:
    print(f"\n=== {titulo} ===")
    print(f"Pedido: {pedido.origen} → {pedido.destino} ({pedido.peso_kg} kg, {pedido.distancia_km} km)")
    print(f"IA (ya traducida): {motivo}")
    print(f"Strategy ({plan.medio}): cabe={plan.cabe}  {plan.minutos} min  ${plan.costo:.0f}")
    print(f"  {plan.detalle}")
    if not plan.cabe:
        print("  El medio sugerido no cabe; habría que pedir otra sugerencia o otro medio.")


def main() -> None:
    print("Plataforma de entregas")
    print("Adapter traduce la IA. Factory Method crea el medio. Strategy planea.")

    ligero = Pedido("Centro", "Roma Norte", peso_kg=1.2, distancia_km=4.0, urgente=True)
    pesado = Pedido("Bodega Norte", "Iztapalapa", peso_kg=28.0, distancia_km=18.0)
    ciudad = ContextoViaje(trafico_alto=True, lluvia=False)

    plan1, motivo1 = registrar_pedido(ligero, ciudad, AdaptadorOpenAI())
    mostrar("Pedido ligero + JSON de OpenAI", ligero, plan1, motivo1)

    plan2, motivo2 = registrar_pedido(pesado, ciudad, AdaptadorXml())
    mostrar("Pedido pesado + XML de otro proveedor", pesado, plan2, motivo2)


if __name__ == "__main__":
    main()
