import osascript

osascript.run("set volume output volume 50")
code, out, err = osascript.run("output volume of (get volume settings)")
print(out)