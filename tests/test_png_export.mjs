import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import * as THREE from '../web/vendor/three/build/three.module.js';

// Exercise the production export method with real Three camera/geometry maths.
// The small renderer double records state; pixel appearance is checked in-browser.
const source=await readFile(new URL('../web/scene.js',import.meta.url),'utf8');
const method=source.slice(source.indexOf(' screenshot({'),source.indexOf(' capturePoint(){'));
assert.ok(method.startsWith(' screenshot({'));
const ExportScene=new Function('THREE',`return class {${method}}`)(THREE);
const make=(mode='3d',cutaway=true)=>{
 const scene=new ExportScene();Object.assign(scene,{mode,cutaway,dirty:false});
 scene.camera=new THREE.PerspectiveCamera(36,496/1009,.1,180);scene.camera.position.set(35,40,45);scene.camera.lookAt(5,0,3);
 scene.ortho=new THREE.OrthographicCamera(-7*496/1009,7*496/1009,7,-7,.1,180);scene.ortho.position.set(5,25,3.001);scene.ortho.lookAt(5,0,3);
 scene.camera.updateMatrixWorld();scene.ortho.updateMatrixWorld();scene.controls={enabled:true,target:new THREE.Vector3(5,0,3),enableDamping:true};
 scene.activeCamera=mode==='2d'?scene.ortho:scene.camera;
 for(const key of ['architecture','furniture','cloud','labels','dimensionGroup','boxGroup','research','cameras','selectionBox'])scene[key]=new THREE.Group();
 scene.architecture.add(new THREE.Mesh(new THREE.BoxGeometry(10,1.2,6),new THREE.MeshBasicMaterial()));scene.architecture.position.set(5,.6,3);scene.cloud.visible=false;scene.boxGroup.visible=false;
 const renderer={size:new THREE.Vector2(496,1009),ratio:1.5,viewport:new THREE.Vector4(0,0,496,1009),scissor:new THREE.Vector4(1,2,3,4),scissorTest:false,target:null,shadowMap:{needsUpdate:false},getSize(v){return v.copy(this.size)},getPixelRatio(){return this.ratio},getViewport(v){return v.copy(this.viewport)},getScissor(v){return v.copy(this.scissor)},getScissorTest(){return this.scissorTest},getRenderTarget(){return this.target},setPixelRatio(v){this.ratio=v},setSize(w,h,style){assert.equal(style,false);this.size.set(w,h)},setRenderTarget(v){this.target=v},setViewport(...v){v.length===1?this.viewport.copy(v[0]):this.viewport.set(...v)},setScissor(v){this.scissor.copy(v)},setScissorTest(v){this.scissorTest=v},domElement:{toDataURL(type){assert.equal(type,'image/png');if(scene.fail)throw Error('PNG encoder failure');return 'data:image/png;test'}}};
 scene.renderer=renderer;scene.composer={_width:496,_height:1009,_pixelRatio:1,setPixelRatio(v){this._pixelRatio=v},setSize(w,h){this._width=w;this._height=h}};scene.renderPass={camera:scene.camera};scene.ao={camera:scene.camera};
 scene.frames=[];scene.renderFrame=function(){this.activeCamera.updateMatrixWorld();this.frames.push({camera:this.activeCamera.clone(),width:renderer.size.x*renderer.ratio,height:renderer.size.y*renderer.ratio,labels:this.labels.visible,boxes:this.boxGroup.visible,composer:[this.composer._width,this.composer._height],shadow:renderer.shadowMap.needsUpdate})};
 return scene;
};
const state=s=>JSON.stringify({camera:s.camera.toJSON(),ortho:s.ortho.toJSON(),controls:s.controls,size:s.renderer.size,ratio:s.renderer.ratio,viewport:s.renderer.viewport,scissor:s.renderer.scissor,scissorTest:s.renderer.scissorTest,composer:[s.composer._width,s.composer._height,s.composer._pixelRatio],visible:[s.labels.visible,s.boxGroup.visible,s.cloud.visible],dirty:s.dirty});
for(const mode of ['3d','2d']){
 const scene=make(mode),before=state(scene),camera=scene.camera,active=scene.activeCamera;
 assert.equal(scene.screenshot(),'data:image/png;test');assert.equal(state(scene),before);assert.equal(scene.camera,camera);assert.equal(scene.activeCamera,active);
 const frame=scene.frames[0];assert.equal(frame.width,1600);assert.equal(frame.height,1000);assert.deepEqual(frame.composer,[1600,1000]);assert.equal(frame.labels,false);assert.equal(frame.shadow,true);assert.equal(scene.frames[1].labels,true);assert.equal(scene.frames[1].boxes,false);
 const bounds=new THREE.Box3().setFromObject(scene.architecture);let extent=0;
 for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const p=new THREE.Vector3(x,y,z).project(frame.camera);assert.ok(Math.abs(p.x)<.9&&Math.abs(p.y)<.9&&Math.abs(p.z)<1);extent=Math.max(extent,Math.abs(p.x),Math.abs(p.y));}
 assert.ok(extent>.85,'overview uses the export frame instead of portrait viewport padding');
 scene.fail=true;assert.throws(()=>scene.screenshot(),/PNG encoder failure/);assert.equal(state(scene),before);
}
const interior=make('3d',false),before=state(interior);interior.screenshot({width:1920,height:1080});assert.equal(state(interior),before);assert.equal(interior.frames[0].camera.aspect,1920/1080);assert.deepEqual(interior.frames[0].camera.position,interior.camera.position);assert.deepEqual(interior.frames[0].camera.quaternion.toArray(),interior.camera.quaternion.toArray());assert.equal(interior.frames[0].camera.fov,interior.camera.fov);
assert.throws(()=>interior.screenshot({width:0}),/PNG/);interior.recording=true;assert.throws(()=>interior.screenshot(),/прогулки/);
console.log('PNG export PASS: independent 1600x1000/default and 1920x1080/custom sizes, perspective/orthographic framing, interior pose, state restoration including encoder failure, immediate editor redraw.');
