(() => {
 const root=document.documentElement,overlay=document.querySelector('#brand-intro');
 if(!overlay)return;
 const skip=overlay.querySelector('#intro-skip'),acts=[...overlay.querySelectorAll('[data-intro-act]')];
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const content=[...document.querySelectorAll('.site-header,main,.footer')];
 let timers=[],playing=false,closing=false,returnFocus=null,generation=0;
 const later=(fn,ms)=>{const id=setTimeout(fn,ms);timers.push(id);return id;};
 const clearTimers=()=>{timers.forEach(clearTimeout);timers=[];};
 const remember=()=>{try{sessionStorage.setItem('jhg-brand-intro-v1','seen');}catch{}};
 function finish(){
  if(!playing)return;
  playing=false;closing=true;generation++;clearTimers();remember();
  overlay.classList.add('is-leaving');root.classList.remove('intro-pending');root.classList.add('intro-revealing');
  skip.disabled=true;
  later(()=>{
   overlay.classList.remove('is-playing','is-leaving');overlay.setAttribute('aria-hidden','true');
   content.forEach(el=>el.inert=false);closing=false;skip.disabled=false;
   if(overlay.contains(document.activeElement)){
    if(returnFocus&&returnFocus.isConnected)returnFocus.focus({preventScroll:true});
    else{const main=document.querySelector('main');main.tabIndex=-1;main.focus({preventScroll:true});}
   }
  },reduced.matches?0:1100);
  later(()=>root.classList.remove('intro-revealing'),1500);
 }
 function act(index){
  overlay.dataset.act=acts[index].dataset.introAct;
  acts.forEach((el,i)=>el.classList.toggle('is-active',i===index));
 }
 async function start(){
  if(reduced.matches){root.classList.remove('intro-pending');return;}
  if(playing||closing)return;
  clearTimers();root.classList.remove('intro-revealing');playing=true;const run=++generation;
  returnFocus=document.activeElement?.closest('[data-replay-intro]')||null;
  overlay.classList.remove('is-leaving');overlay.classList.add('is-playing');overlay.setAttribute('aria-hidden','false');
  root.classList.add('intro-pending');content.forEach(el=>el.inert=true);act(0);skip.focus({preventScroll:true});
  // Decode the incoming marks before starting the sequence. Both layers remain
  // mounted so outgoing and incoming logos overlap for the full crossfade.
  await Promise.race([
   Promise.all([...overlay.querySelectorAll('img')].map(img=>img.decode?img.decode().catch(()=>{}):Promise.resolve())),
   new Promise(resolve=>later(resolve,1800))
  ]);
  if(run!==generation||!playing)return;
  overlay.classList.add('sequence-ready');
  [2300,4600,6900].forEach((ms,i)=>later(()=>act(i+1),ms));
  later(finish,9200);
 }
 skip.addEventListener('click',finish);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&playing)finish();});
 reduced.addEventListener('change',()=>{if(reduced.matches)finish();});
 document.querySelectorAll('[data-replay-intro]').forEach(button=>button.addEventListener('click',()=>{overlay.classList.remove('sequence-ready');start();}));
 if(root.classList.contains('intro-pending'))start();
})();
