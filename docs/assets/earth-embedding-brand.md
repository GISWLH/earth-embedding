# earth-embedding visual identity

The original orbital Earth mark connects a hand-sketched globe to three feature-vector
nodes. Ink teal, sage, and a small terracotta accent keep the identity approachable
and readable. The warm-paper hero explains the shared interface without asserting
model counts, benchmark results, or universal downstream capabilities.

| Asset | Editable source | Web vector | Raster fallback |
| --- | --- | --- | --- |
| Desktop hero, 1440 × 760 design | [Excalidraw](earth-embedding-hero.excalidraw) | [SVG](earth-embedding-hero.svg) | [PNG, 2×](earth-embedding-hero.png) |
| Mobile hero, 720 × 1130 design | [Excalidraw](earth-embedding-hero-mobile.excalidraw) | [SVG](earth-embedding-hero-mobile.svg) | [PNG, 2×](earth-embedding-hero-mobile.png) |
| Transparent logo, 240 × 240 design | [Excalidraw](earth-embedding-logo.excalidraw) | [SVG](earth-embedding-logo.svg) | [PNG, 2×](earth-embedding-logo.png) |

All marks, shapes, arrows, and text are native editable Excalidraw elements. Open
the `.excalidraw` files in [Excalidraw](https://excalidraw.com) to change the artwork.
The drawings contain no raster background or AI-generated image. The hero's A/B/C
labels follow the project's release taxonomy; C2 is a taxonomy category, not a
claim that a particular C2 product is implemented. Downstream tasks describe what
users can build with suitable features and task-specific methods.

## Rebuild

From the repository root, install the isolated artwork tooling and run:

```sh
npm install --prefix work/brand --save-exact @excalidraw/excalidraw@0.18.0 react@19.2.0 react-dom@19.2.0 vite@7.1.12 playwright@1.56.1
node scripts/render_brand.mjs
```

The script uses the actual Excalidraw `convertToExcalidrawElements`, `exportToSvg`,
and `exportToBlob` APIs through headless Chromium. On Windows it can use the installed
Chrome or Edge. Elsewhere install Playwright's Chromium, or set
`BRAND_CHROMIUM_EXECUTABLE` to a Chromium executable. The Vite server binds only
to `127.0.0.1` and closes after rendering. Development dependencies are isolated
under `work/brand`; the Python package does not depend on them.

Exports include embedded Excalifont/Cascadia font subsets. PNGs are rendered by
Excalidraw at 2× resolution. Review snapshots at 1280 px and 390 px, a light/dark
logo preview, and a compact rendering report are written to `work/brand`.

For a responsive GitHub README, use:

```html
<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/earth-embedding-hero-mobile.svg">
  <img src="docs/assets/earth-embedding-hero.svg" width="100%"
       alt="earth-embedding: image encoders, location encoders and precomputed products connect through a shared Python interface to geospatial workflows.">
</picture>
```

## Credits and licensing

Original earth-embedding artwork is distributed under the repository's Apache-2.0 license.
The export engine is [Excalidraw](https://github.com/excalidraw/excalidraw) (MIT).
Excalifont is copyright © 2024 Excalidraw, designed by Ján Filípek / DizajnDesign
and derived from Virgil by Your Own Font Foundry; it is distributed under the
[SIL Open Font License 1.1](https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/fonts/Excalifont/index.ts).
Cascadia is by Microsoft and distributed under the
[SIL Open Font License 1.1](https://github.com/microsoft/cascadia-code/blob/main/LICENSE).
These font licenses apply to the embedded font data, independently of the artwork.
Complete notices are retained locally: [Excalifont OFL](licenses/Excalifont-OFL.txt),
[Cascadia OFL](licenses/Cascadia-OFL.txt), and [font provenance](licenses/font-provenance.json).

Palette: paper `#faf8f1`, ink `#173f40`, teal `#267b72`, sage `#d8ece0`,
terracotta `#d98950`, muted text `#57706b`.
