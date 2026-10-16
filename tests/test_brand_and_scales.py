"""Smoke-check GN branding, scale guardrail, main result, and report text."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parents[1]

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = await browser.new_page(viewport={'width': 1440,'height': 1000}, device_scale_factor=1)
        errors=[]
        page.on('pageerror', lambda e:errors.append(str(e)))
        await page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        assert await page.title() == 'GN v1.0 beta — Guided Statistical Power Analysis'
        assert 'GN' in await page.locator('.brand').inner_text()
        assert await page.locator('#totalN').inner_text() == '128'
        assert 'GN v1.0 beta' in await page.locator('#summary').inner_text()
        assert 'systolic blood pressure' in await page.locator('#outcome').inner_text()
        assert 'anxiety' not in (await page.locator('body').inner_text()).lower()
        await page.screenshot(path=str(ROOT/'preview_desktop.png'),full_page=True)
        await page.select_option('#outcome','other')
        assert await page.locator('#totalN').inner_text() == '—'
        assert await page.locator('#err').is_visible()
        assert 'ordinal' in (await page.locator('#err').inner_text()).lower()
        await page.select_option('#outcome','numeric')
        await page.select_option('#power','custom')
        await page.fill('#customPower','87.5')
        assert '87.5%' in await page.locator('#summary').inner_text()
        assert not errors, errors
        mob = await browser.new_page(viewport={'width':390,'height':844}, device_scale_factor=1)
        await mob.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        assert await mob.locator('#totalN').inner_text() == '128'
        await mob.screenshot(path=str(ROOT/'preview_mobile.png'),full_page=True)
        await browser.close()
        print('GN branding, ordinal guardrail, custom power, desktop and mobile smoke tests passed.')

if __name__=='__main__':
    asyncio.run(main())
