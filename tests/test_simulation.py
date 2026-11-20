import hashlib
import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path

from web.simulation import create

ROOT = Path(__file__).resolve().parents[1]
BOUNDS = [[-2, 2, -2, 2], [-0.82, -0.65, 0.03, 0.17], [1, 1.6, -0.4, 0.2]]


class FractalTest(unittest.TestCase):
    def test_original_threshold_and_full_sample_masks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    "javac",
                    "--release",
                    "25",
                    "-d",
                    directory,
                    ROOT / "julia/JuliaCanvas.java",
                    ROOT / "julia/Julia.java",
                    ROOT / "myutil/SimApp.java",
                    ROOT / "myutil/AppletFrame.java",
                    ROOT / "myutil/SL.java",
                    ROOT / "myutil/Format.java",
                    ROOT / "tests/GL.java",
                    ROOT / "tests/FractalReference.java",
                ],
                check=True,
                timeout=30,
            )
            output = subprocess.check_output(
                [
                    "java",
                    "-Djava.awt.headless=true",
                    "-cp",
                    directory,
                    "julia.FractalReference",
                ],
                text=True,
                timeout=30,
                stderr=subprocess.DEVNULL,  # Legacy per-frame trace.
            )
        models = [create(json.dumps(bounds)) for bounds in BOUNDS]
        records = output.splitlines()
        self.assertEqual(len(records), 12)
        for line in records:
            case, step, threshold, mask, real, imag = line.split(",")
            model, target = models[int(case)], int(step)
            with self.subTest(case=case, step=step):
                while model.steps < target:
                    model.advance(min(target - model.steps, 16))
                self.assertEqual(hashlib.sha256(model.dark.tobytes()).hexdigest(), mask)
                self.assertTrue(
                    math.isclose(model.threshold, float(threshold), rel_tol=2e-12)
                )
                self.assertTrue(
                    math.isclose(model.real[299, 150], float(real), rel_tol=2e-12)
                )
                self.assertTrue(
                    math.isclose(model.imag[299, 150], float(imag), rel_tol=2e-12)
                )

    def test_screen_order_and_bounds(self) -> None:
        model = create("[-2,2,-2,2]")
        model.dark[17, 298] = True
        self.assertEqual(model.frame()[3][300 + 17], 1)
        for bounds in ("[2,-2,-2,2]", "[-2,2,0,0]", "[0,1e-15,0,1]", "[NaN,1,0,1]"):
            with self.subTest(bounds=bounds), self.assertRaises(ValueError):
                create(bounds)
