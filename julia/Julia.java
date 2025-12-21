package julia;

import java.awt.*;
import java.awt.image.*;
import java.util.*;
import java.io.*;
import java.text.*;

import myutil.*;
import myutil.Format;

public class Julia extends Panel implements SimApp
{
	TextField Minx, Maxx, Miny, Maxy;

	JuliaCanvas mc;

        public static void main(String[] args) {
                new AppletFrame(new Julia(), 350, 450);
        }

	public void init()
	{
	    setLayout(new FlowLayout(FlowLayout.LEFT));
	    setBackground(Color.white);

	    Minx  = new TextField("-2", 10);
	    Maxx  = new TextField(" 2", 10);
	    Miny  = new TextField("-2", 10);
	    Maxy  = new TextField(" 2", 10);
	    mc = new JuliaCanvas(this);
	    add(new Label("minx:")); add(Minx);
	    add(new Label("maxx:")); add(Maxx);
	    add(new Label("miny:")); add(Miny);
	    add(new Label("maxy:")); add(Maxy);
	    add(new Button("Simulate"));
	    add(mc);

	    mc.resize(300,300);
	}

	public void start() {
		// No-op for this simulation
	}

	public void stop()
	{
	    mc.stop();
	}

        public boolean action(Event evt, Object arg)
        {
                if (arg.equals("Simulate")) {
			/*
			double mixx = SL.atof(Minx.getText());
			double maxx = SL.atof(Maxx.getText());
			double mixy = SL.atof(Miny.getText());
			double maxy = SL.atof(Maxy.getText());
			*/
			mc.stop();
			mc.start();
                } else {
                        return super.action(evt, arg);
                }
                return true;
        }

        public boolean handleEvent(Event evt)
        {
                if (evt.id == Event.WINDOW_DESTROY) System.exit(0);
                return super.handleEvent(evt);
        }
}
