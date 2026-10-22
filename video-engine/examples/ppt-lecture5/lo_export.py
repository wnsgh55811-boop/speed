import uno, sys, time, subprocess
from com.sun.star.beans import PropertyValue
def pv(n,v):
    p=PropertyValue(); p.Name=n; p.Value=v; return p
src, dst = sys.argv[1], sys.argv[2]
proc = subprocess.Popen(["soffice","--headless","--invisible","--norestore","--accept=socket,host=127.0.0.1,port=2002;urp;"])
ctx=None
for _ in range(60):
    try:
        local=uno.getComponentContext()
        res=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
        ctx=res.resolve("uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext"); break
    except Exception: time.sleep(1)
desk=ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
doc=desk.loadComponentFromURL(uno.systemPathToFileUrl(src),"_blank",0,(pv("Hidden",True),))
n=0
def fix_text(t):
    global n
    try:
        t.setPropertyValue("ParaIsCharacterDistance",False); n+=1000
    except Exception: pass
    try:
        e=t.getText().createEnumeration()
    except Exception: return
    while e.hasMoreElements():
        p=e.nextElement()
        try:
            p.setPropertyValue("ParaIsCharacterDistance",False); n+=1
        except Exception as ex: pass
def walk(sh):
    if sh.supportsService("com.sun.star.drawing.GroupShape"):
        for i in range(sh.getCount()): walk(sh.getByIndex(i))
        return
    if sh.supportsService("com.sun.star.drawing.TableShape"):
        m=sh.Model
        for r in range(m.Rows.Count):
            for c in range(m.Columns.Count):
                cell=m.getCellByPosition(c,r)
                fix_text(cell)
                try:
                    cur=cell.createTextCursor(); cur.gotoStart(False); cur.gotoEnd(True)
                    cur.setPropertyValue("ParaIsCharacterDistance",False)
                except Exception as ex: print("cur",ex)
        return
    fix_text(sh)
fams=doc.getStyleFamilies()
for fn in fams.getElementNames():
    fam=fams.getByName(fn)
    for sn in fam.getElementNames():
        st=fam.getByName(sn)
        try:
            st.setPropertyValue("ParaIsCharacterDistance",False); print("style",fn,sn)
        except Exception: pass
pages=doc.getDrawPages()
for i in range(pages.getCount()):
    pg=pages.getByIndex(i)
    for j in range(pg.getCount()): walk(pg.getByIndex(j))
print("paragraphs fixed",n)
doc.storeToURL(uno.systemPathToFileUrl(dst),(pv("FilterName","impress_pdf_Export"),))
doc.close(True)
try: desk.terminate()
except Exception: pass
proc.wait(timeout=30)
