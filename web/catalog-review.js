import * as THREE from 'three';
import { makeFurniture } from './furniture.js';

const $ = selector => document.querySelector(selector);
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const params = new URLSearchParams(location.search);
let mode = ['iso','top','both'].includes(params.get('view')) ? params.get('view') : 'iso';
let page = Math.max(0, Number(params.get('page') || 1) - 1);
let catalog = [], categories = [], selected = params.get('category') || 'all';
let renderer, generation = 0;
const objects = new Map();
const thumbnails = new Map();
const gray = new THREE.MeshStandardMaterial({ color: '#b4b8ae', roughness: .78 });
const lightDirection = new THREE.Vector3(-3, 7, 5);

function createRenderer() {
  renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(720, 534);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  $('#renderer').append(renderer.domElement);
}

function getObject(entry) {
  if (!objects.has(entry.id)) {
    const object = makeFurniture({ ...entry, id: entry.id, catalogId: entry.id, position: [0,0,0], rotation: 0 }, catalog);
    object.updateMatrixWorld(true);
    const bounds = new THREE.Box3().setFromObject(object);
    objects.set(entry.id, { object, bounds });
  }
  return objects.get(entry.id);
}

function getFraming(entries, view) {
  // Use the same centred world origin and projected bounds for both variants.
  // Top-down models keep their actual horizontal position and dimensions.
  const combined = new THREE.Box3();
  entries.forEach(entry => combined.union(getObject(entry).bounds));
  const target = view === 'top' ? new THREE.Vector3(0,0,0) : new THREE.Vector3(0,combined.max.y * .43,0);
  const camera = new THREE.OrthographicCamera(-1,1,1,-1,.01,100);
  camera.position.copy(target).add(view === 'top' ? new THREE.Vector3(0,10,.001) : new THREE.Vector3(6,5,7));
  camera.lookAt(target);
  camera.updateMatrixWorld(true);
  let maxX = 0, maxY = 0;
  for (const x of [combined.min.x,combined.max.x]) for (const y of [combined.min.y,combined.max.y]) for (const z of [combined.min.z,combined.max.z]) {
    const point = new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse);
    maxX = Math.max(maxX, Math.abs(point.x)); maxY = Math.max(maxY, Math.abs(point.y));
  }
  const aspect = 720/534;
  const extent = Math.max(maxY, maxX/aspect, .32) * 1.23;
  camera.left = -extent*aspect; camera.right = extent*aspect;
  camera.top = extent; camera.bottom = -extent;
  camera.updateProjectionMatrix();
  return camera;
}

function renderThumbnail(entry, camera, view, scaleKey, monochrome) {
  const key = [entry.id,view,scaleKey,monochrome].join(':');
  if (thumbnails.has(key)) return thumbnails.get(key);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#f5f6f1');
  scene.add(new THREE.HemisphereLight('#fff9ec','#bdc7b9',1.8));
  const sun = new THREE.DirectionalLight('#fff6e5',3);
  sun.position.copy(lightDirection); sun.castShadow = true;
  sun.shadow.mapSize.set(1024,1024);
  Object.assign(sun.shadow.camera, { left:-3.5,right:3.5,top:3.5,bottom:-3.5,near:.1,far:20 });
  sun.shadow.normalBias = .015; sun.shadow.bias = -.0002; sun.shadow.radius = 3;
  scene.add(sun);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({ color:'#f5f6f1',roughness:.9 }));
  floor.rotation.x = -Math.PI/2; floor.position.y = -.014; floor.receiveShadow = true;
  scene.add(floor);
  const { object } = getObject(entry);
  const savedMaterials = [];
  if (monochrome) object.traverse(node => { if (node.isMesh) { savedMaterials.push([node,node.material]); node.material = gray; } });
  scene.add(object);
  renderer.render(scene,camera);
  const image = renderer.domElement.toDataURL('image/png');
  savedMaterials.forEach(([node,material]) => node.material = material);
  scene.remove(object);
  floor.geometry.dispose(); floor.material.dispose(); sun.shadow.dispose();
  thumbnails.set(key,image);
  return image;
}

