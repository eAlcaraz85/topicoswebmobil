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


## Cliente Flutter (web, escritorio y Android)

El demo original sirve un `index.html` en el gateway. Además existe
`cliente_flutter/`: la misma operación `POST /pedidos` en una app
Flutter, de la cual se pueden generar artefactos para web, Linux,
Windows y Android (`apk`).

### Requisitos previos

1. Backend en marcha: `docker compose up --build` (puerto `8080`).
2. Flutter estable en el `PATH`.
3. Según el artefacto:
   - **Web:** Chrome o cualquier navegador (ya cubierto por Flutter).
   - **Linux:** `clang`, `cmake`, `ninja-build`, `pkg-config`, `libgtk-3-dev`.
   - **Android:** Android Studio / SDK y licencias (`flutter doctor --android-licenses`).
   - **Windows:** compilar en Windows (Visual Studio con workload de escritorio) o en CI (`windows-latest`).

En esta máquina de desarrollo, `flutter doctor` puede marcar en rojo
Android SDK y el toolchain Linux; eso no impide usar **GitHub Actions**
para producir los artefactos en runners limpios.

### URL del gateway (`API_BASE`)

| Dónde corre el cliente | Valor típico de `API_BASE` |
|------------------------|----------------------------|
| Web / Linux / Windows en la misma PC | `http://127.0.0.1:8080` |
| Emulador Android | `http://10.0.2.2:8080` |
| Dispositivo físico | `http://IP_DE_LA_PC:8080` |

Ejemplo en local:

```bash
cd cliente_flutter
flutter pub get
flutter run -d chrome --dart-define=API_BASE=http://127.0.0.1:8080
```

### Generar artefactos en local

```bash
./scripts/build_artefactos_local.sh
```

Los archivos quedan en `dist/` (web siempre; Linux y `apk` solo si el
entorno está completo). Windows no se construye desde Linux.

Comandos equivalentes a mano:

```bash
cd cliente_flutter
flutter build web --release --dart-define=API_BASE=http://127.0.0.1:8080
flutter build linux --release --dart-define=API_BASE=http://127.0.0.1:8080
flutter build apk --release --dart-define=API_BASE=http://10.0.2.2:8080
# En Windows:
flutter build windows --release --dart-define=API_BASE=http://127.0.0.1:8080
```

### CI/CD con Git (GitHub Actions)

El flujo está en `.github/workflows/artefactos-cliente.yml`.

**Importante:** GitHub solo ejecuta workflows desde `.github/` en la
*raíz del repositorio*. Este directorio `microservicios-entregas`
suele vivir dentro de otro repo. Para activar la tubería hay que
hacer una de estas dos cosas:

1. **Publicar esta carpeta como repositorio propio** (recomendado para
   la demo de CI/CD), o
2. Copiar el workflow a la raíz del monorepo y ajustar
   `working-directory` / rutas.

Pasos recomendados (repo propio):

```bash
cd proyectos/microservicios-entregas
git init
git add .
git commit -m "Demo microservicios con cliente Flutter y CI de artefactos"
# crear repo vacío en GitHub y:
git remote add origin git@github.com:USUARIO/microservicios-entregas.git
git branch -M main
git push -u origin main
```

Disparar la construcción:

```bash
git tag v0.1.0
git push origin v0.1.0
```

También puede ejecutarse a mano en la pestaña **Actions**
(`workflow_dispatch`).

La tubería produce:

| Job | Artefacto |
|-----|-----------|
| web | carpeta `build/web` (luego `entregas-web.tar.gz` en el Release) |
| linux | `entregas-linux-x64.tar.gz` |
| android | `app-release.apk` |
| windows | `entregas-windows-x64.zip` |

Con un tag `v*`, el job `release` adjunta esos archivos al
**GitHub Release** correspondiente.

### Actualizar cada cliente

| Cliente | Cómo actualizar |
|---------|-----------------|
| Web (HTML del gateway) | Rebuild de imágenes Compose / sustituir `gateway/html` |
| Web (Flutter) | Nuevo `build/web` o servir el tarball del Release |
| Linux | Descomprimir el `.tar.gz` del Release y reemplazar el bundle |
| Windows | Descomprimir el `.zip` del Release |
| Android | `adb install -r entregas-app-release.apk` |

El backend se actualiza con `docker compose up --build`. Un cambio
solo en el cliente Flutter no requiere republicar Pedidos ni
Recomendar, siempre que el contrato JSON de `/pedidos` se mantenga.

### Qué falta en el equipo local (checklist)

- [ ] Android SDK (para `apk` en esta PC)
- [ ] Toolchain Linux (`clang`, `cmake`, `ninja`, `pkg-config`, GTK)
- [ ] Repositorio Git con Actions habilitadas (para Windows y para
      artefactos sin instalar el SDK local)
- [ ] (Opcional) keystore propio si el `apk` irá a una tienda

Con Actions habilitadas ya se pueden obtener **los cuatro artefactos**
aunque el laboratorio no tenga SDK de Android ni una máquina Windows.
