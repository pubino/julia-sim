package julia;

import java.lang.reflect.Field;
import java.security.MessageDigest;
import java.util.HexFormat;
import myutil.GL;

public final class FractalReference {
    public static void main(String[] args) throws Exception {
        Field initialized = JuliaCanvas.class.getDeclaredField("ginited");
        initialized.setAccessible(true);
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        double[][] cases = {{-2, 2, -2, 2}, {-0.82, -0.65, 0.03, 0.17}, {1, 1.6, -0.4, 0.2}};
        for (int index = 0; index < cases.length; index++) {
            double[] bounds = cases[index];
            JuliaCanvas original = new JuliaCanvas(null);
            original.minx = bounds[0];
            original.maxx = bounds[1];
            original.miny = bounds[2];
            original.maxy = bounds[3];
            initialized.setBoolean(original, true);
            for (int step = 1; step <= 48; step++) {
                original.paint(null);
                if (step == 1 || step == 2 || step == 12 || step == 48) {
                    System.out.println(index + "," + step + "," + original.thresh + ","
                        + HexFormat.of().formatHex(digest.digest(GL.mask)) + ","
                        + original.wreal[299][150] + "," + original.wimag[299][150]);
                }
            }
        }
    }
}
