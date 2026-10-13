#!/usr/bin/env node
/**
 * Rebuild the original earth-embedding brand artwork with Excalidraw itself.
 *
 * npm install --prefix work/brand --save-exact @excalidraw/excalidraw@0.18.0 \
 *   react@19.2.0 react-dom@19.2.0 vite@7.1.12 playwright@1.56.1
 * node scripts/render_brand.mjs
 *
 * Uses a temporary, loopback-only Vite server and headless Chromium. Set
 * BRAND_CHROMIUM_EXECUTABLE for a system browser, or install Playwright Chromium.
 * Artwork contains editable native Excalidraw elements, never a raster backdrop.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const workspace = path.join(root, 'work', 'brand');
const output = path.join(root, 'docs', 'assets');
const require = createRequire(path.join(workspace, 'package.json'));
const { chromium } = require('playwright');
const { createServer } = await import(pathToFileURL(require.resolve('vite')).href);

const C = {
  paper: '#faf8f1', ink: '#173f40', teal: '#267b72', mint: '#d8ece0',
  soft: '#edf3eb', orange: '#d98950', peach: '#f4e3d2', grey: '#57706b',
  lavender: '#e9e6f2', purple: '#6b6487', white: '#fffef9', grid: '#dce5d9',
};
let serial = 0;
const elements = [];
const push = (type, x, y, width, height, extra = {}) => {
  const element = { id: `earth-brand-${++serial}`, type, x, y, width, height,
    strokeColor: C.ink, backgroundColor: 'transparent', fillStyle: 'solid',
    strokeWidth: 1.8, strokeStyle: 'solid', roughness: 1.1, opacity: 100,
    seed: 4096 + serial * 173, ...extra };
  elements.push(element);
  return element;
};
const box = (x, y, w, h, extra) => push('rectangle', x, y, w, h, { roundness: { type: 3 }, ...extra });
const ellipse = (x, y, w, h, extra) => push('ellipse', x, y, w, h, extra);
const line = (x, y, points, extra = {}) => push('line', x, y,
  Math.max(...points.map(p => p[0])) - Math.min(...points.map(p => p[0])),
  Math.max(...points.map(p => p[1])) - Math.min(...points.map(p => p[1])),
  { points, ...extra });
const arrow = (x, y, points, extra = {}) => {
  const result = line(x, y, points, { strokeColor: C.teal, strokeWidth: 2.3,
    endArrowhead: 'arrow', ...extra });
  result.type = 'arrow';
  return result;
};
const text = (x, y, value, size = 24, extra = {}) => push('text', x, y, 1, 1, {
  text: value, fontSize: size, fontFamily: 2, textAlign: 'left', verticalAlign: 'top',
  lineHeight: 1.25, roughness: 0, strokeWidth: 1, ...extra,
});
const hand = (x, y, value, size = 26, extra = {}) => text(x, y, value, size, { fontFamily: 5, ...extra });
const poly = (x, y, points, color = C.teal, extra = {}) => line(x, y, [...points, points[0]], {
  backgroundColor: color, strokeColor: color, strokeWidth: 1, roughness: 1.1, ...extra,
});
const dot = (x, y, r, fill, extra = {}) => ellipse(x-r, y-r, r*2, r*2,
  { strokeColor: C.ink, backgroundColor: fill, strokeWidth: 1.4, ...extra });

/** Original orbital Earth mark: globe + geographic contours + feature-vector nodes. */
function globe(x, y, scale = 1, monochrome = false) {
  const saved = elements.length;
  const tint = monochrome ? C.white : C.mint;
  const accent = monochrome ? C.ink : C.orange;
  ellipse(9, 70, 203, 59, { angle: -0.43, strokeColor: C.teal, strokeWidth: 2.5 });
  ellipse(45, 26, 135, 135, { backgroundColor: tint, strokeWidth: 2.4 });
  ellipse(84, 28, 57, 131, { strokeColor: C.teal, opacity: 55, strokeWidth: 1.4 });
  line(50, 71, [[0,0],[25,8],[63,13],[102,6],[125,-1]], { strokeColor: C.teal, opacity: 42, strokeWidth: 1.3 });
  line(49, 116, [[0,0],[29,-7],[65,-9],[101,-5],[124,0]], { strokeColor: C.teal, opacity: 42, strokeWidth: 1.3 });
  poly(70, 48, [[0,5],[14,-2],[27,0],[33,9],[25,20],[27,28],[15,32],[8,26],[-2,27],[-6,17]], C.teal, { opacity: 88 });
  poly(90, 90, [[0,0],[17,0],[26,12],[19,27],[12,36],[5,28],[1,14]], C.teal, { opacity: 88 });
  poly(137, 63, [[0,1],[17,-4],[28,5],[27,18],[16,25],[6,17],[-4,11]], C.teal, { opacity: 88 });
  line(17, 129, [[0,0],[24,11],[57,4],[87,-8],[124,-27],[157,-51],[185,-76]], {
    strokeColor: C.ink, strokeWidth: 2.7, roughness: 1.1,
  });
  line(166, 46, [[0,0],[22,-13],[33,-9]], { strokeColor: C.teal, strokeWidth: 1.8 });
  dot(194, 42, 7, accent);
  dot(159, 90, 5.3, C.paper);
  dot(27, 137, 6.4, monochrome ? C.ink : C.mint);
  line(201, 77, [[0,0],[10,-2]], { strokeColor: C.teal });
  line(202, 88, [[0,0],[8,3]], { strokeColor: C.teal });
  for (const el of elements.slice(saved)) {
    el.x = x + el.x * scale; el.y = y + el.y * scale;
    el.width *= scale; el.height *= scale;
    if (el.points) el.points = el.points.map(([a,b]) => [a*scale,b*scale]);
    el.strokeWidth *= scale;
  }
}

