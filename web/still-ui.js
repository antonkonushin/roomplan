// Optional expensive export stays separate from the immediate viewport snapshot.
export function openPhysicalExport({scene,modal,closeModal,download}){
 modal('<div class="eyebrow">ФИЗИЧЕСКИЙ СВЕТ</div><h2 class="modal-title">Кадр из модели</h2><p class="modal-subtitle">Расчёт отражений и непрямого света в текущей 3D-сцене. Может занять несколько минут.</p><label class="field">Качество<select id="still-quality" class="modal-select"><option value="preview">Проба · 800 × 500 · 16 сэмплов</option><option value="standard" selected>Стандарт · 1200 × 750 · 96 сэмплов</option><option value="high">Детально · 1600 × 1000 · 192 сэмпла</option></select></label><button id="still-start" class="button primary full">Рассчитать PNG</button><button id="still-cancel" class="button full" disabled>Отменить расчёт</button><div class="modal-status" id="still-status">Рендер использует текущий ракурс. Для вида из комнаты выберите «Интерьерный ракурс» в экспорте.</div>');
 const $=s=>document.querySelector(s);let controller;
 $('#still-cancel').onclick=()=>controller?.abort();
 $('#still-start').onclick=async()=>{
  const choice=$('#still-quality').value,config={preview:{samples:16,width:800,height:500,maxSeconds:120},standard:{samples:96,width:1200,height:750,maxSeconds:300},high:{samples:192,width:1600,height:1000,maxSeconds:600}}[choice];
  const start=$('#still-start'),cancel=$('#still-cancel'),quality=$('#still-quality'),close=$('#modal-close'),oldClose=close.onclick;
  controller=new AbortController();start.disabled=true;quality.disabled=true;cancel.disabled=false;close.onclick=()=>{controller.abort();closeModal()};
  try{const url=await scene.renderStill({...config,signal:controller.signal,onProgress:(fraction,info)=>{const status=$('#still-status');if(status)status.textContent=info.phase+' · '+Math.round(fraction*100)+'%'+(info.total?' · '+info.samples+'/'+info.total:'')}});download(await (await fetch(url)).blob(),'roomplan-физический-рендер.png');if($('#still-status'))$('#still-status').textContent='PNG сохранён. Использована геометрия текущего проекта.'}
  catch(e){if($('#still-status'))$('#still-status').textContent=e.message}
  finally{start.disabled=false;quality.disabled=false;cancel.disabled=true;close.onclick=oldClose}
 };
}
