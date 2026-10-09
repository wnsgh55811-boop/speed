# resumable: render.py-like but iterates chunks; usage: html outdir fps total chunk worker nworkers
import sys,subprocess,asyncio,os
from playwright.async_api import async_playwright
html,outd,fps,N,C,wid,nw=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7])
chunks=[(a,min(a+C,N)) for a in range(0,N,C)]
mine=[c for k,c in enumerate(chunks) if k%nw==wid]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',args=['--disable-gpu','--force-color-profile=srgb'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+html); await pg.evaluate('window.__ready'); await pg.wait_for_timeout(500)
        for a,e in mine:
            out=f'{outd}/c{a:06d}.mp4'
            if os.path.exists(out): continue
            tmp=out+'.part.mp4'
            ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(fps),'-c:v','png','-i','-',
              '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-profile:v','high','-g',str(fps*2),
              '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',tmp],stdin=subprocess.PIPE)
            for f in range(a,e):
                await pg.evaluate(f'window.__seek({f/fps:.6f})')
                ff.stdin.write(await pg.screenshot(type='png'))
            ff.stdin.close(); ff.wait(); os.rename(tmp,out); print(wid,'done',a,flush=True)
        await b.close()
asyncio.run(main())
