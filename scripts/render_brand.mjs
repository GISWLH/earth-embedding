#!/usr/bin/env node
/**
 * Rebuild the earth-embedding brand artwork with Excalidraw itself.
 *
 * npm install --prefix work/brand --save-exact @excalidraw/excalidraw@0.18.0 \
 *   react@19.2.0 react-dom@19.2.0 vite@7.1.12 playwright@1.56.1
 * node scripts/render_brand.mjs [--only banner,logo]
 *
 * Uses a temporary, loopback-only Vite server and headless Chromium. Set
 * BRAND_CHROMIUM_EXECUTABLE for a system browser, or install Playwright Chromium.
 * Artwork contains editable native Excalidraw elements, never a raster backdrop.
 * Outputs go to docs/assets/brand/: <name>.excalidraw and <name>.svg for every
 * scene, plus 2x PNGs for the logo and banner (README social preview, favicons).
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const workspace = path.join(root, 'work', 'brand');
const output = path.join(root, 'docs', 'assets', 'brand');
const require = createRequire(path.join(workspace, 'package.json'));
const { chromium } = require('playwright');
const { createServer } = await import(pathToFileURL(require.resolve('vite')).href);

const C = {
  paper: '#faf8f1', ink: '#173f40', teal: '#267b72', mint: '#d8ece0',
  soft: '#edf3eb', orange: '#d98950', peach: '#f4e3d2', grey: '#57706b',
  lavender: '#e9e6f2', purple: '#6b6487', white: '#fffef9', grid: '#dce5d9',
  sky: '#dcebf2', blue: '#3f7cac', sand: '#efe3c6', green: '#5f9e6e', deep: '#1f5f58',
};
const FONT = { hand: 5, body: 6, code: 3 }; // Excalifont, Nunito, Cascadia
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
  text: value, fontSize: size, fontFamily: FONT.body, textAlign: 'left', verticalAlign: 'top',
  lineHeight: 1.25, roughness: 0, strokeWidth: 1, ...extra,
});
const hand = (x, y, value, size = 26, extra = {}) => text(x, y, value, size, { fontFamily: FONT.hand, ...extra });
const code = (x, y, value, size = 22, extra = {}) => text(x, y, value, size, { fontFamily: FONT.code, ...extra });
const poly = (x, y, points, color = C.teal, extra = {}) => line(x, y, [...points, points[0]], {
  backgroundColor: color, strokeColor: color, strokeWidth: 1, roughness: 1.1, ...extra,
});
const dot = (x, y, r, fill, extra = {}) => ellipse(x-r, y-r, r*2, r*2,
  { strokeColor: C.ink, backgroundColor: fill, strokeWidth: 1.4, ...extra });

/** Draw with fn() in local coordinates, then move/scale the new elements to (x, y). */
function place(x, y, scale, fn) {
  const saved = elements.length;
  fn();
  for (const el of elements.slice(saved)) {
    el.x = x + el.x * scale; el.y = y + el.y * scale;
    el.width *= scale; el.height *= scale;
    if (el.points) el.points = el.points.map(([a, b]) => [a * scale, b * scale]);
    if (el.type === 'text') el.fontSize *= scale;
    else el.strokeWidth *= Math.max(scale, 0.55);
  }
}

/**
 * Logo mark, 240 x 240 design: a sketched globe inside vector brackets whose
 * lower-right edge breaks into embedding cells. Earth, encoded.
 */
