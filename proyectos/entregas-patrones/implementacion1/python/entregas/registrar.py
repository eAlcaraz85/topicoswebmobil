from .dominio import ContextoViaje, Pedido, Plan
from .ia import RecomendadorIA
from .logistica import logistica_para


def registrar_pedido(
    pedido: Pedido,
    ctx: ContextoViaje,
    recomendador: RecomendadorIA,
) -> tuple[Plan, str]:
    """Orquesta Adapter → Factory Method → Strategy. No nombra EntregaDron."""
    sugerencia = recomendador.sugerir(pedido, ctx)
    logistica = logistica_para(sugerencia)
    plan = logistica.despachar(pedido, ctx)
    return plan, sugerencia.motivo
