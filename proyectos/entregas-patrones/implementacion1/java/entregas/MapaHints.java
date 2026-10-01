package entregas;

public final class MapaHints {
    private MapaHints() {}

    public static String aDominio(String routeHint) {
        switch (routeHint) {
            case "drone":
                return "dron";
            case "bike":
                return "bicicleta";
            case "moto":
                return "motocicleta";
            case "van":
                return "camioneta";
            default:
                throw new IllegalArgumentException("hint desconocido: " + routeHint);
        }
    }
}
