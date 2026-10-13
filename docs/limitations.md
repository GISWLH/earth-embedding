# Known Limitations

This page lists the main user-facing constraints in the current `0.1.x` implementation.

## API Boundary

`BBox` and `PointBuffer` currently require `crs="EPSG:4326"`. Other CRS inputs are not accepted at the public API boundary.

## Temporal Semantics

Most on-the-fly adapters interpret `TemporalSpec.range(start, end)` as a filter window plus one composite image, not as automatic single-scene selection by acquisition date. Temporal support is also model-specific: for example, `gse` requires `TemporalSpec.year(...)`, and `copernicus` is currently limited to year `2021`.

## Output Semantics

For many ViT-like models, `OutputSpec.grid()` is a token or patch grid rather than guaranteed georeferenced raster space. Treat `grid` as model-internal spatial structure unless the model page says otherwise.

## Dependencies

Different providers and models require different optional packages such as `terratorch`. Missing optional dependencies usually fail only when you actually use the corresponding model path.

## Known Edge Case

Near some Tessera UTM-zone boundaries, fetched tiles may have different CRS or resolution, and strict mosaic can fail. If that happens, try shifting the ROI slightly or using a smaller ROI or window.
