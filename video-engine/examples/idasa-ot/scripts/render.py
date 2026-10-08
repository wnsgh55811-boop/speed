# usage: render.py html out_dir fps start_frame end_frame worker_id  -> writes seg_{id}.mp4 (video only)
import sys,subprocess,asyncio
from playwright.async_api import async_playwright
html,outd,fps,f0,f1,wid=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',args=['--disable-gpu','--force-color-profile=srgb','--disable-lcd-text'])
        pg=await b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
        await pg.goto('file://'+html); await pg.evaluate('window.__ready'); await pg.wait_for_timeout(500)
        ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(fps),'-c:v','png','-i','-',
            '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-profile:v','high','-g',str(fps*2),
            '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',f'{outd}/seg_{wid}.mp4'],stdin=subprocess.PIPE)
        for f in range(f0,f1):
            await pg.evaluate(f'window.__seek({f/fps:.6f})')
            png=await pg.screenshot(type='png')
            ff.stdin.write(png)
            if (f-f0)%300==0: print(wid,f,flush=True)
        ff.stdin.close(); ff.wait(); await b.close()
asyncio.run(main())
