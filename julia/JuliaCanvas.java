package julia;

import java.awt.*;
import java.applet.*;
import java.awt.image.*;
import java.util.*;
import java.io.*;
import java.net.*;
import java.text.*;

import myutil.*;
import myutil.Format;

class JuliaCanvas extends Canvas implements Runnable
{
	Julia parent;
	Graphics g;
	double minx, maxx, miny, maxy;
	double thresh = 1000;
	double[][] wreal;
	double[][] wimag;

	public JuliaCanvas(Julia parent)
	{
		this.parent = parent;
		wreal = new double[300][300];
		wimag = new double[300][300];
	}

	private Thread animate;
	private boolean ginited=false;

	public void start()
	{
	    if (animate == null) {
		minx = SL.atof(parent.Minx.getText());
		maxx = SL.atof(parent.Maxx.getText());
		miny = SL.atof(parent.Miny.getText());
		maxy = SL.atof(parent.Maxy.getText());

		g = getGraphics();
	        GL.ginit(g, size().width, size().height, this);
		ginited=true;

		animate = new Thread( this );
		animate.start();
	    }
	}

	public void stop()
	{
	    if (animate != null) {
		animate.stop();
		animate = null;
	    }
	}

	public void run()
	{
		int i, j, t;
		thresh = 1000;
		for (i=0; i<300; i++) {
		    for (j=0; j<300; j++) {
			wreal[i][j] = 0;
			wimag[i][j] = 0;
		    }
		}
		for (t=0; ; t++) {
			try { Thread.sleep( 100 ); }
			catch ( InterruptedException e ){};

			paint(g);
		}
	}

	public void paint (Graphics g)
	{
		int i,j;
		double x, y;
		double w2, maxw2, newwreal, newwimag;

		if (!ginited) {return;}
                GL.ortho2( minx, maxx, miny, maxy );

		GL.color(Color.white);
		GL.clear();

		GL.color(Color.black);
		maxw2 = 0;
		for (i=0; i<300; i++) {
		    for (j=0; j<300; j++) {
			x = minx + (i*(maxx-minx))/300;
			y = miny + (j*(maxy-miny))/300;
			newwreal = wreal[i][j]*wreal[i][j]
				 - wimag[i][j]*wimag[i][j] + x;

			newwimag = 2*wreal[i][j]*wimag[i][j] + y;
			w2 = newwreal*newwreal+newwimag*newwimag;
			if (w2 > thresh) { GL.pnt2(x,y); }
			if (w2 > maxw2) { maxw2 = w2; }
			if (w2 < 1.0e+100) {
			    wreal[i][j] = newwreal;
			    wimag[i][j] = newwimag;
			}
		    }
		}
		thresh = Math.sqrt(maxw2);
		System.err.println("thresh = "+thresh+" wreal = "
				   +wreal[299][150]);

		GL.swapbuffers();
	}
}
