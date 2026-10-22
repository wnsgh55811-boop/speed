import uno, sys, time, subprocess
from com.sun.star.beans import PropertyValue
src, dst = sys.argv[1], sys.argv[2]
p = subprocess.Popen(["soffice","--headless","--invisible","--norestore",'--accept=socket,host=localhost,port=2002;urp;'])
ctx=None
for _ in range(60):
    try:
        lc = uno.getComponentContext()
        res = lc.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", lc)
        ctx = res.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception: time.sleep(1)
desk = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
def pv(n,v):
    x=PropertyValue(); x.Name=n; x.Value=v; return x
doc = desk.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0, (pv("Hidden",True),))
cnt=0
def fix_text(t):
    global cnt
    try:
        en = t.createEnumeration()
        while en.hasMoreElements():
            para = en.nextElement()
            try:
                para.ParaIsCharacterDistance = False; cnt+=1
            except Exception: pass
    except Exception: pass
def walk(sh):
    if sh.supportsService("com.sun.star.drawing.GroupShape"):
        for i in range(sh.Count): walk(sh.getByIndex(i))
        return
    if sh.ShapeType=="com.sun.star.drawing.TableShape":
        m = sh.Model
        for r in range(m.Rows.Count):
            for c in range(m.Columns.Count):
                cell=m.getCellByPosition(c,r)
                global cnt
                try:
                    cur=cell.createTextCursor(); cur.gotoStart(False); cur.gotoEnd(True)
                    cur.ParaIsCharacterDistance=False; cnt+=1
                except Exception as ex: print('cellerr',ex)
                try:
                    en=cell.createEnumeration()
                    while en.hasMoreElements():
                        en.nextElement().ParaIsCharacterDistance=False
                except Exception as ex: print('cellenum',ex)
        return
    try: fix_text(sh.Text)
    except Exception: pass
pages = doc.DrawPages
for i in range(pages.Count):
    pg = pages.getByIndex(i)
    for j in range(pg.Count): walk(pg.getByIndex(j))
print("paras fixed", cnt)
doc.storeToURL(uno.systemPathToFileUrl(dst), (pv("FilterName","impress_pdf_Export"),))
doc.close(True)
try: desk.terminate()
except Exception: pass
p.wait(timeout=30)
