import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
const materials=new Map();
let weave,linen;
export function fabric(color){const key='fabric:'+color;if(materials.has(key))return materials.get(key);
 if(!weave){const cv=document.createElement('canvas');cv.width=cv.height=256;const ctx=cv.getContext('2d');const im=ctx.createImageData(256,256);let seed=29;for(let y=0;y<256;y++)for(let x=0;x<256;x++){seed=seed*16807%2147483647;const k=(y*256+x)*4,thread=((x%4<2)===(y%4<2)?6:-6),v=239+thread+(seed/2147483647-.5)*12;im.data[k]=im.data[k+1]=im.data[k+2]=v;im.data[k+3]=255}ctx.putImageData(im,0,0);weave=new THREE.CanvasTexture(cv);weave.wrapS=weave.wrapT=THREE.RepeatWrapping;weave.repeat.set(2,2);weave.anisotropy=8;linen=weave.clone();linen.colorSpace=THREE.SRGBColorSpace;linen.needsUpdate=true;}
 const mat=new THREE.MeshStandardMaterial({color,map:linen,roughness:.96,bumpMap:weave,bumpScale:.0025});materials.set(key,mat);return mat;
}
function leather(color){const key='leather:'+color;if(materials.has(key))return materials.get(key);fabric(color);const m=new THREE.MeshStandardMaterial({color,roughness:.53,bumpMap:weave,bumpScale:.001});materials.set(key,m);return m}
export function material(color,roughness=.75,metalness=0){const key=new THREE.Color(color).getHexString()+':'+roughness+':'+metalness;if(!materials.has(key))materials.set(key,new THREE.MeshStandardMaterial({color,roughness,metalness}));return materials.get(key)}
export function woodMaterial(color='#aa8059'){
 const key='wood:'+color;if(materials.has(key))return materials.get(key);
 const cv=document.createElement('canvas');cv.width=256;cv.height=512;const ctx=cv.getContext('2d');ctx.fillStyle=color;ctx.fillRect(0,0,256,512);let seed=51;const rnd=()=>((seed=seed*16807%2147483647)/2147483647);const hex=new THREE.Color(color).getHexString(),rgb=[0,2,4].map(i=>parseInt(hex.slice(i,i+2),16));
 for(let i=0;i<280;i++){const x=rnd()*256,f=.78+rnd()*.42;ctx.strokeStyle=`rgba(${rgb.map(v=>Math.min(255,Math.round(v*f))).join(',')},${.06+rnd()*.13})`;ctx.lineWidth=.25+rnd()*1.3;ctx.beginPath();ctx.moveTo(x,0);ctx.bezierCurveTo(x+8*Math.sin(i),170,x-6,300,x+3,512);ctx.stroke()}

 const tx=new THREE.CanvasTexture(cv);tx.colorSpace=THREE.SRGBColorSpace;tx.wrapS=tx.wrapT=THREE.RepeatWrapping;tx.anisotropy=4;const m=new THREE.MeshStandardMaterial({map:tx,roughness:.63,bumpMap:tx,bumpScale:.002});m.userData.grain=true;materials.set(key,m);return m;
}
const wood=woodMaterial('#ae845c'), dark=material('#40473d'), white=material('#f4f0e5'), metal=material('#59605a',.4,.65);
function box(g,w,h,d,x=0,y=0,z=0,mat=wood,r=0){const geo=new RoundedBoxGeometry(w,h,d,2,Math.min(w,h,d,.12)*.16);if(mat.userData.grain){const p=geo.attributes.position,n=geo.attributes.normal,uv=geo.attributes.uv;for(let i=0;i<p.count;i++){const nx=Math.abs(n.getX(i)),ny=Math.abs(n.getY(i)),nz=Math.abs(n.getZ(i));if(ny>nx&&ny>nz)uv.setXY(i,p.getZ(i)*2,p.getX(i)*.75);else if(nx>nz)uv.setXY(i,p.getZ(i)*2,p.getY(i)*.75);else uv.setXY(i,p.getX(i)*2,p.getY(i)*.75)}}const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.rotation.y=r;m.castShadow=true;m.receiveShadow=true;g.add(m);return m}
function round(g,r,h,x,y,z,mat=wood){const m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,h,36),mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;g.add(m);return m}
function sphere(g,x,y,z,sx,sy,sz,mat){const m=new THREE.Mesh(new THREE.SphereGeometry(1,20,14),mat);m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=true;g.add(m);return m}
function rod(g,a,b,r,mat=wood){const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b),v=vb.clone().sub(va);const m=new THREE.Mesh(new THREE.CylinderGeometry(r*.82,r,v.length(),12),mat);m.position.copy(va.add(vb).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());m.castShadow=true;m.receiveShadow=true;g.add(m);return m}
function cushion(g,w,h,d,x,y,z,mat){const m=new THREE.Mesh(new RoundedBoxGeometry(w,h,d,4,Math.min(w,h,d)*.35),mat);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;g.add(m);return m}
function piping(g,w,d,y,x,z,col){const pts=[];for(let i=0;i<=64;i++){const a=i/64*Math.PI*2;pts.push(new THREE.Vector3(x+Math.sign(Math.cos(a))*Math.pow(Math.abs(Math.cos(a)),.25)*w/2,y,z+Math.sign(Math.sin(a))*Math.pow(Math.abs(Math.sin(a)),.25)*d/2))}const m=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),64,.0023,4,false),col);g.add(m)}
function legs(g,w,d,h,mat=wood){for(const x of [-1,1])for(const z of [-1,1])box(g,.045,h,.045,x*w*.4,h/2,z*d*.38,mat)}
// Continuous shell: outside wall, lip, recessed inner wall and basin floor.
// Unlike an inset top panel, this leaves an actual visible cavity.
function basin(g,w,d,bottom,top,mat,{exponent=1,rim=.1,x=0,z=0}={}){
 const rings=[[.82,bottom],[1,top-.025],[1,top],[1-rim,top],[1-rim,top-.035],[.65,bottom+.065],[0,bottom+.065]],segments=64;
 const vertices=[],indices=[];
 for(const [radius,y] of rings)for(let i=0;i<segments;i++){const angle=i/segments*Math.PI*2,cs=Math.cos(angle),sn=Math.sin(angle);vertices.push(x+Math.sign(cs)*Math.pow(Math.abs(cs),exponent)*w*.5*radius,y,z+Math.sign(sn)*Math.pow(Math.abs(sn),exponent)*d*.5*radius)}
 for(let row=0;row<rings.length-1;row++)for(let i=0;i<segments;i++){const a=row*segments+i,b=row*segments+(i+1)%segments,c=a+segments,dd=b+segments;indices.push(a,c,b,b,c,dd)}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geometry.setIndex(indices);geometry.computeVertexNormals();
 const mesh=new THREE.Mesh(geometry,mat);mesh.castShadow=true;mesh.receiveShadow=true;g.add(mesh);return mesh;
}
function tubePath(g,points,radius,mat){const path=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),mesh=new THREE.Mesh(new THREE.TubeGeometry(path,32,radius,10,false),mat);mesh.castShadow=true;mesh.receiveShadow=true;g.add(mesh);return mesh}
export function makeFurniture(o,catalog=[]){const g=new THREE.Group();const def=catalog.find(c=>c.id===o.catalogId)||{};const kind=o.kind||def.kind||'custom';g.userData.objectId=o.id;const [w,h,d]=def.size||o.size;const soft=['sofa','armchair','bed','rug'].includes(kind);const c=kind==='armchair'?leather(o.color||def.color||'#b4b9a5'):soft?fabric(o.color||def.color||'#b4b9a5'):kind==='wardrobe'&&o.catalogId==='wardrobe-2'?material(o.color||'#666e70',.67):['coffeeTable','diningTable','desk','diningChair','cabinet','wardrobe'].includes(kind)?woodMaterial(o.color||def.color||'#b4b9a5'):material(o.color||def.color||'#b4b9a5');const light=soft?fabric(new THREE.Color(o.color||'#d8d5c5').lerp(new THREE.Color('white'),.17).getHexString().replace(/^/,'#')):material(new THREE.Color(o.color||'#d8d5c5').lerp(new THREE.Color('white'),.17));
 if(kind==='sofa'&&o.catalogId==='sofa-2'){
  // Asymmetric chaise module gives a genuinely different L-shaped plan.
  const shortDepth=d*.68,leftW=w*.65,rightW=w*.35;
  for(const [x,z] of [[-w*.42,-d*.36],[-w*.42,d*.1],[w*.41,-d*.36],[w*.41,d*.4]])round(g,.028,.14,x,.07,z,dark);
  cushion(g,leftW,.22,shortDepth,-rightW/2,.25,-d*.16,c);cushion(g,rightW,.22,d,leftW/2,.25,0,c);
  cushion(g,w-.06,.42,.16,0,h-.22,-d/2+.09,c);
  cushion(g,.17,.5,shortDepth,-w/2+.085,.4,-d*.16,c);cushion(g,.17,.5,d,w/2-.085,.4,0,c);
  for(let i=0;i<2;i++){const x=-w/2+.18+(i+.5)*(leftW-.18)/2;cushion(g,(leftW-.2)/2-.02,.15,shortDepth-.2,x,.43,-d*.1,light);const back=cushion(g,(leftW-.2)/2-.015,.31,.16,x,.64,-d*.3,light);back.rotation.x=-.1;}
  cushion(g,rightW-.19,.15,d-.21,leftW/2-.03,.43,.055,light);const back=cushion(g,rightW-.2,.31,.16,leftW/2-.03,.64,-d*.3,light);back.rotation.x=-.1;
  const bolster=round(g,.095,rightW-.25,leftW/2-.03,.56,-d*.17,fabric('#8b9b84'));bolster.rotation.z=Math.PI/2;
 }
 else if(kind==='armchair'&&o.catalogId==='armchair-2'){
  // Open timber lounge frame, reclined back, floating upholstered seat.
  for(const x of [-1,1]){rod(g,[x*w*.42,.025,d*.4],[x*w*.35,.56,-d*.27],.025,wood);rod(g,[x*w*.4,.025,-d*.39],[x*w*.35,.55,d*.25],.025,wood);rod(g,[x*w*.4,.53,d*.33],[x*w*.4,.57,-d*.35],.035,wood);rod(g,[x*w*.35,.32,-d*.28],[x*w*.35,h-.045,-d*.41],.027,wood)}
  const seat=cushion(g,w*.73,.14,d*.68,0,.34,d*.04,c);seat.rotation.x=.06;
  const back=cushion(g,w*.73,h*.47,.13,0,h*.69,-d*.32,c);back.rotation.x=-.22;
  rod(g,[-w*.36,.28,d*.22],[w*.36,.28,d*.22],.024,wood);
 }
 else if(kind==='sofa'||kind==='armchair') {
  legs(g,w,d,.16,dark);cushion(g,w,.23,d,0,.25,0,c);cushion(g,w-.06,.46,.18,0,h-.25,-d/2+.11,c);
  for(const x of [-1,1])cushion(g,.18,h-.15,d-.02,x*(w/2-.09),h/2+.04,0,c);
  const n=kind==='sofa'?3:1,cw=(w-.39)/n;
  for(let i=0;i<n;i++){const x=-(w-.39)/2+(i+.5)*cw;cushion(g,cw-.018,.17,d-.3,x,.43,.065,light);piping(g,cw-.03,d-.32,.46,x,.065,c);const b=cushion(g,cw-.025,.35,.18,x,.67,-d*.27,light);b.rotation.x=-.16;}
  if(w>1.2){const p=cushion(g,.36,.34,.15,-w*.32,.67,.035,fabric('#a16d48'));p.rotation.z=.18;p.rotation.x=-.15;const p2=cushion(g,.34,.35,.15,w*.32,.67,.035,fabric('#566b60'));p2.rotation.z=-.23;p2.rotation.x=-.1;const tg=new THREE.PlaneGeometry(.43,.7,16,24),tp=tg.attributes.position;for(let j=0;j<tp.count;j++){const u=tp.getX(j),q=(tp.getY(j)+.35)/.7;tp.setXYZ(j,u+w*.22,.55-Math.max(q-.65,0)*.75+Math.sin(q*35+u*25)*.006,-.02+Math.min(q,.65)*.7)}tg.computeVertexNormals();const tm=fabric('#b3b6aa').clone();tm.side=THREE.DoubleSide;const throwMesh=new THREE.Mesh(tg,tm);throwMesh.castShadow=true;throwMesh.receiveShadow=true;g.add(throwMesh);}
 }
 else if(kind==='bed'&&o.catalogId==='bed-2'){
  // Low open timber platform with a slatted headboard and two cylindrical bolsters.
  legs(g,w,d,.16,wood);box(g,w,.12,d,0,.19,0,wood);
  for(let i=0;i<9;i++)box(g,w*.075,h-.12,.07,-w*.43+i*w*.1075,h/2+.055,-d/2+.045,wood);
  box(g,w,.045,.08,0,h-.022,-d/2+.045,wood);
  cushion(g,w-.1,.18,d-.13,0,.33,.025,fabric('#e4e0d5'));
  cushion(g,w-.12,.045,d*.57,0,.44,d*.19,c);
  box(g,w-.13,.024,d*.18,0,.474,d*.3,fabric('#8d7661'));
  for(const x of [-1,1]){const bolster=round(g,.1,w*.39,x*w*.235,.45,-d*.31,fabric('#faf4e7'));bolster.rotation.z=Math.PI/2}
 }
 else if(kind==='bed'){legs(g,w,d,.15);box(g,w,.23,d,0,.22,0,wood);box(g,w+.05,h,.12,0,h/2,-d/2,material('#bdad92'));cushion(g,w-.06,.24,d-.08,0,.43,0,fabric('#ede8dc'));box(g,w-.08,.07,d*.64,0,.57,d*.15,c);box(g,w-.07,.035,d*.15,0,.62,d*.29,material('#ded4bd'));for(const x of [-1,1])cushion(g,w*.4,.14,.45,x*w*.24,.61,-d*.32,fabric('#faf7ed'));for(let i=0;i<7;i++)box(g,.012,.012,d*.6,-w*.42+i*w*.14,.612,d*.15,light)}
 else if(['coffeeTable','diningTable','desk'].includes(kind)){legs(g,w,d,h-.06,kind==='coffeeTable'?dark:wood);box(g,w,.07,d,0,h-.035,0,c);if(kind==='coffeeTable'){
 round(g,.12,.018,w*.22,h+.012,0,material('#cac0a9'));round(g,.07,.022,w*.22,h+.03,0,white);
 const vase=new THREE.Mesh(new THREE.LatheGeometry([[0,0],[.075,0],[.09,.025],[.085,.12],[.045,.19],[.035,.25],[.042,.26]].map(([x,y])=>new THREE.Vector2(x,y)),32),material('#8c998d',.32));vase.position.set(-w*.23,h,-d*.12);vase.castShadow=true;vase.receiveShadow=true;g.add(vase);
 for(let i=0;i<3;i++){const tip=[-w*.23+(i-1)*.055,h+.39+i*.035,-d*.12+(i%2)*.04];rod(g,[-w*.23,h+.2,-d*.12],tip,.002,material('#606d46'));const leaf=sphere(g,tip[0]+.015,tip[1]-.035,tip[2],.045,.012,.019,material('#697c58'));leaf.rotation.z=.5+i*.3;}
 box(g,.3,.028,.21,w*.08,h+.018,d*.22,material('#eee7d9'));box(g,.31,.007,.22,w*.08,h+.036,d*.22,material('#60796e'));box(g,.26,.016,.19,w*.05,h+.05,d*.2,material('#b79570'),.12);
 }if(kind==='desk'){box(g,.45,.025,.3,0,h+.02,-d*.15,dark);box(g,.4,.27,.025,0,h+.16,-d*.2,material('#728b8c'))}if(kind==='diningTable'){for(const x of [-1,1])for(const z of [-1,1]){round(g,.13,.012,x*w*.28,h+.045,z*d*.26,white);round(g,.055,.012,x*w*.28,h+.054,z*d*.26,material('#d1cebd'))}plant(g,.15,h+.05,0,0,.18)}}
 else if(kind==='officeChair'){
  const meshBack=o.catalogId==='officeChair-2',seatY=h*.44,backW=w*.69,backHeight=h*(meshBack?.43:.39);
  // Five-star swivel base and paired caster wheels, shared task-chair semantics.
  round(g,.035,seatY-.11,0,(seatY+.11)/2,0,metal);round(g,.065,.1,0,.13,0,dark);
  for(let i=0;i<5;i++){const a=i*Math.PI*2/5,r=Math.min(w,d)*.42,x=Math.cos(a)*r,z=Math.sin(a)*r;rod(g,[0,.14,0],[x,.075,z],.026,meshBack?metal:dark);for(const side of [-1,1]){const wheel=round(g,.035,.024,x+Math.cos(a)*side*.019,.037,z+Math.sin(a)*side*.019,dark);wheel.rotation.z=Math.PI/2;wheel.rotation.y=-a;}}
  cushion(g,w*.79,.09,d*.73,0,seatY,d*.04,meshBack?fabric(o.color):leather(o.color));
  rod(g,[0,seatY-.03,-d*.22],[0,h*.75,-d*.34],.032,dark);
  for(const x of [-1,1]){rod(g,[x*w*.34,seatY-.025,0],[x*w*.4,seatY+.18,0],.018,dark);cushion(g,w*.12,.045,d*.43,x*w*.4,seatY+.19,d*.04,dark)}
  if(meshBack){
   const y0=seatY+.08,y1=Math.min(h-.12,y0+backHeight),z=-d*.32;
   tubePath(g,[[-backW/2,y0,z],[-backW*.54,(y0+y1)/2,z-.025],[-backW*.43,y1,z-.02],[0,y1+.025,z-.02],[backW*.43,y1,z-.02],[backW*.54,(y0+y1)/2,z-.025],[backW/2,y0,z]],.022,dark);
   for(let i=1;i<15;i++){const yy=y0+(y1-y0)*i/15;rod(g,[-backW*.47,yy,z],[backW*.47,yy,z],.0035,material('#7d8a80',.95))}
   for(let i=1;i<12;i++){const xx=-backW*.48+backW*.96*i/12;rod(g,[xx,y0,z],[xx,y1,z],.0025,material('#829088',.95))}
   cushion(g,backW*.6,.085,.065,0,h-.05,z-.005,dark);
  }else{const back=cushion(g,backW,backHeight,.105,0,seatY+.1+backHeight/2,-d*.3,leather(o.color));back.rotation.x=-.1;for(const y of [seatY+.19,seatY+.33])box(g,backW*.8,.008,.009,0,y,-d*.239,light)}
 }
 else if(kind==='diningChair'&&o.catalogId==='diningChair-2'){
  // Closed upholstered shell contrasts with the open wishbone reference.
  for(const x of [-1,1])for(const z of [-1,1])rod(g,[x*w*.43,.02,z*d*.4],[x*w*.3,h*.48,z*d*.27],.013,metal);
  cushion(g,w*.95,.075,d*.88,0,h*.49,d*.015,c);
  const back=cushion(g,w*.9,h*.43,.09,0,h*.77,-d*.35,c);back.rotation.x=-.12;
  box(g,w*.75,.012,.012,0,h*.63,-d*.29,light);
 }
 else if(kind==='diningChair'){
 for(const x of [-1,1])for(const z of [-1,1])rod(g,[x*w*.45,.02,z*d*.42],[x*w*.35,h*.5,z*d*.32],.022,c);
 cushion(g,w,.065,d*.91,0,h*.49,0,fabric('#b4aa91'));
 for(const x of [-1,1])rod(g,[x*w*.36,h*.48,-d*.34],[x*w*.43,h*.92,-d*.43],.018,c);
 const path=new THREE.CatmullRomCurve3([new THREE.Vector3(-w*.46,h*.9,-d*.28),new THREE.Vector3(-w*.3,h*.95,-d*.48),new THREE.Vector3(0,h*.96,-d*.52),new THREE.Vector3(w*.3,h*.95,-d*.48),new THREE.Vector3(w*.46,h*.9,-d*.28)]);const rail=new THREE.Mesh(new THREE.TubeGeometry(path,24,.035,10,false),c);rail.castShadow=true;g.add(rail);rod(g,[0,h*.53,-d*.4],[-w*.26,h*.92,-d*.48],.011,c);rod(g,[0,h*.53,-d*.4],[w*.26,h*.92,-d*.48],.011,c);
 }
 else if(['wardrobe','cabinet'].includes(kind)){box(g,w,h-.08,d,0,h/2+.04,0,c);legs(g,w,d,.1,dark);const n=Math.max(2,Math.round(w/.5));for(let i=0;i<n;i++){box(g,w/n-.012,h-.15,.025,-w/2+(i+.5)*w/n,h/2+.04,d/2+.013,light);box(g,.018,.12,.03,-w/2+(i+.85)*w/n,h*.58,d/2+.04,metal)}if(kind==='cabinet'){box(g,w+.02,.035,d+.02,0,h,0,wood);plant(g,.12,h+.02,-w*.35,0,.18);box(g,.23,.025,.19,w*.3,h+.035,0,material('#aca083'))}}
 else if(kind==='fridge'){box(g,w,h,d,0,h/2,0,c);box(g,w-.025,.012,.025,0,h*.34,d*.51,dark);for(const y of [.52,.8])box(g,.025,h*.17,.035,w*.36,h*y,d*.53,metal)}
 else if(kind==='stove'){box(g,w,h-.04,d,0,h/2,0,c);box(g,w,.045,d,0,h,0,dark);box(g,w*.77,h*.52,.02,0,h*.42,d/2+.01,material('#303a38'));for(const x of [-1,1])for(const z of [-1,1])round(g,.09,.015,x*w*.25,h+.028,z*d*.25,metal);box(g,w*.7,.02,.055,0,h*.77,d/2+.03,metal)}
 else if(kind==='sink'){
  const bath=o.catalogId==='sink-2',ceramic=material('#f1f1e9',.24),bowlMat=bath?ceramic:material('#a5afac',.26,.65);
  if(bath){
   // Wall vanity with a separate oval vessel; open niche below the bowl.
   box(g,w,.1,d,0,h*.39,0,wood);for(const x of [-1,1])box(g,.035,h*.38,d,x*(w/2-.018),h*.23,0,wood);
   box(g,w,.04,d,0,h*.69,0,wood);basin(g,w*.85,d*.85,h*.7,h,bowlMat,{exponent:1,rim:.12,z:.02});
   for(let i=0;i<3;i++)box(g,w*.23,.04,d*.45,-w*.29+i*w*.29,h*.48,.04,fabric('#dedbd0'));
  }else{
   // The cabinet has side/front panels, leaving the countertop recess open.
   box(g,w,h-.24,d,0,(h-.24)/2,0,c);for(const x of [-1,1])box(g,.035,.24,d,x*(w/2-.018),h-.12,0,c);
   box(g,w,.24,.035,0,h-.12,d/2-.018,c);box(g,w,.24,.035,0,h-.12,-d/2+.018,c);
   const bw=w*.59,bd=d*.69,bx=-w*.13;
   box(g,w,.035,(d-bd)/2,0,h-.015,-d/2+(d-bd)/4,white);box(g,w,.035,(d-bd)/2,0,h-.015,d/2-(d-bd)/4,white);
   const left=bx-bw/2,right=bx+bw/2;box(g,left+w/2,.035,bd,(-w/2+left)/2,h-.015,0,white);box(g,w/2-right,.035,bd,(right+w/2)/2,h-.015,0,white);
   basin(g,bw,bd,h-.22,h,bowlMat,{exponent:.36,rim:.1,x:bx});
   for(let i=0;i<6;i++)box(g,.012,.006,bd*.75,w*.27+i*w*.029,h+.007,0,metal);
   box(g,w*.72,.014,.024,0,h*.63,d/2+.005,metal);
  }
  round(g,.023,.005,bath?0:-w*.13,bath?h*.7+.07:h-.15,bath?.02:0,metal);
  tubePath(g,[[0,h-.01,-d*.34],[0,h+.16,-d*.34],[0,h+.2,-d*.22],[0,h+.16,-d*.1]],.015,metal);
 }
 else if(kind==='toilet'){
  const hung=o.catalogId==='toilet-2',ceramic=material('#f4f4ee',.2);
  if(hung){
   // Wall-hung square-front pan, no exposed cistern and clear floor gap.
   box(g,w*.72,h*.32,d*.2,0,h*.48,-d*.34,ceramic);
   basin(g,w*.98,d*.8,h*.25,h*.63,ceramic,{exponent:.48,rim:.19,z:d*.04});
   box(g,w*.97,.04,d*.65,0,h*.66,d*.065,ceramic);
   box(g,w*.53,h*.2,.035,0,h*.87,-d*.45,material('#d8ded7',.3));
   for(const x of [-1,1]){const button=round(g,w*.065,.006,x*w*.1,h*.87,-d*.427,metal);button.rotation.x=Math.PI/2;}
  }else{
   sphere(g,0,h*.25,d*.08,w*.32,h*.25,d*.28,ceramic);
   box(g,w*.86,h*.52,d*.23,0,h*.74,-d*.35,ceramic);
   basin(g,w*.98,d*.75,h*.32,h*.61,ceramic,{exponent:1,rim:.22,z:d*.08});
   const seat=new THREE.Mesh(new THREE.TorusGeometry(.46,.035,10,64),ceramic);seat.rotation.x=Math.PI/2;seat.scale.set(w,d*.76,.5);seat.position.set(0,h*.64,d*.08);seat.castShadow=true;seat.receiveShadow=true;g.add(seat);
   round(g,.025,.008,0,h+.004,-d*.35,metal);
  }
 }
 else if(kind==='bathtub'){
  const oval=o.catalogId==='bathtub-1',ceramic=material('#f1f3ed',.22);
  basin(g,w,d,.025,h,ceramic,{exponent:oval?1:.25,rim:oval?.12:.2});
  if(!oval){for(const x of [-1,1])box(g,.025,h*.86,d*.97,x*(w/2-.013),h*.45,0,ceramic);for(const z of [-1,1])box(g,w*.97,h*.86,.025,0,h*.45,z*(d/2-.013),ceramic);box(g,w*.6,.025,d*.12,0,h*.91,-d*.36,material('#687c77'))}
  round(g,.025,.008,0,.096,-d*.22,metal);
  tubePath(g,[[w*.33,h-.04,-d*.33],[w*.33,h+.12,-d*.33],[w*.2,h+.15,-d*.33],[w*.1,h+.13,-d*.33]],.014,metal);
 }
 else if(kind==='tv'){box(g,w,.045,d,0,.025,0,dark);round(g,.035,h*.23,0,h*.12,0,dark);box(g,w,h*.75,.045,0,h*.61,0,dark);box(g,w-.04,h*.75-.04,.008,0,h*.61,.025,material('#334747',.16,.1));box(g,w*.65,.008,.009,-w*.12,h*.37,.03,material('#476365'))}
 else if(kind==='plant')plant(g,w*.34,0,0,0,h);
 else if(kind==='rug'){box(g,w,.015,d,0,.009,0,c);for(const x of [-1,1])box(g,.025,.003,d-.08,x*(w/2-.06),.018,0,light);for(const z of [-1,1])box(g,w-.1,.003,.025,0,.018,z*(d/2-.06),light)}
 else{box(g,w,h,d,0,h/2,0,c);box(g,w*.8,.003,d*.8,0,h+.004,0,material('#d8ddcf'))}
 if(def.size)g.scale.set(o.size[0]/def.size[0],o.size[1]/def.size[1],o.size[2]/def.size[2]);g.position.fromArray(o.position);g.rotation.y=o.rotation||0;return g;
}
function plant(g,r,base,x,z,h){
 const ph=h*.24,pot=new THREE.Mesh(new THREE.CylinderGeometry(r*.8,r*.58,ph,32),material('#c5b39a',.85));pot.position.set(x,base+ph/2,z);pot.castShadow=true;pot.receiveShadow=true;g.add(pot);round(g,r*.72,.012,x,base+ph,z,material('#3a3026'));
 const colors=['#365b3b','#4b754a','#638352'];
 for(let i=0;i<19;i++){const a=i*2.399,yy=base+h*(.38+i*.029),reach=r*(.55+(i%3)*.23),tx=x+Math.cos(a)*reach,tz=z+Math.sin(a)*reach;rod(g,[x,base+ph,z],[tx,yy,tz],Math.max(.002,h*.003),material('#6f7241'));const geo=new THREE.PlaneGeometry(1,1,6,10),pos=geo.attributes.position;
  for(let k=0;k<pos.count;k++){const u=pos.getX(k)*2,v=pos.getY(k)+.5;const width=Math.pow(Math.sin(v*Math.PI),.7);pos.setXYZ(k,u*width*r*.5,Math.sin(v*Math.PI)*r*.13- Math.abs(u)*r*.09,v*h*.21)}geo.computeVertexNormals();const m=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({color:colors[i%3],side:THREE.DoubleSide,roughness:.62}));m.position.set(tx,yy,tz);m.rotation.y=-a+Math.PI/2;m.rotation.x=(i%3-.8)*.3;m.castShadow=true;m.receiveShadow=true;g.add(m);
 }
}
export function previewSVG(kind,color='#b2b99f'){let shapes='';const stroke='#6d7962';const poly=(p,c)=>`<polygon points="${p}" fill="${c}" stroke="${stroke}" stroke-width=".7"/>`;const block=(x,y,w,h,d,c)=>poly(`${x},${y} ${x+w},${y-8} ${x+w+d},${y-2} ${x+d},${y+7}`,c)+poly(`${x},${y} ${x+d},${y+7} ${x+d},${y+7+h} ${x},${y+h}`,c)+poly(`${x+d},${y+7} ${x+w+d},${y-2} ${x+w+d},${y-2+h} ${x+d},${y+7+h}`,c);if(['sofa','armchair'].includes(kind)){shapes=block(14,35,54,12,17,color)+block(14,24,54,18,7,color)+block(12,30,7,20,17,color)+block(64,22,7,20,17,color);shapes+=`<path d="M40 38v12M58 35v12" stroke="#89937a"/>`}else if(kind==='bed'){shapes=block(21,28,40,7,26,'#e9e2ce')+block(20,20,40,15,5,color)+block(25,42,38,6,22,color)}else if(kind==='plant'){shapes='<path d="M42 48h25l-4 17H47z" fill="#c6b293"/><path d="M55 48V17" stroke="#758866" stroke-width="2"/><ellipse cx="44" cy="30" rx="8" ry="16" transform="rotate(-40 44 30)" fill="#77926e"/><ellipse cx="64" cy="23" rx="7" ry="16" transform="rotate(32 64 23)" fill="#8ea280"/>'}else if(['coffeeTable','diningTable','desk'].includes(kind)){shapes='<path d="M22 42v18m57-25v20M40 48v17" stroke="#85745c" stroke-width="3"/>'+block(15,33,54,4,20,color)}else if(['diningChair','officeChair'].includes(kind)){shapes='<path d="M35 43v20m26-27v19M48 49v17" stroke="#85745c" stroke-width="2"/>'+block(30,33,24,4,14,color)+block(30,18,24,20,4,color)}else if(kind==='tv'){shapes=block(25,17,50,31,4,'#3e5050')+'<path d="M55 47v9l-16 3h30" fill="none" stroke="#56685a" stroke-width="3"/>'}else if(kind==='rug'){shapes=block(12,39,55,1,25,color)}else{shapes=block(25,22,38,kind==='wardrobe'||kind==='fridge'?39:25,18,color)}return `<svg viewBox="0 0 110 80" aria-hidden="true"><ellipse cx="56" cy="65" rx="35" ry="5" fill="#c2c6b7" opacity=".18"/>${shapes}</svg>`}
