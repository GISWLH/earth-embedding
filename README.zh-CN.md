<p align="center">
  <picture>
    <source media="(max-width: 760px)" srcset="docs/assets/brand/banner-mobile.svg">
    <img src="docs/assets/brand/banner.svg" width="100%" alt="earth-embedding：影像、位置与嵌入产品，一次 Python 调用得到地球嵌入">
  </picture>
</p>

<p align="center">
  <a href="README.md">English</a> · <b>简体中文</b> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="pyproject.toml"><img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-267b72"></a>
  <a href="#模型目录"><img alt="22 models" src="https://img.shields.io/badge/Catalog-22%20models-267b72"></a>
  <a href="https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml/badge.svg"></a>
  <a href="https://giswlh.github.io/earth-embedding/"><img alt="Docs" src="https://img.shields.io/badge/Docs-online-267b72"></a>
  <a href="docs/model-resources.md"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-models%20%26%20data-FFD21E"></a>
</p>

<p align="center">
  <a href="#安装">安装</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#结果展示">结果展示</a> ·
  <a href="#真实数据教程">真实数据教程</a> ·
  <a href="#模型目录">模型目录</a> ·
  <a href="https://giswlh.github.io/earth-embedding/">在线文档</a> ·
  <a href="#引用">引用</a>
</p>

**Earth Embedding** 用一个 Python 接口，从三类地球表征模型中获取嵌入向量及其来源元数据。
选定地点、时间窗口和输出形式，只需更换模型名称：

```python
from earth_embedding import PointBuffer, TemporalSpec, OutputSpec, get_embedding

spatial = PointBuffer(lon=114.41, lat=30.52, buffer_m=640)
temporal = TemporalSpec.range("2021-05-01", "2021-10-31")

emb = get_embedding("prithvi", spatial=spatial, temporal=temporal, output=OutputSpec.grid())
gle = get_embedding("esri_gle", spatial=spatial, output=OutputSpec.grid(), grid_step_m=80)
```

| 影像编码器 · 16 | 位置编码器 · 3 | 预计算产品 · 3 |
| :-- | :-- | :-- |
| 影像 + 时间窗口 → 特征。RemoteCLIP、SatMAE、Prithvi-EO-2.0、TerraMind、DOFA、THOR、Galileo、AnySat 等。 | 经纬度 → 特征，CPU 即可运行，无需影像。SatCLIP、GeoCLIP、Esri GLE。 | 读取已发布的嵌入。AlphaEarth / Google Satellite Embedding（支持直接读取 GCS）、TESSERA、Copernicus-Embed。 |

- **统一地理接口：**`get_embedding`、`compare_embeddings` 与批量导出共用 `spatial` / `temporal` / `output` 规格。
- **真实且可校验的示例：**随包附带 SHA-256 校验的湾区数据，笔记本 CPU 即可离线运行。
- **明确的输入输出契约：**每个结果都包含 `.data` 和 `.meta`（模型、来源、日期、预处理），不掩盖空间支持差异。
- **向后兼容：**原有 `rs_embed` 导入路径与 `rs-embed` 命令继续可用。