function mapIcon(x, y, s = 1) {
  const start = elements.length;
  poly(0, 0, [[0,8],[18,0],[39,8],[57,0],[57,46],[39,54],[18,46],[0,54]], C.soft,
    { strokeColor: C.teal, strokeWidth: 1.7 });
  line(18,0, [[0,0],[0,46]], {strokeColor:C.teal,strokeWidth:1.1});
  line(39,8, [[0,0],[0,46]], {strokeColor:C.teal,strokeWidth:1.1});
  line(4,39, [[0,0],[12,-5],[23,-1],[33,-13],[48,-11]], {strokeColor:C.orange,strokeWidth:3});
  for (const el of elements.slice(start)) {el.x=x+el.x*s;el.y=y+el.y*s;el.width*=s;el.height*=s;if(el.points)el.points=el.points.map(([a,b])=>[a*s,b*s]);}
}
function searchIcon(x, y) {
  ellipse(x+4,y,34,34,{strokeColor:C.teal,backgroundColor:C.soft,strokeWidth:2});
  line(x+31,y+29,[[0,0],[19,19]],{strokeColor:C.teal,strokeWidth:3});
  dot(x+15,y+17,2.6,C.teal);dot(x+26,y+11,2.6,C.teal);dot(x+25,y+25,2.6,C.orange);
}
function classIcon(x, y) {
  [[0,0,C.mint],[26,0,C.peach],[0,26,C.lavender],[26,26,C.mint]].forEach(([a,b,c])=>
    box(x+a,y+b,19,19,{strokeColor:C.teal,backgroundColor:c,strokeWidth:1.5,roundness:{type:2}}));
}
function category(x,y,w,letter,title,subtitle,fill,subtitleSize=20) {
  box(x,y,w,101,{strokeColor:C.ink,backgroundColor:C.white,roughness:1.0,strokeWidth:1.6});
  box(x+18,y+19,62,62,{strokeColor:C.ink,backgroundColor:fill,roughness:1.3,strokeWidth:1.6});
  hand(x+34,y+28,letter,35);
  hand(x+100,y+16,title,29);
  text(x+102,y+60,subtitle,subtitleSize,{strokeColor:C.grey});
}
function api(x,y,mobile=false) {
  box(x+7,y+8,278,210,{backgroundColor:C.mint,strokeColor:C.mint,roughness:1.1});
  box(x,y,278,210,{backgroundColor:C.white,strokeColor:C.teal,strokeWidth:2.5,roughness:1.3});
  hand(x+31,y+26,'Shared Python API',24);
  line(x+28,y+69,[[0,0],[216,-1]],{strokeColor:C.mint,strokeWidth:3});
  text(x+29,y+86,'get_embedding()',24,{fontFamily:3});
  [22,37,15,30,42,23,33].forEach((h,i)=>box(x+61+i*22,y+162-h,12,h,
    {backgroundColor:i===4?C.orange:C.teal,strokeColor:i===4?C.orange:C.teal,strokeWidth:0.8,roughness:0.6,roundness:{type:2}}));
  text(x+(mobile?15:36),y+178,'features + metadata',mobile?24:20,{strokeColor:C.grey});
}
function outcomes(x,y) {
  mapIcon(x,y+3);hand(x+81,y+5,'Map & explore',29);
  searchIcon(x+3,y+97);hand(x+81,y+99,'Find similar places',29);
  classIcon(x+7,y+195);hand(x+81,y+195,'Learn downstream',29);
  text(x+82,y+236,'classify · regress · segment',18,{strokeColor:C.grey});
}
function board(w,h) { box(0,0,w,h,{backgroundColor:C.paper,strokeColor:C.paper,roughness:0,strokeWidth:0,roundness:null}); }
function scene(name, width,height,fn,transparent=false) {
  elements.length=0;serial=0;
  if (!transparent) board(width,height);
  else box(0,0,width,height,{strokeColor:'transparent',backgroundColor:'transparent',strokeWidth:0,roughness:0,roundness:null});
  fn();
  return { name,width,height,transparent,elements:structuredClone(elements) };
}
const scenes = [
  scene('earth-embedding-hero',1440,760,()=>{
    globe(58,42,0.83);
    text(278,54,'GEOSPATIAL EMBEDDINGS · PYTHON',18,{strokeColor:C.teal});
    text(272,85,'earth-embedding',75);
    hand(279,184,'Many ways to encode Earth. One place to begin.',29,{strokeColor:C.grey});
    line(67,249,[[0,0],[1308,1]],{strokeColor:C.grid,strokeWidth:1.5,roughness:1});
    category(67,299,435,'A','Image encoders','A1–A4 · imagery → features',C.peach);
    category(67,422,435,'B','Location encoders','longitude + latitude → features',C.mint);
    category(67,545,435,'C','Precomputed products','C1 gridded · C2 sampled',C.lavender);
    api(610,365);
    arrow(509,349,[[0,0],[41,0],[91,62]]);
    arrow(509,472,[[0,0],[91,0]]);
    arrow(509,596,[[0,0],[41,0],[91,-62]]);
    arrow(907,473,[[0,0],[61,0]],{strokeColor:C.ink});
    outcomes(1002,344);
    text(68,699,'IMAGERY  /  COORDINATES  /  EMBEDDING DATA',17,{strokeColor:C.grey});
    hand(1021,690,'Build on Earth, together.',22,{strokeColor:C.teal});
    line(1231,53,[[0,0],[68,0]],{strokeColor:C.grid,strokeWidth:2});
    [0,1,2,3].forEach(i=>dot(1253+i*26,85+(i%2)*16,3.7,i===2?C.orange:C.mint,{strokeColor:C.teal}));
  }),
  scene('earth-embedding-hero-mobile',720,1130,()=>{
    globe(31,25,0.7);
    text(209,43,'GEOSPATIAL EMBEDDINGS',16,{strokeColor:C.teal});
    text(204,81,'earth-embedding',48);
    hand(57,195,'Many ways to encode Earth.',29,{strokeColor:C.grey});
    hand(57,234,'One place to begin.',29,{strokeColor:C.grey});
    category(54,315,612,'A','Image encoders','A1–A4 · imagery → features',C.peach,26);
    category(54,438,612,'B','Location encoders','longitude + latitude → features',C.mint,26);
    category(54,561,612,'C','Precomputed products','C1 gridded · C2 sampled',C.lavender,26);
    arrow(360,679,[[0,0],[0,53]]);
    api(221,750,true);
    arrow(360,981,[[0,0],[0,42]]);
    hand(67,1050,'Map · retrieve · learn downstream',32);
  }),
  scene('earth-embedding-logo',240,240,()=>globe(7,23,1),true),
];

