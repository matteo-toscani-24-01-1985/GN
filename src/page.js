/* Navigation and provisional citation for the single-file beta app. */
(function(){
  const calculator=document.getElementById('calculatorPage');
  const about=document.getElementById('about');
  const aboutLink=document.getElementById('aboutNav');
  const calcLink=document.getElementById('calcNav');
  function updatePage(){
    const showAbout=window.location.hash==='#about';
    calculator.classList.toggle('hidden',showAbout);
    about.classList.toggle('hidden',!showAbout);
    aboutLink.classList.toggle('active',showAbout);
    calcLink.classList.toggle('active',!showAbout);
    if(showAbout){window.scrollTo(0,0);}  // reveal top of the About screen
    document.title=showAbout?'About & Cite — GN v1.0 beta':'GN v1.0 beta — Guided Statistical Power Analysis';
  }
  window.addEventListener('hashchange',updatePage);
  updatePage();
  document.getElementById('copyCitation').addEventListener('click',async()=>{
    const text=document.getElementById('softwareCitation').textContent.trim();
    const status=document.getElementById('citationStatus');
    try{
      if(!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text);
      status.textContent='Citation copied. Check version and release status before citing.';
    }catch(_e){
      status.textContent='Select and copy the citation text above; clipboard access is unavailable here.';
    }
  });
})();
