# Julia Set Fractal

Part of [Prof. Robert Vanderbei's Java Applications](https://pubino.github.io/vanderbei-apps#julia-sim).

A standalone Java application for visualizing Julia set fractals by Professor Robert Vanderbei, Princeton University.

## Requirements

- Java 14+ (for running the JAR)
- Java 14+ with `jpackage` (for building macOS app bundle)

## Building

```bash
# Build the JAR file
make jar

# Build macOS .app bundle (unsigned)
make app
```

## Running

```bash
# Run the JAR
make run

# Or run directly
java -jar dist/JuliaSim.jar
```

## Usage

1. Adjust the coordinate bounds (minx, maxx, miny, maxy) to explore different regions
2. Click "Simulate" to start the fractal visualization
3. The animation shows points escaping to infinity, revealing the Julia set structure

## Project Structure

```
julia-sim/
├── julia/
│   ├── Julia.java          # Main application entry point
│   └── JuliaCanvas.java    # Fractal rendering canvas
├── myutil/
│   ├── AppletFrame.java    # Applet-to-Frame wrapper
│   ├── Format.java         # Number formatting utilities
│   ├── GL.java             # Graphics library helpers
│   └── SL.java             # String parsing utilities
├── Makefile                # Build configuration
└── .github/workflows/      # CI/CD configuration
```