function mark({ mono = false } = {}) {
  const fill = mono ? C.white : C.mint;
  const land = mono ? C.ink : C.teal;
  // Vector brackets.
  line(30, 34, [[26, 0], [0, 2], [-2, 172], [26, 174]], { strokeWidth: 5.5, roughness: 1.4 });
  line(210, 34, [[-26, 0], [0, 2], [2, 172], [-26, 174]], { strokeWidth: 5.5, roughness: 1.4 });
  // Globe and graticule.
  ellipse(46, 44, 148, 148, { backgroundColor: fill, strokeWidth: 3.4, roughness: 1.2 });
  ellipse(95, 46, 50, 144, { strokeColor: C.teal, opacity: 55, strokeWidth: 1.6 });
  line(52, 92, [[0, 0], [34, 9], [68, 11], [104, 7], [136, 0]], { strokeColor: C.teal, opacity: 50, strokeWidth: 1.5 });
  line(48, 140, [[0, 0], [36, -6], [74, -8], [108, -5], [142, 0]], { strokeColor: C.teal, opacity: 50, strokeWidth: 1.5 });
  // Continents.
  poly(70, 64, [[0, 8], [16, -2], [32, 1], [40, 12], [30, 25], [32, 36], [17, 41], [9, 32], [-3, 31], [-7, 19]], land, { opacity: 92 });
  poly(96, 112, [[0, 0], [20, 0], [30, 14], [22, 30], [14, 42], [6, 32], [1, 16]], land, { opacity: 92 });
  poly(140, 70, [[0, 1], [18, -4], [30, 6], [28, 20], [16, 26], [6, 18], [-4, 12]], land, { opacity: 92 });
  // Embedding cells breaking off the lower-right edge.
  const cells = [
    [146, 128, 20, C.teal], [168, 128, 20, mono ? C.ink : C.deep],
    [134, 150, 20, mono ? C.white : C.lavender], [156, 150, 20, mono ? C.ink : C.orange],
    [122, 172, 20, mono ? C.white : C.peach], [144, 172, 20, C.teal],
    [182, 153, 15, mono ? C.white : C.mint], [192, 112, 13, mono ? C.ink : C.teal],
    [170, 182, 13, mono ? C.white : C.lavender],
  ];
  for (const [x, y, s, color] of cells) {
    box(x, y, s, s, { backgroundColor: color, strokeColor: C.ink, strokeWidth: 1.7,
      roughness: 0.9, roundness: { type: 2 } });
  }
}

