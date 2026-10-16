// Placement rules shared by numeric edits, mounting, duplication and dragging.
// Coordinates follow Three.js Y rotation; position is the bottom centre.
const EPS=1e-7;
const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
function supportKind(o,catalog){return o.kind||catalog.find(c=>c.id===o.catalogId)?.kind}
function usableSupport(o,catalog){return o.mount==='floor'&&['cabinet','desk','diningTable','coffeeTable','custom'].includes(supportKind(o,catalog))}
function supportFit(o,parent){
 const angle=(o.rotation||0)-(parent.rotation||0),c=Math.abs(Math.cos(angle)),s=Math.abs(Math.sin(angle));
 return [parent.size[0]/2-(c*o.size[0]+s*o.size[2])/2,parent.size[2]/2-(s*o.size[0]+c*o.size[2])/2];
}
export function normalizePlacement(project,o,catalog=[]){
 if(!o.position?.every(Number.isFinite)||!o.size?.every(v=>Number.isFinite(v)&&v>0&&v<=30)||!Number.isFinite(o.rotation??0))throw new Error('Проверьте координаты, поворот и размеры предмета.');
 if(o.position.some(v=>Math.abs(v)>1000))throw new Error('Координаты должны быть в пределах ±1000 м.');
 const original=JSON.stringify([o.position,o.rotation,o.supportId,o.wallId]);
 if(o.mount==='floor'){o.position[1]=0;delete o.supportId;delete o.wallId;}
 else if(o.mount==='surface'){
  delete o.wallId;
  let parent=project.objects.find(p=>p.id===o.supportId&&p.id!==o.id);
  if(o.supportId&&!parent)throw new Error('Опора отсутствует. Выберите другую поверхность или размещение на полу.');
  if(!parent){
   const candidates=project.objects.filter(p=>p.id!==o.id&&usableSupport(p,catalog));
   candidates.sort((a,b)=>distance([o.position[0],o.position[2]],[a.position[0],a.position[2]])-distance([o.position[0],o.position[2]],[b.position[0],b.position[2]]));
   parent=candidates.find(p=>{const trial={...o,rotation:p.rotation||0};return supportFit(trial,p).every(v=>v>=-EPS)});
   if(parent)o.rotation=parent.rotation||0;
  }
  if(!parent||!usableSupport(parent,catalog))throw new Error('Нет подходящей опоры. Сначала добавьте тумбу или стол подходящего размера.');
  const [mx,mz]=supportFit(o,parent);
  if(mx<-EPS||mz<-EPS)throw new Error('Предмет не помещается целиком на опоре. Увеличьте опору или уменьшите предмет.');
  const r=parent.rotation||0,c=Math.cos(r),s=Math.sin(r),dx=o.position[0]-parent.position[0],dz=o.position[2]-parent.position[2];
  const x=clamp(dx*c-dz*s,-Math.max(0,mx),Math.max(0,mx)),z=clamp(dx*s+dz*c,-Math.max(0,mz),Math.max(0,mz));
  o.position=[parent.position[0]+x*c+z*s,parent.position[1]+parent.size[1],parent.position[2]-x*s+z*c];o.supportId=parent.id;
 }else if(o.mount==='wall'){
  delete o.supportId;
  let best;
  for(const w of project.walls){
   const dx=w.b[0]-w.a[0],dz=w.b[1]-w.a[1],length=Math.hypot(dx,dz);
   if(length+EPS<o.size[0]||w.height+EPS<o.size[1])continue;
   const ux=dx/length,uz=dz/length,along=clamp((o.position[0]-w.a[0])*ux+(o.position[2]-w.a[1])*uz,o.size[0]/2,length-o.size[0]/2);
   const px=w.a[0]+along*ux,pz=w.a[1]+along*uz,dist=Math.hypot(o.position[0]-px,o.position[2]-pz);
   if(!best||dist<best.dist)best={w,ux,uz,px,pz,dist};
  }
  if(!best)throw new Error('Нет стены, на которой предмет помещается по ширине и высоте.');
  const {w,ux,uz,px,pz}=best,side=(o.position[0]-px)*(-uz)+(o.position[2]-pz)*ux>=0?1:-1,offset=w.thickness/2+o.size[2]/2;
  o.position=[px-uz*offset*side,clamp(o.position[1],0,w.height-o.size[1]),pz+ux*offset*side];o.rotation=-Math.atan2(uz,ux)+(side<0?Math.PI:0);o.wallId=w.id;
 }else throw new Error('Неизвестный способ размещения.');
 return original!==JSON.stringify([o.position,o.rotation,o.supportId,o.wallId]);
}
export function normalizeEdits(project,before,ids,catalog=[],wallsChanged=false){
 const oldById=new Map(before.objects.map(o=>[o.id,o])),pending=new Set(ids),done=new Set();let adjusted=false;
 if(wallsChanged)for(const o of project.objects)if(o.mount==='wall')pending.add(o.id);
 function visit(id){
  if(done.has(id))return;
  const o=project.objects.find(o=>o.id===id);if(!o)return;
  done.add(id);adjusted=normalizePlacement(project,o,catalog)||adjusted;
  const old=oldById.get(id);
  for(const child of project.objects.filter(c=>c.supportId===id)){
   const oldChild=oldById.get(child.id);
   if(old&&oldChild){const r=(o.rotation||0)-(old.rotation||0),c=Math.cos(r),s=Math.sin(r),dx=oldChild.position[0]-old.position[0],dz=oldChild.position[2]-old.position[2];child.position=[o.position[0]+c*dx+s*dz,o.position[1]+o.size[1],o.position[2]-s*dx+c*dz];child.rotation=(oldChild.rotation||0)+r;}
   visit(child.id);
  }
 }
 for(const id of pending)visit(id);
 return adjusted;
}
export function resizeWall(project,wall,length){
 const prior=structuredClone(project.walls),old=[...wall.b],dx=wall.b[0]-wall.a[0],dz=wall.b[1]-wall.a[1],len=Math.hypot(dx,dz);
 if(len<EPS)throw new Error('Нельзя изменить длину стены с совпадающими концами.');
 const next=[wall.a[0]+dx*length/len,wall.a[1]+dz*length/len],delta=[next[0]-old[0],next[1]-old[1]];
 const move=p=>[p[0]+delta[0],p[1]+delta[1]];
 // Preserve small raster-recognition offsets. Only connect nonparallel endpoint
 // junctions; nearby parallel faces of a thick wall must remain separate.
 for(const w of project.walls){if(w.id===wall.id)continue;const wx=w.b[0]-w.a[0],wz=w.b[1]-w.a[1],wl=Math.hypot(wx,wz);const nonparallel=wl>EPS&&Math.abs((dx*wx+dz*wz)/(len*wl))<.3;const tolerance=Math.min(.16,(wall.thickness+w.thickness)/2+.015);for(const key of ['a','b'])if(distance(w[key],old)<.001||(nonparallel&&distance(w[key],old)<=tolerance))w[key]=move(w[key]);}
 for(const room of project.rooms){const polygon=room.polygon;room.polygon=polygon.map((v,i)=>{const close=distance(v,old),parallel=[polygon[(i+1)%polygon.length],polygon[(i+polygon.length-1)%polygon.length]].some(n=>{const vx=n[0]-v[0],vz=n[1]-v[1],vl=Math.hypot(vx,vz);return vl>EPS&&Math.abs((dx*vx+dz*vz)/(len*vl))>.98});return close<.001||(parallel&&close<=Math.min(.16,wall.thickness+.015))?move(v):v;});}
 wall.b=next;
 // A partition can end on the middle of an adjacent wall. Remember its old
 // segment parameter and carry that junction with the deformed segment.
 const anchors=[];
 for(const target of prior){if(target.id===wall.id)continue;const tx=target.b[0]-target.a[0],tz=target.b[1]-target.a[1],tl=Math.hypot(tx,tz);for(const key of ['a','b']){let best;for(const anchor of prior){if(anchor.id===target.id)continue;const ax=anchor.b[0]-anchor.a[0],az=anchor.b[1]-anchor.a[1],al=Math.hypot(ax,az);if(al<EPS||tl<EPS||Math.abs((tx*ax+tz*az)/(tl*al))>.3)continue;const p=target[key],t=((p[0]-anchor.a[0])*ax+(p[1]-anchor.a[1])*az)/(al*al),gap=Math.abs((p[0]-anchor.a[0])*az-(p[1]-anchor.a[1])*ax)/al;if(t<=.001||t>=.999||gap>Math.min(.08,(target.thickness+anchor.thickness)/2))continue;if(!best||gap<best.gap)best={target:target.id,key,anchor:anchor.id,t,gap,point:p};}if(best)anchors.push(best);}}
 for(let pass=0;pass<project.walls.length;pass++){let moved=false;for(const link of anchors){const anchor=project.walls.find(w=>w.id===link.anchor),original=prior.find(w=>w.id===link.anchor),target=project.walls.find(w=>w.id===link.target),t=link.t,p=[link.point[0]+(1-t)*(anchor.a[0]-original.a[0])+t*(anchor.b[0]-original.b[0]),link.point[1]+(1-t)*(anchor.a[1]-original.a[1])+t*(anchor.b[1]-original.b[1])];if(distance(target[link.key],p)>EPS){target[link.key]=p;moved=true;}}if(!moved)break;}
 // Room polygons may explicitly include those T-junction vertices too.
 for(const room of project.rooms)room.polygon=room.polygon.map(p=>{for(const original of prior){const current=project.walls.find(w=>w.id===original.id);for(const key of ['a','b'])if(distance(p,original[key])<.001&&distance(current[key],original[key])>EPS)return [...current[key]];}return p;});
 for(const opening of project.openings||[]){const w=project.walls.find(w=>w.id===opening.wallId),oldWall=prior.find(w=>w.id===opening.wallId);if(!w||!oldWall)continue;const vx=oldWall.b[0]-oldWall.a[0],vz=oldWall.b[1]-oldWall.a[1],den=vx*vx+vz*vz;if(den<EPS)continue;for(const key of ['a','b']){const p=opening[key];if(!p)continue;const t=((p[0]-oldWall.a[0])*vx+(p[1]-oldWall.a[1])*vz)/den;opening[key]=[p[0]+(1-t)*(w.a[0]-oldWall.a[0])+t*(w.b[0]-oldWall.b[0]),p[1]+(1-t)*(w.a[1]-oldWall.a[1])+t*(w.b[1]-oldWall.b[1])];}}
}
