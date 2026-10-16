import asyncio, math, pathlib
from scipy.stats import nct,t, norm
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
async def main():
 async with async_playwright() as p:
  br=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await br.new_page(viewport={'width':1250,'height':900})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content((ROOT/'index.html').read_text())
  assert await page.inner_text('#totalN')=='128', ('default',await page.inner_text('#totalN'),await page.inner_text('#err'))
  await page.select_option('#allocationMode','unequal')
  await page.fill('#allocationWeight_0','1')
  await page.fill('#allocationWeight_1','2')
  data=await page.evaluate('''() => {let x=GNDebug.state.last;return {n:x.n,counts:x.counts,N:x.counts.reduce((a,b)=>a+b,0),alpha:x.v.alpha,effect:x.v.effect,power:x.res.power,summary:x.summary}}''')
  assert data['counts']==[data['n'],2*data['n']],data
  crit=t.ppf(1-data['alpha']/2,data['N']-2)
  delta=data['effect']*math.sqrt(data['counts'][0]*data['counts'][1]/data['N'])
  expected=nct.sf(crit,data['N']-2,delta)+nct.cdf(-crit,data['N']-2,delta)
  assert abs(expected-data['power'])<1e-6,(data,expected)
  print('2:1 unequal t',data['counts'], data['power'], 'reference',expected)
  await page.select_option('#power','custom');await page.fill('#customPower','87.5')
  custom=await page.evaluate('''() => {let x=GNDebug.state.last;return {p:x.v.power,counts:x.counts,summary:x.summary}}''')
  assert abs(custom['p']-.875)<1e-10, custom
  assert '87.5%' in custom['summary'],custom
  print('custom power 87.5%',custom['counts'])
  await page.select_option('#quickstart','two_mixed')
  assert await page.inner_text('#testName')=='Two-way mixed-design ANOVA'
  assert await page.locator('#allocationArea').is_visible()
  await page.select_option('#allocationMode','unequal')
  await page.fill('#allocationWeight_0','1');await page.fill('#allocationWeight_1','2')
  data2=await page.evaluate('''() => {let x=GNDebug.state.last;return {n:x.n,counts:x.counts,lambda:x.res.lambda,alpha:x.v.alpha,power:x.res.power,summary:x.summary,eq:x.res.eq}}''')
  assert 'conservative' in data2['summary'],data2
  print('unequal mixed',data2['counts'],data2['power'])
  # Switch to regression with categorical factor, ensure still works with separate allocation.
  await page.select_option('#quickstart','reg_dummy')
  await page.select_option('#allocationMode','unequal')
  await page.fill('#allocationWeight_0','2')
  assert 'partial f²' in await page.inner_text('#caution')
  # Regression with covariates carries assumption rather than exact effect adjustment.
  await page.select_option('#quickstart','two_mixed')
  await page.select_option('#allocationMode','unequal')
  await page.fill('#allocationWeight_0','2')
  await page.fill('#covariates','1');await page.locator('#covariates').dispatch_event('change')
  assert 'requires assumptions about covariate imbalance' in await page.inner_text('#err')
  # One sample, paired, correlation don't inadvertently require allocations.
  await page.select_option('#quickstart','pearson')
  assert not await page.locator('#allocationArea').is_visible()
  assert await page.inner_text('#totalN')!='—',(await page.inner_text('#err'))
  await page.select_option('#quickstart','paired_t')
  assert not await page.locator('#allocationArea').is_visible()
  assert await page.inner_text('#totalN')!='—',(await page.inner_text('#err'))
  assert not errors,errors
  await br.close()
asyncio.run(main())
