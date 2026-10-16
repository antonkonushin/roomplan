import * as THREE from 'three';
import {WebGLPathTracer,GradientEquirectTexture,DenoiseMaterial} from './vendor/three-gpu-pathtracer/src/index.js';
import {FullScreenQuad} from 'three/addons/postprocessing/Pass.js';

function cloneForTracing(room){
 const hidden=[room.labels,room.dimensionGroup,room.boxGroup,room.research,room.cameras,room.selectionBox].filter(Boolean),visible=hidden.map(g=>g.visible);hidden.forEach(g=>g.visible=false);
 let scene;try{scene=room.scene.clone(true)}finally{hidden.forEach((g,i)=>g.visible=visible[i])}
 const geometries=new Map(),materials=new Map(),textures=new Map();
 const texture=t=>{if(!textures.has(t)){
  // Texture.copy shares Source and increments its version; preserve editor source state.
  const version=t.source.version,copy=t.clone();t.source.version=version;let data=t.source.data;
  if(data?.data&&ArrayBuffer.isView(data.data))data={...data,data:new data.data.constructor(data.data)};
  else if(data?.width&&data?.height){const canvas=document.createElement('canvas');canvas.width=data.width;canvas.height=data.height;canvas.getContext('2d').drawImage(data,0,0);data=canvas;}
  copy.source=new THREE.Source(data);copy.needsUpdate=true;textures.set(t,copy);
 }return textures.get(t)};
 const material=m=>{if(!materials.has(m)){const copy=m.clone();for(const key in copy)if(copy[key]?.isTexture)copy[key]=texture(copy[key]);materials.set(m,copy)}return materials.get(m)};
 scene.traverse(o=>{if(o.userData.physicalOnly)o.visible=true;if(o.isMesh){if(!geometries.has(o.geometry))geometries.set(o.geometry,o.geometry.clone());o.geometry=geometries.get(o.geometry);o.material=Array.isArray(o.material)?o.material.map(material):material(o.material)}});
 return {scene,dispose(){for(const m of materials.values())m.dispose();for(const t of textures.values())t.dispose();for(const g of geometries.values())g.dispose()}};
}
function targetStatistics(renderer,target){const values=[];for(const u of [.2,.5,.8])for(const v of [.2,.5,.8]){const p=new Float32Array(4);renderer.readRenderTargetPixels(target,Math.floor(target.width*u),Math.floor(target.height*v),1,1,p);values.push([...p])}return {width:target.width,height:target.height,type:target.texture.type,pixels:values,finite:values.flat().every(Number.isFinite),max:Math.max(...values.map(p=>Math.max(...p.slice(0,3))))};}

