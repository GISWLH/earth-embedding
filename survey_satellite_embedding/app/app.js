const DEFAULT_CENTER = [30.52, 114.41];
const DEFAULT_ZOOM = 11;
const DATA_URL = "../data/model_dossier.json";
const ROI_URL = "../experiments/roi_wuhan_east_lake.geojson";

const taskNotes = {
  classification:
    "Use pooled embeddings as the mandatory baseline. Compare linear probe and k-NN under the same train/validation/test split.",
  segmentation:
    "Prioritize models that expose dense token grids. For pooled-only models, keep a coarser tile-level segmentation baseline.",
  regression:
    "Use ridge regression over pooled embeddings to predict built-up or vegetation fraction aggregated from label rasters.",
  retrieval:
    "Best suited to vision-language or multimodal models. Start with qualitative text-region queries before adding Recall@K.",
};

const state = {
  dossier: null,
  roiGeoJson: null,
  selectedModel: null,
  selectedTask: "classification",
  roiSizeKm: 10,
  roiCenter: DEFAULT_CENTER,
  map: null,
  marker: null,
  roiRectangle: null,
  pilotLayer: null,
};

const el = {
  modelSelect: document.getElementById("modelSelect"),
  taskSelect: document.getElementById("taskSelect"),
  roiSize: document.getElementById("roiSize"),
  roiSizeValue: document.getElementById("roiSizeValue"),
  inventorySummary: document.getElementById("inventorySummary"),
  modelSummary: document.getElementById("modelSummary"),
  taxonomyChips: document.getElementById("taxonomyChips"),
  roiSummary: document.getElementById("roiSummary"),
  benchmarkSummary: document.getElementById("benchmarkSummary"),
  taskGuidance: document.getElementById("taskGuidance"),
  apiPreview: document.getElementById("apiPreview"),
  mapStatus: document.getElementById("mapStatus"),
  focusPilot: document.getElementById("focusPilot"),
  resetView: document.getElementById("resetView"),
};

function kmBounds(center, widthKm) {
  const [lat, lon] = center;
  const halfLatDeg = widthKm / 111.32 / 2;
  const lonScale = Math.max(Math.cos((lat * Math.PI) / 180), 0.15);
  const halfLonDeg = widthKm / (111.32 * lonScale) / 2;
  return [
    [lat - halfLatDeg, lon - halfLonDeg],
    [lat + halfLatDeg, lon + halfLonDeg],
  ];
}

function formatValue(value, fallback = "n/a") {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  if (Array.isArray(value)) {
    return value.join(", ");
  }
  return String(value);
}

function createDetail(label, value) {
  const wrap = document.createElement("div");
  wrap.className = "detail-item";

  const labelEl = document.createElement("div");
  labelEl.className = "list-label";
  labelEl.textContent = label;

  const valueEl = document.createElement("div");
  valueEl.className = "detail-value";
  valueEl.textContent = formatValue(value);

  wrap.append(labelEl, valueEl);
  return wrap;
}

function renderInventorySummary() {
  const records = state.dossier.records;
  const families = new Set(records.map((r) => r.review_family).filter(Boolean));
  const modalities = new Set(records.map((r) => r.modality_scope).filter(Boolean));
  el.inventorySummary.textContent =
    `${records.length} models, ${families.size} review families, ${modalities.size} modality groupings.`;
}

function populateModelSelect() {
  const records = [...state.dossier.records].sort((a, b) =>
    a.model_id.localeCompare(b.model_id),
  );
  el.modelSelect.innerHTML = "";
  records.forEach((record) => {
    const option = document.createElement("option");
    option.value = record.model_id;
    option.textContent = `${record.model_id} · ${record.source_publication.year}`;
    el.modelSelect.append(option);
  });
  state.selectedModel = records[0];
  el.modelSelect.value = state.selectedModel.model_id;
}

function renderModelSummary() {
  const record = state.selectedModel;
  el.modelSummary.innerHTML = "";
  el.modelSummary.className = "detail-list";

  const shape = record.benchmark_summary?.shape || [];
  const embDim = shape.length ? shape[shape.length - 1] : "n/a";
  const publication = `${record.source_publication.title} (${record.source_publication.venue} ${record.source_publication.year})`;

  [
    ["Publication", publication],
    ["Authors", record.paper_authors],
    ["Backbone", record.backbone_family],
    ["Resolution", record.stated_resolution],
    ["Temporal semantics", record.time_coverage],
    ["Sensors", record.sensor_support],
    ["Embedding dimension", embDim],
    ["Typical tasks", record.typical_tasks],
  ].forEach(([label, value]) => el.modelSummary.append(createDetail(label, value)));
}

function renderTaxonomyChips() {
  const record = state.selectedModel;
  el.taxonomyChips.innerHTML = "";
  (record.taxonomy_labels || []).filter(Boolean).forEach((label) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = label;
    el.taxonomyChips.append(chip);
  });
}

function renderBenchmarkSummary() {
  const record = state.selectedModel;
  const bench = record.benchmark_summary || {};
  el.benchmarkSummary.innerHTML = "";
  el.benchmarkSummary.className = "detail-list";

  [
    ["Output shape", formatValue(bench.shape)],
    ["Elapsed time", bench.elapsed_s ? `${bench.elapsed_s.toFixed(2)} s` : "n/a"],
    ["Peak GPU memory", bench.peak_mem_mb ? `${bench.peak_mem_mb.toFixed(1)} MB` : "0.0 MB"],
    ["Output modes", record.output_modes],
    ["Adapter", record.adapter_class],
  ].forEach(([label, value]) => el.benchmarkSummary.append(createDetail(label, value)));
}

