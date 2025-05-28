import sys, pathlib, base64, os
sys.path.append("packages/vision/form")
import vision

def test_form():
    import pathlib, base64
    img = base64.b64encode(pathlib.Path("tests/vision/cat.jpg").read_bytes()).decode()
    vis = vision.Vision({})
    res = vis.decode(img)
    print("Decode result:", res)  # <-- qui la stampa di debug
    assert res.find("cat") != -1
