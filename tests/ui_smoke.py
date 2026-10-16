import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':425,'height':900})
  errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  await page.set_content((ROOT/'index.html').read_text())
  await page.screenshot(path=str(ROOT/'preview_mobile.png'),full_page=True)
  assert await page.inner_text('#totalN')=='128'
  await page.select_option('#ivType','continuous')
  assert await page.input_value('#goal')=='regression'
  assert (await page.locator('[data-factor]').count())==0
  print('continuous IV',await page.inner_text('#testName'),await page.inner_text('#totalN'))
  await page.select_option('#ivType','both')
  assert (await page.locator('[data-factor]').count())==1
  print('mixed predictors',await page.inner_text('#testName'))
  await page.select_option('#goal','correlation')
  assert await page.inner_text('#totalN')=='85'
  assert (await page.input_value('#ivType'))=='continuous'
  print('correlation without hidden group',await page.inner_text('#totalN'))
  await page.select_option('#goal','reference')
  assert await page.inner_text('#totalN')=='34'
  assert (await page.input_value('#ivType'))=='none'
  print('one sample without hidden group',await page.inner_text('#totalN'))
  await page.select_option('#quickstart','two_mixed')
  await page.select_option('#effectKind','main')
  await page.select_option('#mainFactor','f2')
  assert await page.input_value('#mainFactor')=='f2'
  print('selected main B persisted',await page.inner_text('#targetExplain'))
  await page.select_option('#effectKind','interaction')
  assert await page.inner_text('#totalN')=='28'
  await page.select_option('#outcome','binary')
  assert await page.inner_text('#totalN')=='—'
  await page.select_option('#outcome','numeric')
  await page.select_option('#quickstart','ind_t')
  await page.select_option('#outcome','binary')
  await page.locator('#effectHelper').evaluate('(x)=>x.open=true')
  await page.fill('#hp0','0.2');await page.fill('#hp1','0.5')
  await page.locator('#applyHelper').click()
  print('binary baseline set',await page.input_value('#baselineRate'), await page.inner_text('#totalN'))
  assert abs(float(await page.input_value('#baselineRate'))-.2)<1e-6
  print('JS error count',len(errs))
  await browser.close()
asyncio.run(main())
