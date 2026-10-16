// Actual Three.js primitives, GLTFLoader and production scene methods; no GPU/browser claim.
import fs from 'node:fs';
import vm from 'node:vm';
import {createHash} from 'node:crypto';
import * as THREE from '../web/vendor/three/build/three.module.js';
import {GLTFLoader} from '../web/vendor/three/examples/jsm/loaders/GLTFLoader.js';
const root=new URL('../',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
const results=[],check=(name,pass,evidence)=>results.push({name,status:pass?'PASS':'FAIL',evidence});
const ctx={THREE,GLTFLoader,Uint8Array,ArrayBuffer,structuredClone,atob,console,CustomEvent:class{constructor(type,options){this.type=type;this.detail=options.detail}}};
vm.createContext(ctx);
vm.runInContext(read('web/research.js').replace(/^import .*;\r?\n/gm,'').replace(/\bexport /g,'')+'\nglobalThis.build=buildResearchLayers;',ctx);
vm.runInContext(read('web/scene.js').replace(/^import .*;\r?\n/gm,'').replace('export class RoomScene','class RoomScene')+'\nglobalThis.RoomScene=RoomScene;',ctx);
const p=JSON.parse(read('artifacts/reviews/research-project.json')), research=ctx.build(p);
for(let i=0;i<p.researchLayers.length;i++){
 const layer=p.researchLayers[i],group=research.children[i],draw=group.children[0],a=Array.from(draw.geometry.attributes.position.array),expected=layer.positions.flat();
 check('Actual '+layer.kind+' geometry '+layer.id,(layer.kind==='points'?draw.isPoints:draw.isLineSegments)&&a.length===expected.length&&a.every((x,k)=>Math.abs(x-expected[k])<1e-6)&&JSON.stringify(Array.from(draw.geometry.index?.array||[]))===JSON.stringify(layer.segments?.flat()||[]),{type:draw.type,positions:a,index:Array.from(draw.geometry.index?.array||[]),visible:group.visible});
 check('Layer metadata copied '+layer.id,JSON.stringify(group.userData.provenance)===JSON.stringify(layer.provenance)&&JSON.stringify(group.userData.assetIds)===JSON.stringify(layer.assetIds),group.userData);
}
const room=Object.create(ctx.RoomScene.prototype);
Object.assign(room,{project:p,research,mode:'3d',showLabels:true,showDimensions:true,selected:null,renderer:{shadowMap:{}},el:{dispatchEvent:e=>events.push(e.detail)},cb:{onAssetError:m=>errors.push(m)},pendingAssets:new Set(),assetErrors:new Map()});
const errors=[],events=[];
for(const k of ['architecture','furniture','cloud','boxGroup','cameras','labels','dimensionGroup'])room[k]=new THREE.Group();
function effective(g){return g.visible&&(!g.parent||effective(g.parent))}
for(const mode of ['2d','3d']){
 room.mode=mode;p.layers={architecture:true,furniture:true,pointCloud:true,boxes:true,research:true,cameras:true};p.researchLayers[0].visible=false;p.researchLayers[1].visible=true;room.applyLayers();
 check(mode+' independent child visibility',!effective(research.children[0].children[0])&&effective(research.children[1].children[0])&&['architecture','furniture','cloud','boxGroup','cameras'].every(k=>room[k].visible),research.children.map(g=>({id:g.userData.researchLayerId,group:g.visible,primitive:g.children[0].visible})));
 p.layers.research=false;room.applyLayers();check(mode+' master switch preserves child settings and other groups',!effective(research.children[1].children[0])&&p.researchLayers[1].visible&&room.cameras.visible&&room.furniture.visible,{});
 p.layers.research=true;p.layers.cameras=false;room.applyLayers();check(mode+' camera helper independently hidden',effective(research.children[1].children[0])&&!room.cameras.visible,{});
}
const object=p.objects.find(o=>o.assetId),o=structuredClone(object);o.rotation=0;o.position=[0,0,0];o.size=[1,1,1];
async function load(obj){const g=new THREE.Group();g.position.fromArray(obj.position);g.userData.objectId=obj.id;g.add(new THREE.Mesh(new THREE.BoxGeometry(...obj.size),new THREE.MeshBasicMaterial()));room.furniture.add(g);const promise=room.loadAsset(obj,g);room.pendingAssets.add(promise);promise.finally(()=>room.pendingAssets.delete(promise));await room.awaitAssets();return g}
let g=await load(o);let b=new THREE.Box3().setFromObject(g);check('Actual asymmetric GLB reaches exact dimensions and floor',g.userData.assetState==='ready'&&b.min.y>-1e-6&&Math.abs(b.min.y)<1e-6&&b.getSize(new THREE.Vector3()).toArray().every(x=>Math.abs(x-1)<1e-6),{min:b.min.toArray(),max:b.max.toArray(),state:g.userData.assetState});
o.position[1]=.48;g=await load(o);b=new THREE.Box3().setFromObject(g);check('Actual GLB on support plane',Math.abs(b.min.y-.48)<1e-6,{min:b.min.toArray(),max:b.max.toArray()});
let release;const firstSet=new Set(),firstPromise=new Promise(r=>release=()=>{firstSet.delete(firstPromise);r()});firstSet.add(firstPromise);room.pendingAssets=firstSet;let screenshotCalls=0;room.screenshot=()=>{screenshotCalls++;return 'pixel-result'};const still=room.screenshotAsync();await Promise.resolve();check('Still waits for pending asset',screenshotCalls===0,{screenshotCalls});release();check('Still runs after asset readiness',await still==='pixel-result'&&screenshotCalls===1,{screenshotCalls});
room.pendingAssets=new Set();const asset=p.assets.find(a=>a.id===o.assetId),original=asset.data;asset.data=Buffer.from('invalid GLB').toString('base64');
let blocked=false;try{await load(o)}catch{blocked=true}check('Malformed GLB reports error and prevents readiness',blocked&&room.assetErrors.has(o.id)&&errors.length>0&&events.length>0,{blocked,errors,events});
let screenshotBlocked=false;try{await room.screenshotAsync()}catch{screenshotBlocked=true}check('Failed asset blocks beauty screenshot',screenshotBlocked&&screenshotCalls===1,{screenshotBlocked,screenshotCalls});asset.data=original;
const stale=new THREE.Group();room.furniture.add(stale);room.assetErrors.clear();const pending=room.loadAsset(o,stale);room.furniture=new THREE.Group();await pending;check('Stale parse does not attach to replacement scene',stale.children.length===0&&room.furniture.children.length===0,{staleChildren:stale.children.length});
// Simulate a project/rebuild switch while a still waits for the previous parse.
let releaseOld,releaseNew,newFinished=false,raceFinished=false;room.pendingAssets=new Set([new Promise(r=>releaseOld=r)]);const racingStill=room.screenshotAsync().then(x=>{raceFinished=true;return x});
const nextSet=new Set(),nextPromise=new Promise(r=>releaseNew=()=>{newFinished=true;nextSet.delete(nextPromise);r()});nextSet.add(nextPromise);room.pendingAssets=nextSet;room._assetGeneration=(room._assetGeneration||0)+1;releaseOld();
for(let i=0;i<20;i++)await Promise.resolve();const premature=raceFinished;releaseNew();await racingStill;
check('Still waits for current assets after pending set replacement',!premature&&newFinished,{premature,newFinished,screenshotCalls});await room.awaitAssets();
const oldName=asset.name,oldMime=asset.mime;asset.name='research.json';asset.mime='application/json';asset.data=Buffer.from('{}').toString('base64');let unsupportedBlocked=false,unsupportedGroup;
try{unsupportedGroup=await load(o)}catch{unsupportedBlocked=true}
check('Unsupported object asset is explicitly rejected',unsupportedBlocked,{unsupportedBlocked,state:unsupportedGroup?.userData.assetState,children:unsupportedGroup?.children.length});asset.name=oldName;asset.mime=oldMime;asset.data=original;
const integration=Object.create(ctx.RoomScene.prototype);Object.assign(integration,{project:{...structuredClone(p),rooms:[],walls:[],objects:[],openings:[],pointCloud:[],provenance:{},settings:{walkPath:[{position:[0,1,0],target:[1,1,1]}]}},renderer:{shadowMap:{}},sun:{position:new THREE.Vector3()},content:new THREE.Group(),mode:'3d',selected:null,showLabels:true,showDimensions:true,highlight(){}});integration.rebuild();
const primitiveTypes=[];integration.research.traverse(g=>{if(g.isPoints||g.isLineSegments)primitiveTypes.push(g.type)});check('Production rebuild integrates data and camera groups separately',primitiveTypes.includes('Points')&&primitiveTypes.includes('LineSegments')&&integration.cameras.children.some(x=>x.isCameraHelper||x.type==='CameraHelper')&&integration.research!==integration.cameras,{primitiveTypes,cameraTypes:integration.cameras.children.map(g=>g.type)});
const report={at:new Date().toISOString(),scope:'Production research/scene methods; actual Three primitives and actual GLTFLoader. No rasterization, DOM, browser uploads, texture loading or human recognizability proof.',sourceSHA256:Object.fromEntries(['web/research.js','web/scene.js','web/app.js','roomplan/research.py'].map(f=>[f,createHash('sha256').update(read(f)).digest('hex')])),results};
fs.writeFileSync(new URL('artifacts/reviews/research-geometry.json',root),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));process.exitCode=results.some(x=>x.status==='FAIL')?1:0;