async function renderPage() {
  const currentGeneration = ++generation;
  const single = selected !== 'all';
  const count = Math.ceil(categories.length/3);
  page = Math.max(0,Math.min(page,count-1));
  const visibleCategories = single ? [selected] : categories.slice(page*3,page*3+3);
  const monochrome = $('#monochrome').checked;
  const globalScale = $('#scale').value === 'global';
  $('#prev').disabled = single || page === 0;
  $('#next').disabled = single || page === count-1;
  $('#page-number').textContent = single ? 'Одна категория' : `Страница ${page+1} / ${count}`;
  $('#summary').textContent = `${visibleCategories.join(' · ')} — ${catalog.filter(entry => visibleCategories.includes(entry.category)).length} из ${catalog.length} моделей`;
  $('#sheet').className = `sheet ${single?'single':''} ${mode==='both'?'both':''}`;
  document.querySelectorAll('[data-mode]').forEach(button => button.classList.toggle('active',button.dataset.mode===mode));
  $('#sheet').replaceChildren();
  $('#busy').hidden = false;
  const query = new URLSearchParams({view:mode,page:String(page+1),category:selected});
  history.replaceState(null,'',`${location.pathname}?${query}`);
  for (const category of visibleCategories) {
    if (currentGeneration !== generation) return;
    const entries = catalog.filter(entry => entry.category===category);
    const section = document.createElement('section');
    section.className = 'category';
    section.innerHTML = `<h2>${escapeHtml(category)}<small>${entries.length} модели · одна камера</small></h2><div class="category-items"></div>`;
    $('#sheet').append(section);
    const views = mode === 'both' ? ['iso','top'] : [mode];
    const scaleEntries = globalScale ? catalog : entries;
    const cameras = Object.fromEntries(views.map(view => [view,getFraming(scaleEntries,view)]));
    for (const entry of entries) {
      const card = document.createElement('article');
      card.className = 'card';
      card.dataset.catalogId = entry.id;
      const pictures = views.map(view => {
        const src = renderThumbnail(entry,cameras[view],view,globalScale?'global':category,monochrome);
        return `<figure><img src="${src}" alt="${escapeHtml(entry.name)} — ${view==='top'?'вид сверху':'изометрия'}"><figcaption>${view==='top'?'2D · СВЕРХУ':'3D · ИЗОМЕТРИЯ'}</figcaption></figure>`;
      }).join('');
      card.innerHTML = `<div class="pictures">${pictures}</div><div class="card-info"><div><h3>${escapeHtml(entry.name)}</h3><code>${escapeHtml(entry.id)} · ${escapeHtml(entry.kind)}</code></div><div class="dims">${entry.size.map(value=>Math.round(value*100)).join(' × ')} см<br><span>${escapeHtml(entry.mount)}</span></div></div>`;
      section.querySelector('.category-items').append(card);
    }
    // Yield between category batches so UI remains responsive.
    await new Promise(resolve => requestAnimationFrame(resolve));
  }
  $('#busy').hidden = true;
  $('#manifest').textContent = `Производственный каталог: ${catalog.length} моделей, ${categories.length} категорий. Видимых WebGL-контекстов: 1. Режим: ${mode}; масштаб: ${globalScale?'общий':'внутри категории'}.`;
}

document.querySelectorAll('[data-mode]').forEach(button => button.onclick=()=>{mode=button.dataset.mode;renderPage()});
$('#category').onchange=event=>{selected=event.target.value;renderPage()};
$('#scale').onchange=renderPage;
$('#monochrome').onchange=renderPage;
$('#prev').onclick=()=>{page--;renderPage()};
$('#next').onclick=()=>{page++;renderPage()};

try {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error(`Каталог недоступен: HTTP ${response.status}`);
  catalog = await response.json();
  categories = [...new Set(catalog.map(entry=>entry.category))];
  if (!categories.includes(selected)) selected='all';
  $('#category').innerHTML += categories.map(category=>`<option value="${escapeHtml(category)}">${escapeHtml(category)}</option>`).join('');
  $('#category').value=selected;
  createRenderer();
  await renderPage();
} catch (error) {
  $('#sheet').innerHTML = `<div class="status error">${escapeHtml(error.message)}</div>`;
  $('#summary').textContent='Ошибка создания проверочной страницы';
  $('#busy').hidden=true;
  console.error(error);
}
