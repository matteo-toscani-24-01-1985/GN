"""Check the About & cite screen and beta authorship/citation metadata."""
from pathlib import Path
import asyncio
import yaml
from playwright.async_api import async_playwright, expect

ROOT=Path(__file__).resolve().parents[1]

async def main():
    cff=yaml.safe_load((ROOT/'CITATION.cff').read_text(encoding='utf-8'))
    assert len(cff['authors'])==2
    assert cff['authors'][1]['given-names']=='Anna'
    assert cff['authors'][1]['family-names']=='Metzger'
    assert cff['authors'][0]['family-names']=='Toscani'
    for width,height,preview in [(1400,950,'preview_about_desktop.png'),(390,844,'preview_about_mobile.png')]:
        async with async_playwright() as p:
            browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            page=await browser.new_page(viewport={'width':width,'height':height})
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            await page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
            assert await page.locator('#totalN').inner_text()=='128'
            await page.locator('#aboutNav').click()
            assert await page.title() == 'About & Cite — GN v1.0 beta'
            assert await page.locator('#about').is_visible()
            assert not await page.locator('#calculatorPage').is_visible()
            assert await page.get_by_role('heading',name='Developed by').is_visible()
            assert await page.get_by_text('Anna Metzger').is_visible()
            assert await page.get_by_text('Matteo Toscani').is_visible()
            assert 'provisional' in (await page.locator('#about').inner_text()).lower()
            assert await page.locator('#copyCitation').is_visible()
            await page.screenshot(path=str(ROOT/preview),full_page=True)
            await page.locator('#copyCitation').click()
            assert await page.locator('#citationStatus').inner_text()
            await page.locator('.about-back a').click()
            await expect(page.locator('#calculatorPage')).to_be_visible()
            assert await page.locator('#totalN').inner_text()=='128'
            assert not errors,errors
            await browser.close()
    print('About & cite navigation, CFF authors, beta attribution, and desktop/mobile views passed.')

if __name__=='__main__':
    asyncio.run(main())