// Separate WebGL context and fully owned material/texture copies isolate the interactive editor.
export async function renderPhysical(room,{samples=96,width=1200,height,onProgress=()=>{},signal,maxSeconds=180,denoise=true}={}){
 await room.awaitAssets();if(room.mode!=='3d')throw new Error('Для физического рендера выберите 3D-ракурс.');if(room.recording)throw new Error('Дождитесь завершения текущего экспорта.');
 const camera=room.camera.clone(),enabled=room.controls.enabled,start=performance.now();
 width=Math.max(320,Math.min(1920,Math.round(width)));height=Math.max(240,Math.min(1440,Math.round(height||width/camera.aspect)));samples=Math.max(8,Math.min(512,Math.round(samples)));
 let renderer,owned,env,quad,shaderFailure;room.recording=true;room.controls.enabled=false;
 try{
 onProgress(0,{phase:'Подготовка геометрии',samples:0,total:samples});await new Promise(r=>setTimeout(r,0));
 renderer=new THREE.WebGLRenderer({canvas:document.createElement('canvas'),antialias:false,alpha:false,preserveDrawingBuffer:true});renderer.setPixelRatio(1);renderer.setSize(width,height,false);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=room.renderer.toneMapping;renderer.toneMappingExposure=room.renderer.toneMappingExposure;renderer.debug.onShaderError=(gl,program)=>{shaderFailure=gl.getProgramInfoLog(program)||'Шейдер не скомпилирован'};
 camera.aspect=width/height;camera.updateProjectionMatrix();camera.updateMatrixWorld();owned=cloneForTracing(room);const scene=owned.scene;
 env=new GradientEquirectTexture(128);env.topColor.set('#dce9ff');env.bottomColor.set('#f1ece1');env.update();scene.environment=env;scene.environmentIntensity=.35;scene.background=new THREE.Color('#eef1f3');scene.backgroundIntensity=1;
 const tracer=new WebGLPathTracer(renderer);tracer.textureSize.set(512,512);tracer.tiles.set(2,2);tracer.bounces=6;tracer.transmissiveBounces=4;tracer.filterGlossyFactor=.5;tracer.renderDelay=0;tracer.minSamples=1;tracer.fadeDuration=0;tracer.rasterizeScene=false;tracer.dynamicLowRes=false;tracer.renderToCanvas=false;tracer.renderScale=1;tracer.setScene(scene,camera);
 // Accumulation is a screen-space pass; depth must never reject its fragments.
 tracer._pathTracer.material.depthTest=false;tracer._pathTracer.material.depthWrite=false;
 for(const target of [tracer._pathTracer._primaryTarget,...tracer._pathTracer._blendTargets]){target.depthBuffer=false;target.dispose();}
 tracer.reset();
 while(tracer.samples<samples){if(signal?.aborted)throw new Error('Физический рендер отменён.');if((performance.now()-start)/1000>maxSeconds)throw new Error(`Физический рендер не завершился за ${maxSeconds} с. Уменьшите размер или число сэмплов.`);tracer.renderSample();if(shaderFailure)throw new Error('Физический шейдер не поддерживается GPU: '+shaderFailure.slice(0,500));if(renderer.getContext().isContextLost())throw new Error('GPU потерял контекст при физическом рендере.');onProgress(Math.min(.98,.05+.93*tracer.samples/samples),{phase:tracer.isCompiling?'Компиляция шейдера':'Трассировка света',samples:Math.floor(tracer.samples),total:samples,seconds:(performance.now()-start)/1000});await new Promise(r=>setTimeout(r,tracer.isCompiling?20:0));}
 const raw=targetStatistics(renderer,tracer.target),ctx=renderer.getContext();renderer.setRenderTarget(tracer.target);const gpu={error:ctx.getError(),framebuffer:ctx.checkFramebufferStatus(ctx.FRAMEBUFFER),floatColor:!!ctx.getExtension('EXT_color_buffer_float'),floatBlend:!!ctx.getExtension('EXT_float_blend'),calls:renderer.info.render.calls,programs:renderer.info.programs.length};renderer.setRenderTarget(null);room.lastPhysicalDiagnostic={raw,gpu,samples:tracer.samples};console.info('[physical-target]',JSON.stringify(room.lastPhysicalDiagnostic));
 if(!raw.finite||raw.max<=1e-6)throw new Error('Физический рендер вернул пустой буфер. PNG не сохранён. Диагностика: '+JSON.stringify(room.lastPhysicalDiagnostic));
 const mat=denoise?new DenoiseMaterial({map:tracer.target.texture,sigma:2,kSigma:1,threshold:.08}):new THREE.ShaderMaterial({uniforms:{map:{value:tracer.target.texture}},depthTest:false,depthWrite:false,vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position.xy,0.,1.);}',fragmentShader:'uniform sampler2D map;varying vec2 vUv;void main(){gl_FragColor=vec4(texture2D(map,vUv).rgb,1.);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}'});
 quad=new FullScreenQuad(mat);renderer.setRenderTarget(null);renderer.setViewport(0,0,width,height);renderer.setScissorTest(false);renderer.autoClear=true;renderer.setClearColor('#000000',1);renderer.clear();quad.render(renderer);
 const pixels=new Uint8Array(width*height*4),gl=renderer.getContext();gl.readPixels(0,0,width,height,gl.RGBA,gl.UNSIGNED_BYTE,pixels);let max=0,min=255,alpha=0;for(let i=0;i<pixels.length;i+=4){max=Math.max(max,pixels[i],pixels[i+1],pixels[i+2]);min=Math.min(min,pixels[i],pixels[i+1],pixels[i+2]);alpha+=pixels[i+3]}const output={min,max,meanAlpha:alpha/(width*height)};room.lastPhysicalDiagnostic.output=output;console.info('[physical-output]',JSON.stringify(output));if(max<3||max-min<2||output.meanAlpha<250)throw new Error('Физический рендер не сформировал корректное изображение. Пустой PNG не сохранён. '+JSON.stringify(output));
 const result=renderer.domElement.toDataURL('image/png');room.lastPhysicalRender={renderer:'three-gpu-pathtracer 0.0.23',samples:tracer.samples,bounces:6,width,height,denoise,seconds:(performance.now()-start)/1000,camera:room.capturePoint(),fov:camera.fov,output};onProgress(1,{phase:'Готово',...room.lastPhysicalRender});return result;
 }finally{quad?.material.dispose();owned?.dispose();env?.dispose();renderer?.dispose();renderer?.forceContextLoss();room.recording=false;room.controls.enabled=enabled;room.dirty=true;}
}
