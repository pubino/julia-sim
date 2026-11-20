# Julia Set Fractal

[Run in your browser](https://pubino.github.io/julia-sim/).

The browser port keeps the Java app's 300 × 300 grid, zero initial state,
and adaptive threshold. Each sample uses its own complex coordinate as
the constant in the recurrence. Use **Step** to inspect one frame or
set bounds to explore a region of the plane.

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

## Browser development

Preview with Docker or Python 3.13 and uv.

```sh
docker-compose up --build preview
uv sync --locked
uv run python scripts/build_site.py
uv run python -m http.server 8000 --bind 127.0.0.1 --directory build/site
```

Run the Java parity, Chromium, lint, and type checks used in CI.

```sh
docker-compose run --build --rm -T js-check
docker-compose run --build --rm -T test
```