await fs.mkdir(workspace,{recursive:true});
await fs.mkdir(output,{recursive:true});
await fs.writeFile(path.join(workspace,'index.html'),`<!doctype html><html><head><meta charset="utf-8"><title>earth-embedding brand renderer</title></head><body><main id="preview"></main><script type="module" src="/renderer.js"></script></body></html>`);
await fs.writeFile(path.join(workspace,'renderer.js'),`
import { convertToExcalidrawElements, exportToSvg, exportToBlob } from '@excalidraw/excalidraw';
import '@excalidraw/excalidraw/index.css';
window.EXCALIDRAW_ASSET_PATH = '/node_modules/@excalidraw/excalidraw/dist/prod/';
window.renderBrand = async (scene) => {
  const elements = convertToExcalidrawElements(scene.elements, { regenerateIds: false });
  const appState = { viewBackgroundColor: '${C.paper}', exportBackground: !scene.transparent,
    exportWithDarkMode: false, exportEmbedScene: false, exportScale: 2, gridSize: null };
  const opts = { elements, appState, files: {}, exportPadding: 0 };
  // exportToSvg initializes and embeds the package's Excalifont/Cascadia fonts.
  const svg = await exportToSvg(opts);
  await document.fonts.ready;
  const blob = await exportToBlob({ ...opts, mimeType: 'image/png',
    getDimensions: (width,height) => ({width:width*2,height:height*2,scale:2}) });
  const bytes = new Uint8Array(await blob.arrayBuffer());
  let binary = ''; for (let i=0;i<bytes.length;i+=32768) binary += String.fromCharCode(...bytes.subarray(i,i+32768));
  const source = { type:'excalidraw', version:2, source:'https://excalidraw.com', elements, appState,
    files:{}, earthEmbeddingBrand:{ title:scene.name, originalArtwork:true, renderer:'@excalidraw/excalidraw@0.18.0', license:'Apache-2.0' } };
  document.querySelector('#preview').replaceChildren(svg);
  return {svg: svg.outerHTML, png:btoa(binary), source,
    stats:{elements:elements.length,width:svg.getAttribute('width'),height:svg.getAttribute('height'),loadedFonts:[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family))]}};
};
window.brandReady = true;
`);

