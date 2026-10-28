# earth-embedding visual identity

The mark is a hand-sketched globe inside vector brackets whose lower-right edge
breaks into a few embedding cells: Earth, encoded. The banner tells the same story
as a sketch, with imagery, places and products flowing through `get_embedding()` into a
vector and an embedding space where similar places cluster. Ink teal, sage and a
small terracotta accent on warm paper keep every asset in one family. Every scene sits on
its own paper card, so it reads on light and dark pages alike.

| Asset | Design size | Editable source | Web vector | Raster |
| --- | --- | --- | --- | --- |
| README banner | 1600 × 620 | [Excalidraw](banner.excalidraw) | [SVG](banner.svg) | [PNG, 2×](banner.png) |
| README banner, narrow screens | 720 × 1160 | [Excalidraw](banner-mobile.excalidraw) | [SVG](banner-mobile.svg) | — |
| Logo on a paper tile | 240 × 240 | [Excalidraw](logo.excalidraw) | [SVG](logo.svg) | [PNG, 2×](logo.png) |
| How it works | 1440 × 460 | [Excalidraw](how-it-works.excalidraw) | [SVG](how-it-works.svg) | — |
| How it works, narrow screens | 720 × 860 | [Excalidraw](how-it-works-mobile.excalidraw) | [SVG](how-it-works-mobile.svg) | — |
| Real-data workflow | 1200 × 560 | [Excalidraw](demo-workflow.excalidraw) | [SVG](demo-workflow.svg) | — |
| Real-data workflow, narrow screens | 660 × 1090 | [Excalidraw](demo-workflow-mobile.excalidraw) | [SVG](demo-workflow-mobile.svg) | — |

`banner.png` (3200 × 1240) also works as the repository's social preview image
(GitHub → Settings → Social preview). The logo PNG suits avatars and favicons.

All marks, shapes, arrows and text are native editable Excalidraw elements. Open the
`.excalidraw` files in [Excalidraw](https://excalidraw.com) to change the artwork. The
drawings contain no raster background or AI-generated image. The A/B/C labels follow the
project's release taxonomy; C2 is a taxonomy category, not a claim that a particular C2
product is implemented. Downstream tasks describe what users can build with suitable
features and task-specific methods.

## Rebuild

From the repository root, install the isolated artwork tooling and run:

```sh
npm install --prefix work/brand --save-exact @excalidraw/excalidraw@0.18.0 react@19.2.0 react-dom@19.2.0 vite@7.1.12 playwright@1.56.1
node scripts/render_brand.mjs               # all scenes
node scripts/render_brand.mjs --only banner,logo
python scripts/optimize_images.py docs/assets/brand
```

The script builds each scene from code and exports it with Excalidraw's own
`convertToExcalidrawElements`, `exportToSvg` and `exportToBlob` APIs in headless
Chromium. On Windows it can use the installed Chrome or Edge. Elsewhere install
Playwright's Chromium, or set `BRAND_CHROMIUM_EXECUTABLE` to a Chromium executable.
The Vite server binds only to `127.0.0.1` and closes after rendering. Development
dependencies are isolated under `work/brand`; the Python package does not depend on them.

SVG exports embed Excalifont, Nunito and Cascadia font subsets, so they render the same
on GitHub and the documentation site. Review screenshots of the banner (900 px and 390 px,
on a dark page), both diagrams and the logo at 32–180 px are written to `work/brand`.

For a responsive GitHub README, use:

```html
<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/brand/banner-mobile.svg">
  <img src="docs/assets/brand/banner.svg" width="100%"
       alt="earth-embedding: imagery, places and products become Earth embeddings in one Python call">
</picture>
```

## Credits and licensing

Original earth-embedding artwork is distributed under the repository's Apache-2.0 license.
The export engine is [Excalidraw](https://github.com/excalidraw/excalidraw) (MIT).
Excalifont is copyright © 2024 Excalidraw, designed by Ján Filípek / DizajnDesign
and derived from Virgil by Your Own Font Foundry. Nunito is copyright 2014 The Nunito
Project Authors. Cascadia is by Microsoft. All three are distributed under the
SIL Open Font License 1.1; these licenses apply to the embedded font data, independently
of the artwork. Complete notices are retained locally:
[Excalifont OFL](licenses/Excalifont-OFL.txt), [Nunito OFL](licenses/Nunito-OFL.txt),
[Cascadia OFL](licenses/Cascadia-OFL.txt), and [font provenance](licenses/font-provenance.json).

Palette: paper `#faf8f1`, ink `#173f40`, teal `#267b72`, deep teal `#1f5f58`,
sage `#d8ece0`, terracotta `#d98950`, muted text `#57706b`.
