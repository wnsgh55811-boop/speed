# usage: shots.py html outdir t1 t2 ...
import sys,asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',args=['--disable-gpu'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+sys.argv[1]); await pg.evaluate('window.__ready'); await pg.wait_for_timeout(300)
        for t in sys.argv[3:]:
            await pg.evaluate(f'window.__seek({t})'); await pg.screenshot(path=f'{sys.argv[2]}/t{float(t):07.2f}.png')
        await b.close()
asyncio.run(main())