> **项目来源。** Earth Embedding 基于 Dingqi Ye 及贡献者开发的
> [CyberGIS rs-embed](https://github.com/cybergis/rs-embed) 独立扩展与维护，保留 Apache-2.0
> 许可证、API 与适配器。详见[来源与致谢](#来源与致谢)。

## 安装

需要 Python 3.12+。从本仓库安装（不假设 PyPI 上已有发布包）：

```bash
python -m pip install "earth-embedding @ git+https://github.com/GISWLH/earth-embedding.git"
```

运行教程、使用可选集成或参与开发时，克隆仓库并安装扩展依赖：

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[demo,location,aef]"
```

<details>
<summary><b>可选依赖</b>与 Earth Engine 配置</summary>

| 依赖选项 | 适用场景 |
| --- | --- |
| `.[demo]` | 绘图、线性探针及执行导览 Notebook |
| `.[location]` | GeoCLIP 官方包；SatCLIP 与 Esri GLE 使用包内运行时 |
| `.[aef]` | 通过 Rasterio / PyArrow 直接采样 AlphaEarth COG 并读取 Parquet 索引 |
| `.[benchmark]` | 空间留出评估示例所需的 Scikit-learn 与 SciPy |
| `.[terratorch]` | TerraMind 所需的 TerraTorch；Prithvi 使用包内运行时 |
| `.[dev,full,location,aef,benchmark]` | 开发检查及全部可选集成 |

请为硬件安装合适的 PyTorch。首次使用会下载权重，大型影像编码器需要较多内存。查看模型目录不会运行推理：

```bash
earth-embedding models --json
earth-embedding describe satclip
```

使用 Earth Engine 的影像和产品路径需要执行 `earthengine authenticate`，并配置具备访问资格的
Cloud 项目（必要时设置 `EE_PROJECT`）。位置编码器和直接读取 AlphaEarth GCS 不会初始化 Earth Engine。

</details>

## 快速开始

### 经纬度 → 嵌入

无需影像或日期。输入为 WGS84 角度，顺序为 **`[经度, 纬度]`**。

```python
from earth_embedding import get_location_embeddings

locations = [[-122.42, 37.77], [139.76, 35.68], [-0.12, 51.51]]
satclip = get_location_embeddings("satclip", locations, device="cpu")  # (3, 256)
esri = get_location_embeddings("esri_gle", locations, device="cpu")   # (3, 256), ~3.7 MB weights
geoclip = get_location_embeddings("geoclip", locations, device="cpu") # (3, 512), needs .[location]
print(satclip.data.shape, satclip.meta)
```

Esri GLE 直接用 PyTorch 加载官方权重，无需 ArcGIS 或 ArcPy。下载文件通过固定 SHA-256 校验，
也可传入本地 `.dlpk` 或 `satclip.pth` 离线使用；Esri 模型条款另行适用（[配置说明](docs/models/esri_gle.md)）。
位置嵌入是模型学到的地理先验：改变年份不会产生新的观测。

### 地点 + 时间 → 影像嵌入

```python
from earth_embedding import PointBuffer, TemporalSpec, OutputSpec, get_embedding

result = get_embedding(
    "remoteclip",
    spatial=PointBuffer(lon=-122.42, lat=37.77, buffer_m=320),
    temporal=TemporalSpec.range("2021-05-01", "2021-10-31"),
    output=OutputSpec.pooled(),
    device="cpu",
)
print(result.data.shape, result.meta)
```

该路径通过 Earth Engine 获取影像，并需要模型权重与运行时依赖。已有影像时，可调用
`get_image_embedding(model, pixels, spatial=..., temporal=..., sensor=..., device=...)`，输入
CHW 或 TCHW 数组，但必须满足适配器的波段顺序与数值单位（[API](docs/api.md)、[模型说明](docs/models.md)）。

### 直接从 Cloud Storage 读取 AlphaEarth

```bash
curl -L -o aef_index.parquet https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.parquet
```

```python
from earth_embedding import BBox, find_aef_tiles, sample_aef

tiles = find_aef_tiles("aef_index.parquet", spatial=BBox(-122.43, 37.76, -122.41, 37.78), year=2021)
result = sample_aef([[-122.42, 37.77]], tiles=tiles)
print(result.data.shape, result.meta["source_for_point"])  # (1, 64)
```

采样器处理坐标系转换、COG 按字节范围读取、int8 反量化与无效值；无覆盖时默认报错，可设
`strict=False` 保留为 NaN。Google [官方 GCS 文档](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme)
说明自 2026 年 7 月起为提供方付费，年度覆盖 2017—2025；索引与署名要求见[数据访问](docs/data-access.md)。

## 结果展示

### 22 个模型，同一区域

![同一武汉区域的 Sentinel-2 参考影像与 22 个模型配置](docs/assets/comparison/all-models.webp)

影像编码器、位置编码器和预计算产品同图展示。每个面板独立计算 PCA 颜色并保留原生空间支持，
同色不代表同类特征或类别；这是定性展示，不是排名。影像与产品面板复用已验证的武汉历史输出
（日期不同，图中已标注），位置面板为新推理结果。[输入与复现](docs/tutorials/model-comparison.md)。

```python
from earth_embedding import compare_embeddings, plot_embedding_comparison

comparison = compare_embeddings(
    ["prithvi", "dofa", "remoteclip", "satclip", "geoclip", "esri_gle"],
    spatial=spatial, temporal=temporal, output=OutputSpec.grid(),
    model_options={m: {"grid_step_m": 80} for m in ("satclip", "geoclip", "esri_gle")},
    on_error="record",  # keep successful panels; show each failure explicitly
)
plot_embedding_comparison(comparison, columns=3).savefig("comparison.png", dpi=180)
```

`models=None` 选择整个目录。[`examples/compare_models.py`](examples/compare_models.py) 会自动为年度产品设置年份，
并保存对比图、特征数组和运行报告（`--models satclip geoclip esri_gle --device cpu` 无需影像或 Earth Engine）。

### 位置编码器的两个尺度

![SatCLIP、GeoCLIP 与 Esri GLE 在全球和武汉坐标网格上的结果](docs/assets/comparison/location-encoders.png)

位置编码器只接收经纬度，图中模式是学到的地理先验。可通过 `spatial` 和 `grid_step_m` 调整区域与采样间距。

<!-- REAL_DEMOS_START -->
## 真实数据教程

三个 CPU 可运行示例，无需 Earth Engine 登录。随包附带经 SHA-256 校验的旧金山湾区
**完整 72 × 88 网格**：AlphaEarth（AEF）2021 官方 **1,280 米**金字塔网格，约 92 × 113 公里，
共 6,336 个网格，2.3 MB。安装：`python -m pip install -e ".[demo,aef]"`。

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/brand/demo-workflow-mobile.svg">
  <img src="docs/assets/brand/demo-workflow.svg" width="100%" alt="区域或坐标到嵌入再到地图；特征与标签经空间分折、线性分类器得到地图与指标">
</picture>

**1 · AEF 2021 → PCA 空间图**（离线）

```python
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("aef")
colors = pca_colors(data.features)
fig = plot_map(data.samples, colors, title="San Francisco Bay Area · AEF 2021 · PCA RGB")
fig.savefig("aef-pca.png", dpi=160)
```

**2 · Esri GLE → 位置嵌入地图**（仅首次下载约 3.7 MB 权重）

```python
from earth_embedding import get_location_embeddings
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("bayarea")
points = data.samples[["center_lon", "center_lat"]].to_numpy()
gle = get_location_embeddings("esri_gle", points, device="cpu", batch_size=128)
fig = plot_map(data.samples, pca_colors(gle.data), title="San Francisco Bay Area · Esri GLE · PCA RGB")
fig.savefig("esri-gle-pca.png", dpi=160)
```

<table>
  <tr>
    <td width="50%"><img src="docs/assets/demos/aef-pca.png" alt="旧金山湾区 AEF 2021 PCA 地图"></td>
    <td width="50%"><img src="docs/assets/demos/esri-gle-pca.png" alt="相同 6,336 个位置的 Esri GLE PCA 地图"></td>
  </tr>
  <tr>
    <td><b>AEF 2021</b>：来自观测的嵌入，海湾、山脊、城区与三角洲农田清晰分开。</td>
    <td><b>Esri GLE</b>：仅用坐标编码相同网格，呈现平滑的地理先验，没有观测年份。</td>
  </tr>
</table>

RGB 为三个描述性主成分，**不代表地物类别**，两张图的颜色也不可互相比较。`fetch_aef_demo()` 可重新读取官方 GCS。

**3 · 嵌入 + 标签 → 空间留出分类**

```python
from earth_embedding.demo import classify_demo, plot_classification
result = classify_demo()
print({k: result["metrics"][k] for k in ("oa", "macro_f1", "balanced_accuracy")})
fig = plot_classification(result)
fig.savefig("bayarea-classification.png", dpi=160)
```

![湾区 WorldCover 参考、折外预测、错误分布与混淆矩阵](docs/assets/demos/bayarea-classification.png)

| OA | Macro-F1 | Balanced accuracy | 评分 / 隔离带 / 不评分 |
| ---: | ---: | ---: | --- |
| 93.64% | 91.64% | 92.63% | 5,806 / 528 / 2 个裸地网格 |

两折空间验证：仅用西半部拟合的模型预测东半部，反之亦然，因此每个评分网格都有留出预测。
7.68 公里隔离带既不训练也不评分。标签为 ESA WorldCover 2021（建成区、植被、耕地、水体），
模型为标准化 + 类别平衡逻辑回归。这是区域**软件演示**，不是论文基准结果。
[划分、类别数量、数据来源与限制](docs/tutorials/real-demos.md)。

| Notebook | 内容 |
| --- | --- |
| [01 · 第一张嵌入地图](examples/notebooks/01_first_embedding_map.ipynb) | 读取已校验的 AEF 样例并绘制 PCA 地图 |
| [02 · Esri GLE 位置编码](examples/notebooks/02_esri_locations.ipynb) | 分批、缓存并离线复跑位置编码器 |
| [03 · 区域分类](examples/notebooks/03_regional_classification.ipynb) | 两折空间留出、地图与指标 |
| [04 · 导出与复用](examples/notebooks/04_export_and_reuse.ipynb) | 带 ID 的分批导出与安全对齐 |
| [05 · 多模型对比](examples/notebooks/05_compare_models.ipynb) | 三模型 CPU 对比及全目录运行单元 |

所有 Notebook 均保存真实运行输出（[执行记录](docs/validation/demo-notebooks.json)）。
<!-- REAL_DEMOS_END -->

## 工作原理

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/brand/how-it-works-mobile.svg">
  <img src="docs/assets/brand/how-it-works.svg" width="100%" alt="影像编码器、位置编码器和预计算产品通过共享 Python API 连接到制图、检索和下游学习">
</picture>

模型按用户实际获得的发布对象分类：**A** 影像编码器（A1 RGB、A2 固定波段、A3 通道自适应、A4 多时相），
**B** 位置编码器，**C** 预计算产品（C1 网格、C2 采样）。架构、分辨率与训练信号是独立属性。

| 阶段 | 接口 | 重点检查 |
| --- | --- | --- |
| 发现模型 | `earth-embedding models --json`、`describe MODEL` | 输入要求、输出类型、可选依赖 |
| 检查影像 | `inspect_provider_patch(...)` | 覆盖、波段、数值、形状与获取时间 |
| 影像编码 | `get_embedding(...)`、`get_image_embedding(...)` | 数据提供方或本地输入、正确的预处理 |
| 位置编码 | `get_location_embeddings(...)` | WGS84 `[经度, 纬度]`、权重版本、设备 |
| 读取 AEF | `find_aef_tiles(...)`、`sample_aef(...)` | 年份、覆盖、CRS、无效值与来源 |
| 规模化 | `get_embeddings_batch(...)`、`export_batch(...)` | 统一配置、缓存、元数据与失败记录 |
| 评估 | [`examples/evaluate_embeddings.py`](examples/evaluate_embeddings.py) | 空间划分、泄漏、匹配的空间支持 |

请同时保存 `.data` 与 `.meta`。不同模型的特征维度和空间支持不同，统一接口并不意味着不同编码器的向量可以互换。

## 模型目录

| 模型 ID | 类别 | 适配器输入 | 上游 | 权重或产品 |
| --- | --- | --- | --- | --- |
| [`remoteclip`](docs/models/remoteclip.md) | A1 · 影像 | Sentinel-2 RGB | [代码](https://github.com/ChenDelong1999/RemoteCLIP) | [🤗 模型](https://huggingface.co/MVRL/remote-clip-vit-base-patch32) |
| [`satmae`](docs/models/satmae.md) | A1 · 影像 | Sentinel-2 RGB | [代码](https://github.com/sustainlab-group/SatMAE) | [🤗 模型](https://huggingface.co/MVRL/satmae-vitlarge-fmow-pretrain-800) |
| [`satmaepp`](docs/models/satmaepp.md) | A1 · 影像 | Sentinel-2 RGB | [代码](https://github.com/techmn/satmae_pp) | [🤗 模型](https://huggingface.co/MVRL/satmaepp_ViT-L_pretrain_fmow_rgb) |
| [`scalemae`](docs/models/scalemae.md) | A1 · 影像 | Sentinel-2 RGB + 地面分辨率 | [代码](https://github.com/bair-climate-initiative/scale-mae) | [🤗 模型](https://huggingface.co/MVRL/scalemae-vitlarge-800) |
| [`wildsat`](docs/models/wildsat.md) | A1 · 影像 | Sentinel-2 RGB | [代码](https://github.com/cvl-umass/wildsat) | [官方](https://github.com/cvl-umass/wildsat#quickstart) |
| [`satmaepp_s2_10b`](docs/models/satmaepp.md) | A2 · 影像 | Sentinel-2 10 波段 | [代码](https://github.com/techmn/satmae_pp) | [🤗 模型](https://huggingface.co/mubashir04/checkpoint_ViT-L_pretrain_fmow_sentinel) |
| [`prithvi`](docs/models/prithvi.md) | A2 · 影像 | Sentinel-2 6 波段 + 时间/位置 | [代码](https://github.com/NASA-IMPACT/Prithvi-EO-2.0) | [🤗 模型](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-100M-TL) |
| [`terrafm`](docs/models/terrafm.md) | A2 · 影像 | Sentinel-2 12 波段或 Sentinel-1 VV/VH | [代码](https://github.com/mbzuai-oryx/TerraFM) | [🤗 模型](https://huggingface.co/MBZUAI/TerraFM) |
| [`terramind`](docs/models/terramind.md) | A2 · 影像 | Sentinel-2 12 波段 | [代码](https://github.com/IBM/terramind) | [🤗 模型](https://huggingface.co/ibm-esa-geospatial/TerraMind-1.0-small) |
| [`satvision`](docs/models/satvision.md) | A2 · 影像 | 14 通道 MODIS TOA | [代码](https://github.com/nasa-nccs-hpda/pytorch-caney) | [🤗 模型](https://huggingface.co/nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128) |
| [`dofa`](docs/models/dofa.md) | A3 · 影像 | 多光谱影像 + 波长 | [代码](https://github.com/zhu-xlab/DOFA) | [🤗 模型](https://huggingface.co/earthflow/DOFA) |
| [`fomo`](docs/models/fomo.md) | A3 · 影像 | Sentinel-2 12 波段 | [代码](https://github.com/RolnickLab/FoMo-Bench) | [官方](https://github.com/RolnickLab/FoMo-Bench#loading-pretrained-fomo-net) |
| [`thor`](docs/models/thor.md) | A3 · 影像 | Sentinel-2 10 波段 | [代码](https://github.com/FM4CS/THOR) | [🤗 模型](https://huggingface.co/FM4CS/THOR-1.0-base) |
| [`galileo`](docs/models/galileo.md) | A4 · 影像 | Sentinel-2 10 波段时间序列 | [代码](https://github.com/nasaharvest/galileo) | [🤗 模型](https://huggingface.co/nasaharvest/galileo) |
| [`anysat`](docs/models/anysat.md) | A4 · 影像 | Sentinel-2 10 波段时间序列 | [代码](https://github.com/gastruc/anysat) | [🤗 模型](https://huggingface.co/g-astruc/AnySat) |
| [`agrifm`](docs/models/agrifm.md) | A4 · 影像 | Sentinel-2 10 波段时间序列 | [代码](https://github.com/flyakon/AgriFM) | [官方](https://github.com/flyakon/AgriFM#model-training) |
| [`satclip`](docs/models/satclip.md) | B · 位置 | 经纬度，256 维 | [代码](https://github.com/microsoft/satclip) | [🤗 模型](https://huggingface.co/microsoft/SatCLIP-ViT16-L40) |
| [`geoclip`](docs/models/geoclip.md) | B · 位置 | 经纬度，512 维 | [代码](https://github.com/VicenteVivan/geo-clip) | [官方](https://github.com/VicenteVivan/geo-clip#usage-pre-trained-location-encoder) |
| [`esri_gle`](docs/models/esri_gle.md) | B · 位置 | 经纬度，256 维 | [文档](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm) | [官方](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3) |
| [`gse`](docs/models/gse.md) | C1 · 产品 | 年度 Google Satellite Embedding，10 m，64 维 | [目录](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) | [官方](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) |
| [`tessera`](docs/models/tessera.md) | C1 · 产品 | GeoTessera 发布瓦片，10 m | [代码](https://github.com/ucam-eo/geotessera) | [官方](https://github.com/ucam-eo/geotessera#dataset-versions-and-variants) |
| [`copernicus`](docs/models/copernicus.md) | C1 · 产品 | 0.25° 嵌入网格 | [来源](https://huggingface.co/datasets/wangyi111/Copernicus-Embed-025deg) | [🤗 数据集](https://huggingface.co/datasets/torchgeo/copernicus_embed) |

以上为上游资源，本项目不重新分发权重（[打包形式、默认版本与条款](docs/model-resources.md#which-artifact-am-i-opening)）。
适配器代表集成入口，不保证数据访问或在你的环境中运行成功，见[验证报告](docs/validation.md)。
分类体系还包括 **C2 采样型集合**，当前尚未声称实现 C2 适配器。

## 研究背景与限制

论文工作推动了发布对象分类、可比较的输入输出契约和评估来源记录。冻结的论文基准包含
**20 个系统（A16 + B1 SatCLIP + C3）**；GeoCLIP 与 Esri GLE 是之后的软件集成，不扩大该研究的评估集合。
论文仍在准备中，本仓库不声称论文已被接收、存在最终榜单或科学排名（[研究范围](docs/research.md)）。

数据提供方可能要求身份验证、配额或条款确认；部分模型需要大型权重。位置编码器没有时间观测，
粗分辨率产品重采样后也不等价于 10 m 场。设计比较前请阅读[限制说明](docs/limitations.md)。

## 文档导航

| 入门 | 深入 |
| --- | --- |
| [快速开始](docs/quickstart.md) | [API 参考](docs/api.md) |
| [模型说明](docs/models.md) · [资源](docs/model-resources.md) | [输入输出概念](docs/concepts.md) |
| [真实数据教程](docs/tutorials/real-demos.md) | [批量提取工作流](docs/workflows.md) |
| [多模型对比](docs/tutorials/model-comparison.md) | [验证证据](docs/validation.md) |
| [AlphaEarth 数据访问](docs/data-access.md) | [新增适配器](docs/extending.md) |
| [示例](examples/) | [更新日志](CHANGELOG.md) |

## 参与贡献

欢迎明确输入契约的模型适配器、可复现的故障报告、小型可执行示例、数据访问修复，以及中英日文档改进。
请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，或[提交 Issue](https://github.com/GISWLH/earth-embedding/issues)，
附上官方来源、许可证、权重和具体用途。头图、标志与示意图均为可编辑的 Excalidraw 源文件（[设计说明](docs/assets/brand/README.md)）。

## 来源与致谢

Earth Embedding 是 Dingqi Ye 及贡献者创建的 [CyberGIS rs-embed](https://github.com/cybergis/rs-embed)
的独立维护扩展，保留其 Apache-2.0 许可证，并感谢其 API、适配器与工程基础。
[原 rs-embed 论文](https://arxiv.org/abs/2602.23678)描述 rs-embed；我们的论文与扩展是独立工作（[来源说明](docs/provenance.md)）。

感谢 rs-embed 贡献者、各模型与数据集作者，以及 Google Earth Engine、Google / Google DeepMind、TorchGeo、
GeoTessera、TerraTorch、rshf、Microsoft SatCLIP、GeoCLIP、Esri 和地球观测社区。集成不代表背书。

## 引用

请引用本软件并注明使用的提交或版本（[CITATION.cff](CITATION.cff)）；使用原框架时引用 rs-embed 论文，
并引用分析中所用模型与数据的原始文献。

```bibtex
@article{ye2026modelplacetimeremote,
  title={Any Model, Any Place, Any Time: Get Remote Sensing Foundation Model Embeddings On Demand},
  author={Ye, Dingqi and Kiv, Daniel and Hu, Wei and Shi, Jimeng and Wang, Shaowen},
  year={2026},
  eprint={2602.23678},
  archivePrefix={arXiv},
  url={https://arxiv.org/abs/2602.23678}
}
```

## 许可证

库代码采用 [Apache-2.0](LICENSE)，[NOTICE](NOTICE) 保留上游署名。第三方代码、模型权重、数据与字体遵循各自许可证：
AlphaEarth 数据与 ESA WorldCover 均为 CC-BY-4.0，Esri 软件及模型适用独立条款。详见[来源与许可](docs/provenance.md)。
