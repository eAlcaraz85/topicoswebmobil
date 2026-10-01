# Mala práctica (el mismo trámite, sin patrones)

Misma empresa, mismos dos pedidos. Aquí **no** se usan Strategy,
Adapter ni Factory Method. Es el código del que parten los apuntes:
un método que copia, pega y reza.

| Lo que está mal | Por qué duele mañana |
|-----------------|----------------------|
| `route_hint` y `vehicle` se leen *dentro* de registrar | Cambia el JSON y se rompe el plan |
| Un `if` por medio, repetido para OpenAI y para XML | Un triciclo obliga a editar *dos* bloques |
| No hay `crearMedio()`: el trámite nombra drone/bike/van | Fabricar y planear están pegados |
| Un solo archivo lo sabe todo | No se puede probar el dron sin armar el XML |

Compáralo con `../python` y `../java`. El resultado en pantalla es el
mismo; lo que cambia es *cuántos sitios abres* el día que el
proveedor dice `vehicle` en vez de `route_hint`.

## Python

```bash
cd mala-practica/python
python3 despacho.py
```

## Java

```bash
cd mala-practica/java
javac Despacho.java
java Despacho
```