function renderTaskGuidance() {
  const record = state.selectedModel;
  el.taskGuidance.innerHTML = "";
  el.taskGuidance.className = "detail-list";

  const denseCapable = (record.output_modes || []).includes("grid");
  const retrievalCapable = /vision-language|multimodal/i.test(record.modality_scope || "");

  [
    ["Selected task", state.selectedTask],
    ["Suggested interpretation", taskNotes[state.selectedTask]],
    ["Dense output available", denseCapable ? "yes" : "no"],
    ["Retrieval-friendly", retrievalCapable ? "yes" : "limited"],
  ].forEach(([label, value]) => el.taskGuidance.append(createDetail(label, value)));
}

function renderApiPreview() {
  const [lat, lon] = state.roiCenter;
  const request = {
    model: state.selectedModel.model_id,
    task_lens: state.selectedTask,
    roi_center: {
      lat: Number(lat.toFixed(4)),
      lon: Number(lon.toFixed(4)),
    },
    roi_width_km: state.roiSizeKm,
    temporal_window: ["2021-05-01", "2021-10-31"],
    outputs: state.selectedTask === "segmentation" ? ["pooled", "grid"] : ["pooled"],
  };
  el.apiPreview.textContent = JSON.stringify(request, null, 2);
}

function renderRoiSummary() {
  const [lat, lon] = state.roiCenter;
  const bounds = kmBounds(state.roiCenter, state.roiSizeKm);
  el.roiSummary.innerHTML = "";
  el.roiSummary.className = "detail-list";

  [
    ["Center", `${lat.toFixed(4)}, ${lon.toFixed(4)}`],
    ["Extraction width", `${state.roiSizeKm} km`],
    [
      "Bounds",
      `${bounds[0][0].toFixed(4)}, ${bounds[0][1].toFixed(4)} -> ${bounds[1][0].toFixed(4)}, ${bounds[1][1].toFixed(4)}`,
    ],
    ["Pilot area", "Wuhan East Lake and Tangxun Lake corridor"],
  ].forEach(([label, value]) => el.roiSummary.append(createDetail(label, value)));
}

function updateRoiOverlay() {
  const bounds = kmBounds(state.roiCenter, state.roiSizeKm);
  if (!state.roiRectangle) {
    state.roiRectangle = L.rectangle(bounds, {
      color: "#1f5f58",
      weight: 2,
      fillColor: "#1f5f58",
      fillOpacity: 0.08,
      dashArray: "8 6",
    }).addTo(state.map);
  } else {
    state.roiRectangle.setBounds(bounds);
  }

  if (!state.marker) {
    state.marker = L.circleMarker(state.roiCenter, {
      radius: 7,
      color: "#ba7d38",
      fillColor: "#ba7d38",
      fillOpacity: 0.9,
      weight: 2,
    }).addTo(state.map);
  } else {
    state.marker.setLatLng(state.roiCenter);
  }
}

function refreshPanels() {
  renderModelSummary();
  renderTaxonomyChips();
  renderBenchmarkSummary();
  renderTaskGuidance();
  renderRoiSummary();
  renderApiPreview();
  updateRoiOverlay();
}

function initMap() {
  state.map = L.map("map", {
    zoomControl: true,
    scrollWheelZoom: true,
  }).setView(DEFAULT_CENTER, DEFAULT_ZOOM);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(state.map);

  state.map.on("click", (event) => {
    state.roiCenter = [event.latlng.lat, event.latlng.lng];
    el.mapStatus.textContent =
      `ROI moved to ${event.latlng.lat.toFixed(4)}, ${event.latlng.lng.toFixed(4)}.`;
    refreshPanels();
  });
}

function renderPilotRoi() {
  if (!state.roiGeoJson) {
    return;
  }
  state.pilotLayer = L.geoJSON(state.roiGeoJson, {
    style: {
      color: "#315f93",
      weight: 2,
      fillColor: "#315f93",
      fillOpacity: 0.08,
    },
  }).addTo(state.map);
}

async function loadData() {
  const [dossierResponse, roiResponse] = await Promise.all([fetch(DATA_URL), fetch(ROI_URL)]);
  if (!dossierResponse.ok) {
    throw new Error(`Failed to load dossier JSON: ${dossierResponse.status}`);
  }
  state.dossier = await dossierResponse.json();
  if (roiResponse.ok) {
    state.roiGeoJson = await roiResponse.json();
  }
}

function wireEvents() {
  el.modelSelect.addEventListener("change", (event) => {
    state.selectedModel = state.dossier.records.find((r) => r.model_id === event.target.value);
    refreshPanels();
  });

  el.taskSelect.addEventListener("change", (event) => {
    state.selectedTask = event.target.value;
    refreshPanels();
  });

  el.roiSize.addEventListener("input", (event) => {
    state.roiSizeKm = Number(event.target.value);
    el.roiSizeValue.textContent = `${state.roiSizeKm} km`;
    refreshPanels();
  });

  el.focusPilot.addEventListener("click", () => {
    if (state.pilotLayer) {
      state.map.fitBounds(state.pilotLayer.getBounds(), { padding: [24, 24] });
    }
    state.roiCenter = DEFAULT_CENTER;
    refreshPanels();
  });

  el.resetView.addEventListener("click", () => {
    state.map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
    state.roiCenter = DEFAULT_CENTER;
    refreshPanels();
  });
}

async function main() {
  initMap();
  try {
    await loadData();
    renderPilotRoi();
    renderInventorySummary();
    populateModelSelect();
    wireEvents();
    refreshPanels();
  } catch (error) {
    el.inventorySummary.textContent = error.message;
    el.mapStatus.textContent = "Failed to load local survey assets. Serve this folder over HTTP.";
  }
}

main();