const server = await createServer({root:workspace,configFile:false,server:{host:'127.0.0.1',port:5193,strictPort:false},logLevel:'error'});
await server.listen();
const address = server.httpServer.address();
let executablePath = process.env.BRAND_CHROMIUM_EXECUTABLE;
if(!executablePath && process.platform==='win32') {
  for(const candidate of ['C:/Program Files/Google/Chrome/Application/chrome.exe','C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe']) {
    try {await fs.access(candidate);executablePath=candidate;break;} catch {}
  }
}
const errors=[];
let browser;
try {
  browser = await chromium.launch({headless:true,...(executablePath?{executablePath}:{})});
  const page = await browser.newPage({viewport:{width:1500,height:840},deviceScaleFactor:1});
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${address.port}`);
  await page.waitForFunction(()=>window.brandReady===true);
  const manifest = [];
  for(const input of scenes) {
    const result=await page.evaluate(scene=>window.renderBrand(scene),input);
    await fs.writeFile(path.join(output,`${input.name}.excalidraw`),JSON.stringify(result.source,null,2)+'\n');
    await fs.writeFile(path.join(output,`${input.name}.svg`),result.svg+'\n');
    await fs.writeFile(path.join(output,`${input.name}.png`),Buffer.from(result.png,'base64'));
    manifest.push({name:input.name,...result.stats});
  }
  // Review the exported files as standalone images, as GitHub will display them.
  const dataImage = async name => 'data:image/svg+xml;base64,' +
    Buffer.from(await fs.readFile(path.join(output, name+'.svg'))).toString('base64');
  const desktop = await dataImage('earth-embedding-hero');
  const mobile = await dataImage('earth-embedding-hero-mobile');
  const logo = await dataImage('earth-embedding-logo');
  await page.setViewportSize({width:1280,height:676});
  await page.setContent(`<style>html,body{margin:0}img{width:100%;display:block}</style><img src="${desktop}">`);
  await page.locator('img').evaluate(img=>img.decode());
  await page.screenshot({path:path.join(workspace,'preview-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:613});
  await page.setContent(`<style>html,body{margin:0}img{width:100%;display:block}</style><img src="${mobile}">`);
  await page.locator('img').evaluate(img=>img.decode());
  await page.screenshot({path:path.join(workspace,'preview-mobile-390.png'),fullPage:true});
  await page.setViewportSize({width:520,height:260});
  await page.setContent(`<style>html,body{margin:0;display:flex}div{width:260px;height:260px;display:grid;place-items:center;background:#faf8f1}div+div{background:#182323}img{width:180px}</style><div><img src="${logo}"></div><div><img src="${logo}"></div>`);
  await page.locator('img').first().evaluate(img=>img.decode());
  await page.screenshot({path:path.join(workspace,'preview-logo-context.png')});
  await fs.writeFile(path.join(workspace,'render-report.json'),JSON.stringify({renderer:'@excalidraw/excalidraw@0.18.0',errors,manifest},null,2)+'\n');
  console.log(JSON.stringify({output,errors,manifest},null,2));
} finally {await browser?.close();await server.close();}
