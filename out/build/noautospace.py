import uno, sys, time, subprocess
from com.sun.star.beans import PropertyValue

def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p

proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                         "--accept=socket,host=localhost,port=2002;urp;"])
ctx = uno.getComponentContext()
res = ctx.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", ctx)
for _ in range(60):
    try:
        c = res.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception:
        time.sleep(1)
desk = c.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", c)
doc = desk.loadComponentFromURL(uno.systemPathToFileUrl(sys.argv[1]), "_blank", 0, (pv("Hidden", True),))
n = 0

def walk(shapes):
    global n
    for i in range(shapes.getCount()):
        sh = shapes.getByIndex(i)
        if sh.supportsService("com.sun.star.drawing.GroupShape"):
            walk(sh); continue
        try:
            en = sh.getText().createEnumeration()
        except Exception:
            continue
        while en.hasMoreElements():
            p = en.nextElement()
            try:
                p.setPropertyValue("ParaIsCharacterDistance", False); n += 1
            except Exception:
                pass

pages = doc.getDrawPages()
for i in range(pages.getCount()):
    walk(pages.getByIndex(i))
print("paras", n)
doc.storeToURL(uno.systemPathToFileUrl(sys.argv[2]), (pv("FilterName", "impress_pdf_Export"),))
doc.close(True)
try:
    desk.terminate()
except Exception:
    pass
proc.wait(timeout=30)
