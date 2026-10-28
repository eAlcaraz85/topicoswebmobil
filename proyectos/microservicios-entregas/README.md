# Microservicios de entregas (demo con Docker)

Tres contenedores distintos para ver la diferencia con el monolito Django:

```text
cliente → gateway:8080 → pedidos → recomendar (modelo .joblib)
```

## Arrancar

```bash
cd proyectos/microservicios-entregas
docker compose up --build
```

Abrir en el navegador: http://127.0.0.1:8080/

Ahí está el formulario. Manda el paquete al gateway → pedidos → recomendar
y muestra el recorrido entre servicios.

Probar por terminal:

```bash
curl -s http://127.0.0.1:8080/salud/pedidos
curl -s http://127.0.0.1:8080/salud/recomendar
curl -s -X POST -H "Content-Type: application/json" \
  -d @paquete.json http://127.0.0.1:8080/pedidos
```

Con `hora_salida: 3` en `paquete.json`, las reglas suelen descartar el dron.

## Fallo parcial

```bash
docker compose stop recomendar
curl -s -X POST -H "Content-Type: application/json" \
  -d @paquete.json http://127.0.0.1:8080/pedidos
docker compose start recomendar
```

Pedidos sigue vivo y responde 503 con un plan B. Eso no pasa igual en el monolito: ahí un `import` roto tumba todo el proceso.

## Qué no es

`docker compose up` con *varias réplicas del mismo* `plataforma-entregas` sigue siendo un monolito. Aquí cada servicio tiene otra imagen y otra responsabilidad.