function satelliteImage() { // 150 x 150 imagery tile with fields and a river
  box(0, 0, 150, 150, { backgroundColor: C.sand, strokeWidth: 2.2, roundness: { type: 2 } });
  poly(10, 12, [[0, 0], [52, 4], [48, 46], [-2, 42]], C.green, { fillStyle: 'hachure', strokeColor: C.green, opacity: 85 });
  poly(84, 10, [[0, 4], [54, 0], [56, 40], [2, 44]], '#b8cf8e', { strokeColor: C.green, opacity: 90 });
  poly(80, 94, [[0, 0], [58, 4], [56, 46], [4, 44]], C.green, { fillStyle: 'cross-hatch', strokeColor: C.green, opacity: 80 });
  poly(12, 98, [[0, 0], [40, -2], [44, 40], [2, 42]], '#c9b98f', { strokeColor: '#a89466', opacity: 90 });
  line(-2, 62, [[0, 0], [30, 8], [62, 0], [92, 16], [124, 10], [152, 22]], { strokeColor: C.blue, strokeWidth: 7, roughness: 1.6, opacity: 85 });
  line(70, 0, [[0, 0], [6, 150]], { strokeColor: C.white, strokeWidth: 3, roughness: 1.2, opacity: 80 });
}
function satellite() { // ~70 x 40
  box(24, 10, 22, 20, { backgroundColor: C.white, strokeWidth: 1.8, roundness: { type: 2 } });
  box(0, 14, 20, 12, { backgroundColor: C.sky, strokeColor: C.blue, strokeWidth: 1.5, fillStyle: 'cross-hatch', roundness: null });
  box(50, 14, 20, 12, { backgroundColor: C.sky, strokeColor: C.blue, strokeWidth: 1.5, fillStyle: 'cross-hatch', roundness: null });
  line(35, 30, [[0, 0], [0, 8]], { strokeWidth: 1.6 });
}
function placeMap() { // 150 x 150 map with graticule and a pin
  box(0, 0, 150, 150, { backgroundColor: C.soft, strokeWidth: 2.2, roundness: { type: 2 } });
  for (const v of [38, 75, 112]) {
    line(v, 6, [[0, 0], [2, 138]], { strokeColor: C.teal, opacity: 35, strokeWidth: 1.2 });
    line(6, v, [[0, 0], [138, -2]], { strokeColor: C.teal, opacity: 35, strokeWidth: 1.2 });
  }
  poly(20, 96, [[0, 0], [30, -10], [58, 4], [70, 30], [24, 40]], C.mint, { strokeColor: C.teal, strokeWidth: 1.2 });
  // Pin.
  line(75, 104, [[0, 0], [-17, -32], [-14, -50], [0, -60], [14, -50], [17, -32], [0, 0]], {
    backgroundColor: C.orange, strokeColor: C.ink, strokeWidth: 2, roughness: 0.9 });
  dot(75, 60, 6, C.white, { strokeWidth: 1.6 });
}
function products() { // ~170 x 170 stacked embedding tiles
  const palette = [C.teal, C.mint, C.lavender, C.peach, C.deep, C.orange, C.sky, C.green];
  box(36, 0, 130, 130, { backgroundColor: C.lavender, strokeWidth: 1.8, roundness: { type: 2 } });
  box(18, 18, 130, 130, { backgroundColor: C.peach, strokeWidth: 1.8, roundness: { type: 2 } });
  box(0, 36, 130, 130, { backgroundColor: C.white, strokeWidth: 2.2, roundness: { type: 2 } });
  let k = 0;
  for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) {
    box(10 + c * 28, 46 + r * 28, 26, 26, { backgroundColor: palette[(r * 3 + c * 5 + k++) % palette.length],
      strokeColor: C.ink, strokeWidth: 0.8, roughness: 0.6, roundness: null, opacity: 90 });
  }
}
function brace(height) { // right curly brace
  const h = height, m = h / 2;
  line(0, 0, [[0, 0], [16, 6], [18, m - 18], [34, m], [18, m + 18], [16, h - 6], [0, h]],
    { strokeWidth: 3, roughness: 1.2 });
}
function apiChip(w = 330) {
  box(8, 9, w, 112, { backgroundColor: C.mint, strokeColor: C.mint, roughness: 1.1 });
  box(0, 0, w, 112, { backgroundColor: C.white, strokeColor: C.teal, strokeWidth: 2.6, roughness: 1.3 });
  code(26, 22, 'get_embedding()', 30, { strokeColor: C.ink });
  text(28, 70, '22 models · one interface', 19, { strokeColor: C.grey });
}
function vector(n = 8, vertical = true) {
  const shades = [C.teal, C.mint, C.deep, C.orange, C.lavender, C.teal, C.peach, C.deep];
  for (let i = 0; i < n; i++) {
    const [x, y] = vertical ? [0, i * 25] : [i * 25, 0];
    box(x, y, 23, 23, { backgroundColor: shades[i % shades.length], strokeWidth: 1.3,
      roughness: 0.8, roundness: { type: 2 } });
  }
  if (vertical) {
    line(-8, -6, [[8, 0], [0, 0], [0, n * 25 + 10], [8, n * 25 + 10]], { strokeWidth: 2.4 });
    line(31, -6, [[-8, 0], [0, 0], [0, n * 25 + 10], [-8, n * 25 + 10]], { strokeWidth: 2.4 });
  } else {
    line(-6, -8, [[0, 8], [0, 0], [n * 25 + 10, 0], [n * 25 + 10, 8]], { strokeWidth: 2.4 });
    line(-6, 31, [[0, -8], [0, 0], [n * 25 + 10, 0], [n * 25 + 10, -8]], { strokeWidth: 2.4 });
  }
}
function space(w = 380, h = 250) { // embedding space with three clusters
  box(0, 0, w, h, { backgroundColor: C.white, strokeColor: C.ink, strokeWidth: 2, roughness: 1.2 });
  arrow(24, h - 24, [[0, 0], [w - 60, 0]], { strokeColor: C.grey, strokeWidth: 1.6 });
  arrow(24, h - 24, [[0, 0], [0, -(h - 56)]], { strokeColor: C.grey, strokeWidth: 1.6 });
  const clusters = [
    [0.26, 0.40, C.blue, 'water', -34, -64],
    [0.74, 0.42, C.orange, 'city', -20, -66],
    [0.44, 0.74, C.green, 'forest', 34, -16],
  ];
  const jitter = [[0, 0], [16, -9], [-14, 8], [10, 14], [-6, -15], [22, 8], [-20, -4]];
  for (const [cx, cy, color, label, lx, ly] of clusters) {
    for (const [dx, dy] of jitter) dot(cx * w + dx, cy * h + dy, 5.5, color, { strokeColor: color, strokeWidth: 1 });
    hand(cx * w + lx, cy * h + ly, label, 26, { strokeColor: color });
  }
  ellipse(0.74 * w - 36, 0.42 * h - 29, 72, 58, { strokeColor: C.teal, strokeStyle: 'dashed', strokeWidth: 1.8 });
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
  code(x+29,y+86,'get_embedding()',24);
  [22,37,15,30,42,23,33].forEach((h,i)=>box(x+61+i*22,y+162-h,12,h,
    {backgroundColor:i===4?C.orange:C.teal,strokeColor:i===4?C.orange:C.teal,strokeWidth:0.8,roughness:0.6,roundness:{type:2}}));
  text(x+(mobile?32:46),y+174,'features + metadata',mobile?22:19,{strokeColor:C.grey});
}
function mapIcon(x, y) {
  place(x, y, 1, () => {
    poly(0, 0, [[0,8],[18,0],[39,8],[57,0],[57,46],[39,54],[18,46],[0,54]], C.soft,
      { strokeColor: C.teal, strokeWidth: 1.7 });
    line(18,0, [[0,0],[0,46]], {strokeColor:C.teal,strokeWidth:1.1});
    line(39,8, [[0,0],[0,46]], {strokeColor:C.teal,strokeWidth:1.1});
    line(4,39, [[0,0],[12,-5],[23,-1],[33,-13],[48,-11]], {strokeColor:C.orange,strokeWidth:3});
  });
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
function outcomes(x,y) {
  mapIcon(x,y+3);hand(x+81,y+5,'Map & explore',29);
  searchIcon(x+3,y+97);hand(x+81,y+99,'Find similar places',29);
  classIcon(x+7,y+195);hand(x+81,y+195,'Learn downstream',29);
  text(x+82,y+236,'classify · regress · segment',18,{strokeColor:C.grey});
}
function board(w,h) { box(0,0,w,h,{backgroundColor:C.paper,strokeColor:C.paper,roughness:0,strokeWidth:0,roundness:null}); }
/** A paper card with rounded corners on a transparent canvas; reads well on light and dark pages. */
function card(w,h,radius=36) {
  box(0,0,w,h,{strokeColor:'transparent',backgroundColor:'transparent',strokeWidth:0,roughness:0,roundness:null});
  box(0,0,w,h,{backgroundColor:C.paper,strokeColor:C.grid,strokeWidth:1.5,roughness:0,roundness:{type:3,value:radius}});
}
function scene(name, width,height,fn,{ transparent = false, rounded = false, png = false } = {}) {
  elements.length=0;serial=0;
  if (rounded) card(width,height);
  else if (!transparent) board(width,height);
  else box(0,0,width,height,{strokeColor:'transparent',backgroundColor:'transparent',strokeWidth:0,roughness:0,roundness:null});
  fn();
  return { name,width,height,transparent:transparent||rounded,png,elements:structuredClone(elements) };
}
const label = (x, y, value, size = 24) => hand(x, y, value, size, { strokeColor: C.grey });

const scenes = [
  scene('banner', 1600, 620, () => {
    place(52, 34, 0.94, () => mark());
    hand(318, 58, 'earth-embedding', 104);
    hand(324, 190, 'Images, places and products → Earth embeddings, in one Python call.', 33, { strokeColor: C.grey });
    line(64, 284, [[0, 0], [1472, 2]], { strokeColor: C.grid, strokeWidth: 1.6, roughness: 1 });
    place(72, 348, 1, satelliteImage);
    place(150, 306, 0.9, satellite);
    label(104, 512, 'imagery');
    place(262, 348, 1, placeMap);
    label(296, 512, 'lon, lat');
    place(448, 330, 0.92, products);
    label(458, 512, 'products');
    place(632, 330, 1, () => brace(180));
    arrow(676, 420, [[0, 0], [44, 0]]);
    place(732, 364, 1, () => apiChip(318));
    arrow(1072, 420, [[0, 0], [50, 0]]);
    place(1146, 336, 1, () => vector(7));
    label(1126, 512, 'vector');
    arrow(1196, 420, [[0, 0], [46, 0]]);
    place(1252, 326, 0.8, () => space(380, 230));
    hand(1272, 512, 'similar places cluster', 24, { strokeColor: C.teal });
  }, { rounded: true, png: true }),
  scene('banner-mobile', 720, 1160, () => {
    place(26, 26, 0.62, () => mark());
    hand(196, 62, 'earth-embedding', 62);
    hand(40, 202, 'Images, places and products →', 33, { strokeColor: C.grey });
    hand(40, 246, 'Earth embeddings, in one Python call.', 33, { strokeColor: C.grey });
    line(40, 318, [[0, 0], [640, 1]], { strokeColor: C.grid, strokeWidth: 1.6, roughness: 1 });
    place(44, 364, 0.95, satelliteImage);
    place(118, 330, 0.8, satellite);
    label(66, 518, 'imagery', 26);
    place(285, 364, 0.95, placeMap);
    label(310, 518, 'lon, lat', 26);
    place(504, 350, 0.9, products);
    label(510, 518, 'products', 26);
    arrow(360, 568, [[0, 0], [0, 46]]);
    place(195, 628, 1, () => apiChip(330));
    arrow(360, 762, [[0, 0], [0, 40]]);
    place(258, 822, 1, () => vector(8, false));
    arrow(360, 870, [[0, 0], [0, 34]]);
    place(160, 912, 0.8, () => space(500, 200));
    hand(232, 1086, 'similar places cluster', 28, { strokeColor: C.teal });
  }, { rounded: true }),
  scene('how-it-works', 1440, 460, () => {
    category(60, 40, 435, 'A', 'Image encoders', 'A1–A4 · imagery → features', C.peach);
    category(60, 163, 435, 'B', 'Location encoders', 'longitude + latitude → features', C.mint);
    category(60, 286, 435, 'C', 'Precomputed products', 'C1 gridded · C2 sampled', C.lavender);
    api(603, 106);
    arrow(502, 90, [[0, 0], [41, 0], [91, 62]]);
    arrow(502, 213, [[0, 0], [91, 0]]);
    arrow(502, 337, [[0, 0], [41, 0], [91, -62]]);
    arrow(900, 214, [[0, 0], [61, 0]], { strokeColor: C.ink });
    outcomes(995, 85);
    label(62, 414, 'Classes describe the delivered object, not the architecture.', 20);
  }, { rounded: true }),
  scene('how-it-works-mobile', 720, 860, () => {
    category(54, 30, 612, 'A', 'Image encoders', 'A1–A4 · imagery → features', C.peach, 26);
    category(54, 153, 612, 'B', 'Location encoders', 'longitude + latitude → features', C.mint, 26);
    category(54, 276, 612, 'C', 'Precomputed products', 'C1 gridded · C2 sampled', C.lavender, 26);
    arrow(360, 394, [[0, 0], [0, 53]]);
    api(221, 465, true);
    arrow(360, 696, [[0, 0], [0, 42]]);
    hand(84, 762, 'Map · retrieve · learn downstream', 32);
  }, { rounded: true }),
  scene('logo', 240, 240, () => {
    box(0, 0, 240, 240, { backgroundColor: C.paper, strokeColor: C.grid, strokeWidth: 2, roughness: 0, roundness: { type: 3, value: 52 } });
    place(12, 12, 0.9, () => mark());
  }, { transparent: true, png: true }),
  scene('demo-workflow', 1200, 560, () => {
    hand(44, 30, 'From a place to a result', 34);
    text(44, 80, 'REAL DATA  /  CPU  /  REUSABLE OUTPUTS', 16, { strokeColor: C.grey });
    const card = (x, y, w, title, api, fill) => {
      box(x, y, w, 108, { backgroundColor: fill });
      hand(x + 15, y + 18, title, 24);
      code(x + 15, y + 58, api, 15, { strokeColor: C.teal });
    };
    card(44, 150, 270, 'Region or lon / lat', 'load_demo /\nget_location_embeddings', C.mint);
    card(400, 150, 255, 'Embedding', 'pca_colors', C.lavender);
    card(752, 150, 394, 'Spatial map', 'plot_map → PNG', C.peach);
    arrow(320, 204, [[0, 0], [72, 0]]); arrow(662, 204, [[0, 0], [80, 0]]);
    card(44, 350, 230, 'Features + labels', 'load_demo("bayarea")', C.mint);
    card(316, 350, 242, 'Spatial folds', 'west | buffer | east', C.soft);
    card(600, 350, 243, 'Linear classifier', 'classify_demo', C.lavender);
    card(885, 350, 261, 'Map + metrics', 'plot_classification', C.peach);
    for (const x of [278, 562, 847]) arrow(x, 404, [[0, 0], [30, 0]]);
    text(44, 510, 'PCA colors ≠ classes. Bay Area demo ≠ global benchmark.', 19, { strokeColor: C.grey });
  }, { rounded: true }),
  scene('demo-workflow-mobile', 660, 1090, () => {
    hand(38, 30, 'A place. An embedding. A result.', 29);
    const card = (y, title, api, fill) => {
      box(45, y, 570, 95, { backgroundColor: fill });
      hand(64, y + 13, title, 27);
      code(64, y + 58, api, 19, { strokeColor: C.teal });
    };
    card(105, 'Region / longitude + latitude', 'load_demo / get_location_embeddings', C.mint);
    card(240, 'Embedding → PCA colors', 'pca_colors', C.lavender);
    card(375, 'Your first spatial map', 'plot_map → PNG', C.peach);
    arrow(330, 207, [[0, 0], [0, 26]]); arrow(330, 342, [[0, 0], [0, 26]]);
    hand(45, 514, 'Add labels. Learn a downstream task.', 27);
    card(576, 'Features + labels → two spatial folds', 'load_demo("bayarea")', C.mint);
    card(711, 'Out-of-fold linear classifier', 'classify_demo', C.lavender);
    card(846, 'Held-out map + OA / F1 / recall', 'plot_classification', C.peach);
    arrow(330, 678, [[0, 0], [0, 26]]); arrow(330, 813, [[0, 0], [0, 26]]);
    text(45, 986, 'PCA colors are not land-cover classes.\nBay Area regional software demonstration.', 21, { strokeColor: C.grey });
  }, { rounded: true }),
];

const only = process.argv.includes('--only')
  ? new Set(process.argv[process.argv.indexOf('--only') + 1].split(','))
  : null;
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
  // exportToSvg initializes and embeds the package's Excalifont/Nunito/Cascadia fonts.
  const svg = await exportToSvg(opts);
  await document.fonts.ready;
  let png = null;
  if (scene.png) {
    const blob = await exportToBlob({ ...opts, mimeType: 'image/png',
      getDimensions: (width,height) => ({width:width*2,height:height*2,scale:2}) });
    const bytes = new Uint8Array(await blob.arrayBuffer());
    let binary = ''; for (let i=0;i<bytes.length;i+=32768) binary += String.fromCharCode(...bytes.subarray(i,i+32768));
    png = btoa(binary);
  }
  const source = { type:'excalidraw', version:2, source:'https://excalidraw.com', elements, appState,
    files:{}, earthEmbeddingBrand:{ title:scene.name, originalArtwork:true, renderer:'@excalidraw/excalidraw@0.18.0', license:'Apache-2.0' } };
  document.querySelector('#preview').replaceChildren(svg);
  return {svg: svg.outerHTML, png, source,
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
  for(const input of scenes.filter(s => !only || only.has(s.name))) {
    const result=await page.evaluate(scene=>window.renderBrand(scene),input);
    await fs.writeFile(path.join(output,`${input.name}.excalidraw`),JSON.stringify(result.source,null,2)+'\n');
    await fs.writeFile(path.join(output,`${input.name}.svg`),result.svg+'\n');
    if (result.png) await fs.writeFile(path.join(output,`${input.name}.png`),Buffer.from(result.png,'base64'));
    manifest.push({name:input.name,...result.stats});
  }
  // Review the exported files as standalone images, as GitHub will display them.
  const preview = async (name, width, background = '#faf8f1') => {
    const file = path.join(output, name + '.svg');
    try { await fs.access(file); } catch { return; }
    const data = 'data:image/svg+xml;base64,' + (await fs.readFile(file)).toString('base64');
    await page.setViewportSize({width, height: 400});
    await page.setContent(`<style>html,body{margin:0;background:${background}}img{width:100%;display:block}</style><img src="${data}">`);
    await page.locator('img').evaluate(img=>img.decode());
    await page.screenshot({path:path.join(workspace,`preview-${name}-${width}.png`),fullPage:true});
  };
  await preview('banner', 900, '#0d1117');
  await preview('banner-mobile', 390, '#0d1117');
  await preview('how-it-works', 900);
  await preview('demo-workflow', 900);
  const logoFile = path.join(output, 'logo.svg');
  try {
    await fs.access(logoFile);
    const logo = 'data:image/svg+xml;base64,' + (await fs.readFile(logoFile)).toString('base64');
    await page.setViewportSize({width:640,height:220});
    await page.setContent(`<style>html,body{margin:0;display:flex;align-items:center}div{width:220px;height:220px;display:grid;place-items:center;background:#faf8f1}div+div{background:#0d1117}img.l{width:180px}img.s{width:32px}</style><div><img class="l" src="${logo}"></div><div><img class="l" src="${logo}"></div><div style="width:200px"><img class="s" src="${logo}"><img style="width:64px" src="${logo}"></div>`);
    await page.locator('img').first().evaluate(img=>img.decode());
    await page.screenshot({path:path.join(workspace,'preview-logo.png')});
  } catch {}
  await fs.writeFile(path.join(workspace,'render-report.json'),JSON.stringify({renderer:'@excalidraw/excalidraw@0.18.0',errors,manifest},null,2)+'\n');
  console.log(JSON.stringify({output,errors,manifest:manifest.map(m=>[m.name,m.width,m.height,m.elements,m.loadedFonts.join('/')])}));
} finally {await browser?.close();await server.close();}
