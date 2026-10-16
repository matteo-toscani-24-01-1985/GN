import asyncio, json,csv
from scipy.stats import ncf,nct,t,norm,f as fdist
from playwright.async_api import async_playwright
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

cases=[('independent_t','ind_t',None,None,.5,None),('one_sample_t','one_t',None,None,.5,None),('paired_t','paired_t',None,None,.5,None),('one_way_between','one_anova',None,None,.25,None),('one_way_repeated','rm_anova',None,None,.25,.5),('one_way_repeated_rho80','rm_anova',None,None,.25,.8),('two_between_main','two_between','main',None,.25,None),('two_between_interaction','two_between','interaction',None,.25,None),('two_mixed_main_A','two_mixed','main',None,.25,.5),('two_mixed_main_Time','two_mixed','main','f2',.25,.5),('two_mixed_interaction','two_mixed','interaction',None,.25,.5),('three_within_main','three_within','main',None,.25,.5),('three_mixed_threeway','three_mixed','interaction','ALL',.25,.5),('regression_overall','reg_cont','overall',None,.15,None),('regression_covariate','reg_cont','covariate',None,.15,None),('regression_dummy_factor','reg_dummy','main','f2',.15,None),('regression_dummy_interaction','reg_dummy','interaction',None,.15,None),('correlation','pearson',None,None,.3,None)]
async def main():
 out=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page()
  await page.set_content((ROOT/'index.html').read_text())
  for name,shortcut,kind,factor,effect,rho in cases:
   await page.select_option('#quickstart',shortcut)
   if kind and kind!=await page.input_value('#effectKind'):
    await page.select_option('#effectKind',kind)
   if factor=='ALL':
    for x in await page.locator('[data-int]').all(): await x.check()
   elif factor and kind=='main':await page.select_option('#mainFactor',factor)
   if rho is not None:
    await page.fill('#rho',str(rho));await page.locator('#rho').dispatch_event('change')
   await page.fill('#effectValue',str(effect));await page.locator('#effectValue').dispatch_event('change')
   data=await page.evaluate('''() => {let p=GNDebug.getPlan(),n=GNDebug.state.last.n,v=GNDebug.state.last.v,r=GNDebug.state.last.res;return {plan:{test:p.test.id,B:p.B,M:p.M,d1:p.d1,df1:r.df1,df2:r.df2,hasWithin:p.hasWithin,kind:p.kind,ids:p.ids,p:p.p},N:n*p.B,perCell:n,power:r.power,effect:v.effect,rho:v.rho,lambda:r.lambda,alpha:v.alpha,error:document.getElementById('err').textContent}}''')
   pl=data['plan'];test=pl['test'];n=data['perCell'];df2=pl['df2'];df1=pl['df1'];alpha=data['alpha'];delta=None
   if test in ['ti','tp','t1']:
    delta=effect*(n/2)**.5 if test=='ti' else effect*n**.5
    crit=t.ppf(1-alpha/2,df2)
    expected=nct.sf(crit,df2,delta)+nct.cdf(-crit,df2,delta)
   elif test=='corr':
    crit=norm.ppf(1-alpha/2);z=__import__('math').atanh(effect)*(n-3)**.5
    expected=norm.sf(crit-z)+norm.cdf(-crit-z)
   else:expected=ncf.sf(fdist.ppf(1-alpha,df1,df2),df1,df2,data['lambda'])
   err=abs(data['power']-expected)
   data.update(name=name,scipy_power=expected,abs_difference=err)
   out.append(data)
   if err>1.5e-5:print('CHECK',name,err)
   print(name, 'n=', data['N'], 'power=',round(data['power'],8),'ref=',round(expected,8),'err=',round(err,10),flush=True)
  await browser.close()
 keys=['name','N','perCell','power','scipy_power','abs_difference','effect','rho','lambda','alpha','plan','error']
 with open(str(ROOT/'validation'/'gn_v1_validation.csv'),'w',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=keys);wr.writeheader();wr.writerows({**row,'plan':json.dumps(row['plan'])} for row in out)
 m=max(x['abs_difference'] for x in out)
 with open(str(ROOT/'validation'/'gn_v1_validation.md'),'w') as f:
  f.write(f'# GN v1.0 beta — Numerical cross-checks\n\n{len(out)} distinct design/effect combinations checked against SciPy 1.17.0 reference distributions. Maximum absolute power discrepancy in this set: {m:.2g}.\n\n')
  f.write('These checks compare computed power at the app-selected sample size. They do not constitute comprehensive validation of software behavior, unbalanced or heteroscedastic designs, repeated covariance assumptions, applicability to real research designs, or educational utility.\n\n')
  f.write('| Case | Sample | Browser power | SciPy power | Absolute difference |\n|---|---:|---:|---:|---:|\n')
  for x in out:f.write(f"| {x['name']} | {x['N']} | {x['power']:.6f} | {x['scipy_power']:.6f} | {x['abs_difference']:.2g} |\n")
  f.write('\n## Approximations / definitions\n- t tests: two-sided noncentral t.\n- ANOVA: univariate, balanced, equal within-occasion variance and compound-symmetric repeated covariance, noncentral F.\n- Regressions: block F with lambda = N*f² and p = design-matrix parameter count; covariate correlations are not separately specified.\n- Correlation: Fisher z large-sample approximation, reproduced at the same approximation in SciPy.\n- Binary rates use a normal approximation; full coverage deferred.\n')
 print('MAX',m)
asyncio.run(main())
