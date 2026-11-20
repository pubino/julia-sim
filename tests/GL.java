package myutil;

import java.util.Arrays;

/** Captures the original drawing calls in sample-grid coordinates. */
public final class GL {
    public static final byte[] mask = new byte[300 * 300];
    private static double xmin, xmax, ymin, ymax;

    public static void ortho2(double left, double right, double bottom, double top) {
        xmin = left;
        xmax = right;
        ymin = bottom;
        ymax = top;
    }

    public static void ginit(java.awt.Graphics g, int w, int h, java.awt.Component c) {}

    public static void color(java.awt.Color color) {}
    public static void swapbuffers() {}
    public static void clear() { Arrays.fill(mask, (byte) 0); }

    public static void pnt2(double x, double y) {
        int column = (int) Math.round((x - xmin) * 300 / (xmax - xmin));
        int row = (int) Math.round((y - ymin) * 300 / (ymax - ymin));
        mask[column * 300 + row] = 1;
    }
}
