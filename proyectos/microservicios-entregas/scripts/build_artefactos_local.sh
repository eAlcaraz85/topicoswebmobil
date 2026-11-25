#!/usr/bin/env bash
# Genera artefactos en local (lo que el entorno permita).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="$ROOT/cliente_flutter"
OUT="$ROOT/dist"
API_BASE="${API_BASE:-http://127.0.0.1:8080}"
mkdir -p "$OUT"
cd "$APP"

echo "==> Web"
flutter pub get
flutter build web --release --dart-define=API_BASE="$API_BASE"
tar -czf "$OUT/entregas-web.tar.gz" -C build/web .
echo "    $OUT/entregas-web.tar.gz"

if flutter doctor 2>/dev/null | grep -q "Linux toolchain.*✓"; then
  echo "==> Linux desktop"
  flutter config --enable-linux-desktop >/dev/null
  flutter build linux --release --dart-define=API_BASE="$API_BASE"
  tar -czf "$OUT/entregas-linux-x64.tar.gz" -C build/linux/x64/release/bundle .
  echo "    $OUT/entregas-linux-x64.tar.gz"
else
  echo "==> Linux desktop omitido (faltan clang/cmake/ninja/pkg-config o libgtk)"
fi

if flutter doctor 2>/dev/null | grep -q "Android toolchain.*✓"; then
  echo "==> APK"
  flutter build apk --release --dart-define=API_BASE="${ANDROID_API_BASE:-http://10.0.2.2:8080}"
  cp build/app/outputs/flutter-apk/app-release.apk "$OUT/entregas-app-release.apk"
  echo "    $OUT/entregas-app-release.apk"
else
  echo "==> APK omitido (no hay Android SDK). Use el workflow de CI o un contenedor Flutter."
fi

echo "==> Windows: construir en máquina Windows o en el job windows-latest del CI."
echo "Listo. Artefactos en $OUT"
