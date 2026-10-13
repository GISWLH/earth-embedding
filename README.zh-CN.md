<div align="center">
  <img src="docs/assets/earth-embedding-logo.svg" width="96" alt="Earth Embedding 标志">

# Earth Embedding

**以统一的 Python 接口，连接遥感影像、地理位置与预计算嵌入产品。**

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![License](https://img.shields.io/badge/Code-Apache--2.0-267b72)](LICENSE)
[![Models](https://img.shields.io/badge/Catalog-22%20adapters-267b72)](docs/models.md)
[![Validation](https://img.shields.io/badge/Validation-evidence%20%26%20limits-d98950)](docs/validation.md)
[![Tests](https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml/badge.svg)](https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml)

[开始使用](#安装) · [模型目录](#模型目录) · [完整文档](docs/index.md) · [验证记录](docs/validation.md) · [参与贡献](CONTRIBUTING.md)

</div>

> **项目来源。** Earth Embedding 基于 Dingqi Ye 及贡献者开发的 [CyberGIS rs-embed](https://github.com/cybergis/rs-embed) 二次开发并独立维护，保留 Apache-2.0 许可证及原作者署名。原项目的 API、适配器和工程框架是本项目的重要基础。[原 rs-embed 论文](https://arxiv.org/abs/2602.23678)与我们的研究论文是不同工作；详见[来源与致谢](docs/provenance.md)。

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/earth-embedding-hero-mobile.svg">
  <img src="docs/assets/earth-embedding-hero.svg" width="100%" alt="影像编码器、位置编码器和预计算产品通过 Earth Embedding 接入地理空间分析流程。">
</picture>

## 为什么使用 Earth Embedding？

不同遥感模型对输入波段、预处理、空间尺度、时间序列和数据访问方式有不同要求。Earth Embedding 用可复用接口获取特征，同时明确保留这些差异。你可以从已有影像、经纬度列表或预计算产品出发，得到用于下游分析的嵌入值及来源元数据。

- **三类入口：**按照用户获得的发布对象，区分影像编码器、位置编码器和预计算嵌入产品。
- **22 个适配器条目：**16 种影像配置、3 种位置编码器、3 种预计算产品。条目包含可选集成；真实运行状态以验证报告为准。
- **统一位置接口：**SatCLIP、GeoCLIP 和可选 Esri Global Location Encoder 均使用 `[经度, 纬度]` 输入。
- **直接读取 AlphaEarth：**通过 Google 官方存储桶索引查找瓦片、采样 64 维向量，无需 Earth Engine 身份验证。
- **可复用输出：**池化向量、模型支持的空间网格、批量提取、导出和来源元数据。
- **衔接论文研究：**将发布对象分类、全球评估设计和武汉诊断整理为可阅读的研究说明，并与接口测试分开记录。

新入口为 `import earth_embedding` 和 `earth-embedding` 命令；原 `rs_embed` 导入路径及 `rs-embed` 命令仍保留兼容。

## 安装

使用 Python 3.12 或更新版本。当前从 Git 仓库安装，下面的指令不依赖 PyPI 上存在同名发布包。

```bash
python -m pip install "earth-embedding @ git+https://github.com/GISWLH/earth-embedding.git"
```

需要可选功能或参与开发时：

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[location,aef]"
```

| 依赖选项 / 环境 | 适用场景 |
| --- | --- |
| 基础安装 | 核心 API 及 `pyproject.toml` 声明的依赖 |
| `.[location]` | 安装 GeoCLIP 官方 Python 包；SatCLIP 使用项目包含的适配器和运行时代码 |
| `.[aef]` | 通过 Rasterio / PyArrow 读取 AEF COG 和 Parquet 索引 |
| `.[benchmark]` | 运行空间留出评估示例所需的 Scikit-learn 等依赖 |
| `.[terratorch]` | TerraMind 及当前 Prithvi 集成所需的 TerraTorch |
| `.[dev,full,location,aef,benchmark]` | 开发检查及上述可选集成 |
| Esri 官方支持的 ArcGIS 环境 | Esri GLE，需另行配置兼容的深度学习依赖并遵守相关条款 |

请为硬件安装合适的 PyTorch。首次使用模型可能下载权重，部分影像模型需要较多内存或显存。查看目录与接口说明无需运行推理：

```bash
earth-embedding models --json
earth-embedding describe satclip
```

使用 Earth Engine 影像或产品路径时，先执行 `earthengine authenticate`，并配置具备访问资格的 Cloud 项目，必要时设置 `EE_PROJECT`。下面的位置查询及 GCS 直接采样不初始化 Earth Engine。

## 三个快速示例

### 1. 经纬度转嵌入

无需下载影像或选择日期。坐标必须为 WGS84 角度制，顺序为 **`[经度, 纬度]`**；单点也需嵌套在二维数组中。

```python
from earth_embedding import get_location_embeddings

locations = [[114.41, 30.52], [139.76, 35.68], [-0.12, 51.51]]
result = get_location_embeddings("satclip", locations, device="cpu")
print(result.data.shape)  # (3, 256)
print(result.meta)

# 先安装 .[location]；GeoCLIP 为每个位置返回 512 维特征。
geoclip = get_location_embeddings("geoclip", locations, device="cpu")
```

配置好受支持的 ArcGIS 环境后，同一接口可使用 `"esri_gle"`。Esri 软件及模型适用独立条款；适配器已注册并不代表每个环境都通过了真实推理。请阅读 [Esri GLE 配置](docs/models/esri_gle.md)和[验证报告](docs/validation.md)。

位置嵌入表示模型学到的地理先验。对同一位置改变查询年份，不会产生新的地表观测。

### 2. 按地点和时间提取影像嵌入

地理查询 API 获取配置的影像并运行模型。此例需要有效的 Earth Engine 访问、模型权重及运行时依赖。

```python
from earth_embedding import PointBuffer, TemporalSpec, OutputSpec, get_embedding

result = get_embedding(
    "remoteclip",
    spatial=PointBuffer(lon=114.41, lat=30.52, buffer_m=320),
    temporal=TemporalSpec.range("2021-05-01", "2021-10-31"),
    output=OutputSpec.pooled(),
    device="cpu",
)
print(result.data.shape)
print(result.meta)
```

已有影像时，可调用 `get_image_embedding(model, pixels, spatial=..., temporal=..., sensor=..., device=...)`，直接输入 CHW 或 TCHW 数组，无需再次获取影像。必须满足模型的波段顺序、传感器数值单位及时间要求，不能将任意 RGB 数组送入所有模型。详见 [API](docs/api.md) 与[模型说明](docs/models.md)。

### 3. 直接读取 Google Cloud Storage 中的 AlphaEarth

先下载一次官方全球覆盖索引，再按区域与年份筛选。建议使用体积较小的 Parquet 索引；下载前可以检查文件大小。

```bash
curl -L -o aef_index.parquet https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.parquet
```

```python
from earth_embedding import BBox, find_aef_tiles, sample_aef

tiles = find_aef_tiles(
    "aef_index.parquet",
    spatial=BBox(114.40, 30.51, 114.42, 30.53),
    year=2021,
)
result = sample_aef([[114.41, 30.52]], tiles=tiles)
print(result.data.shape)  # (1, 64)
print(result.meta["source_for_point"])
```

采样器处理坐标系转换、COG 按字节范围读取、有符号 int8 反量化和无效值。请仅传入同一年份的候选瓦片。默认遇到无覆盖或掩膜点会报错；设置 `strict=False` 可保留这些行为 NaN。网络错误仍明确抛出。

Google [官方 GCS 文档](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme)说明：自 2026 年 7 月起，存储桶采用提供方付费，当前年度范围为 2017—2025。更多索引格式、文件清单、Earth Engine 路径和必须保留的数据署名见[数据访问指南](docs/data-access.md)。本项目不分发 AEF 模型权重。

## 模型目录

分类依据发布对象和实际评估配置的输入契约。架构、分辨率、训练信号和评估资格是独立属性。目录收录代表已提供集成入口，不能直接推断当前数据、权重及本机运行环境均可用。

| 类别 | 模型 ID | 模型 / 发布对象 | 输入或访问方式 |
| --- | --- | --- | --- |
| A1 · RGB | `remoteclip` | [RemoteCLIP](docs/models/remoteclip.md) | 三通道光学影像 |
| A1 · RGB | `satmae` | [SatMAE](docs/models/satmae.md) | RGB 配置 |
| A1 · RGB | `satmaepp` | [SatMAE++](docs/models/satmaepp.md) | RGB 配置 |
| A1 · RGB | `scalemae` | [Scale-MAE](docs/models/scalemae.md) | RGB 与空间尺度 |
| A1 · RGB | `wildsat` | [WildSAT](docs/models/wildsat.md) | RGB，骨干网络取决于配置 |
| A2 · 固定波段 | `satmaepp_s2_10b` | [SatMAE++ Sentinel-2](docs/models/satmaepp.md) | 指定顺序的 10 波段 |
| A2 · 固定波段 | `prithvi` | [Prithvi-EO-2.0](docs/models/prithvi.md) | 当前适配器的六波段配置 |
| A2 · 固定波段 | `terramind` | [TerraMind](docs/models/terramind.md) | 当前配置使用 Sentinel-2 路径 |
| A2 · 固定波段 | `terrafm` | [TerraFM](docs/models/terrafm.md) | 当前配置使用 Sentinel-2 路径 |
| A2 · 固定波段 | `satvision` | [SatVision-TOA](docs/models/satvision.md) | 14 通道 MODIS TOA，空间支持较粗 |
| A3 · 通道自适应 | `dofa` | [DOFA](docs/models/dofa.md) | 光谱通道与波长 |
| A3 · 通道自适应 | `fomo` | [FoMo](docs/models/fomo.md) | 模型指定的通道标识 |
| A3 · 通道自适应 | `thor` | [THOR](docs/models/thor.md) | 模型指定的波段及模式元数据 |
| A4 · 多时相 | `galileo` | [Galileo](docs/models/galileo.md) | 带日期的 Sentinel-2 序列 |
| A4 · 多时相 | `anysat` | [AnySat](docs/models/anysat.md) | 带日期的 Sentinel-2 序列 |
| A4 · 多时相 | `agrifm` | [AgriFM](docs/models/agrifm.md) | 带日期的 Sentinel-2 序列 |
| B · 位置编码器 | `satclip` | [SatCLIP](docs/models/satclip.md) | 经纬度，256 维 |
| B · 位置编码器 | `geoclip` | [GeoCLIP](docs/models/geoclip.md) | 经纬度，512 维，需要可选包 |
| B · 位置编码器 | `esri_gle` | [Esri Global Location Encoder](docs/models/esri_gle.md) | 经纬度，256 维，需要可选授权运行时 |
| C1 · 网格产品 | `gse` | [Google Satellite Embedding / AEF](docs/models/gse.md) | 10 m 年度产品，64 维；GEE 或独立 GCS 辅助接口 |
| C1 · 网格产品 | `tessera` | [TESSERA](docs/models/tessera.md) | 10 m 年度产品，GeoTessera 访问或缓存 |
| C1 · 网格产品 | `copernicus` | [Copernicus-Embed-025deg](docs/models/copernicus.md) | 0.25° 预计算网格 |

分类体系还包括 **C2 采样型嵌入集合**，但当前 22 个条目中没有声称实现 C2 适配器。同一模型谱系的权重与预计算产品可以属于不同类别。

## 可复用工作流

| 阶段 | 接口 | 重点检查 |
| --- | --- | --- |
| 发现模型 | `models --json`、`describe MODEL` | 输入条件、输出类型、可选依赖 |
| 检查影像 | `inspect_provider_patch(...)` | 覆盖、波段、数值、形状与获取时间 |
| 提取影像特征 | `get_embedding(...)`、`get_image_embedding(...)` | 数据提供方或本地输入、预处理 |
| 提取位置特征 | `get_location_embeddings(...)` | WGS84 经纬度顺序、权重版本、设备 |
| 读取 AEF | `find_aef_tiles(...)`、`sample_aef(...)` | 年份、覆盖、CRS、无效值与来源 |
| 扩展提取规模 | `get_embeddings_batch(...)`、`export_batch(...)` | 一致配置、缓存、元数据及失败记录 |
| 下游评估 | 自选估计器与空间划分 | 标签、泄漏、空间支持与不确定性 |

结果包含 `.data` 和 `.meta`，建议同时保存。不同编码器的特征维数与空间输出能力不同，统一接口不代表不同模型的向量可以直接混合比较。

## 应用与可执行评估

可用于地表覆盖分类，建筑、植被与水体比例回归，支持密集输出时的水体分割，同一嵌入空间内的相似性检索，以及用于分析地理先验的位置基线。年度产品还能支持时间一致的重复查询。这些是基于特征构建的下游任务，并非所有适配器自带的预测头。

[评估示例](examples/evaluate_embeddings.py)使用已有特征，不下载影像。元数据 CSV 需包含 `sample_id,target,split,spatial_group`；每个 NPZ 包含 `X` 和 `sample_id`。`split` 为 `train` / `test`，两组的空间分组必须互不重叠。

```bash
python -m pip install -e ".[benchmark]"
python examples/evaluate_embeddings.py --metadata metadata.csv --features satclip=satclip.npz geoclip=geoclip.npz --task classification --out evaluation.json
```

示例按样本 ID 对齐所有模型的共同有效样本，仅用训练集拟合标准化与线性模型，并记录样本及输入哈希。回归任务使用 `--task regression`。请自行提供有效的空间划分；此示例不复现论文最终分数。

## 从论文研究到可复用软件

论文工作推动了发布对象分类、可比较的输入输出契约和评估来源记录。冻结的论文基准包含 **20 个系统：A16 + B1（SatCLIP）+ C3**。软件增加 GeoCLIP 与 Esri GLE 后共有 **22 个适配器**，这不自动扩大论文已经评估的集合。

修订后的主实验采用全球分布的 **640 m** 空间单元。武汉 **567 / 2,173 瓦片**材料分别保留其局部与历史诊断范围，不能替代全球主实验。分类、比例回归和适用的密集输出任务需要空间留出划分与匹配的空间支持；SatVision 与 Copernicus-Embed 即使不满足某项受控比较条件，也保留其分类。

详见[研究范围与证据边界](docs/research.md)。论文仍在开发中，仓库不声称 RSE 已接收、最终榜单已确定，或冒烟测试已经证明科学优势。

## 验证状态与限制

[验证报告](docs/validation.md)区分回归测试、真实模型推理和在线数据访问，并记录日期、环境、输出形状与未解决问题。直接 AEF 路径已有[武汉 2021 年真实采样记录](docs/validation/aef-gcs-20261013.json)；单点成功不等于全球覆盖或下游精度已经验证。

数据提供方可能要求身份验证、配额或条款确认；部分模型需要专门环境和大型权重。Esri GLE 依赖独立官方运行时，位置编码器没有时间观测，粗分辨率产品也不会因重采样变成等价的 10 m 嵌入。设计比较前请阅读[限制说明](docs/limitations.md)。

## 文档导航

| 入门 | 深入使用 |
| --- | --- |
| [快速开始](docs/quickstart.md) | [API 参考](docs/api.md) |
| [模型目录](docs/models.md) | [输入输出概念](docs/concepts.md) |
| [AlphaEarth 数据访问](docs/data-access.md) | [批量提取工作流](docs/workflows.md) |
| [研究范围](docs/research.md) | [验证证据](docs/validation.md) |
| [示例与 Notebook](examples/) | [新增适配器](docs/extending.md) |
| [项目来源](docs/provenance.md) | [更新日志](CHANGELOG.md) |

头图和标志使用原生 Excalidraw 手绘元素，提供可编辑源文件、SVG 和 PNG。见[设计源文件与重建说明](docs/assets/earth-embedding-brand.md)。

## 参与贡献

欢迎明确输入契约的新模型集成、可复现的故障报告、可执行示例、数据访问修复，以及中英日文档改进。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，或[提交 Issue](https://github.com/GISWLH/earth-embedding/issues)，附上官方来源、许可证、权重及具体用途。

后续方向包括更多环境验证、已有影像的可复现实例、更多预计算产品访问方式和有充分文档的 C2 集成。这些是开发方向，不代表已经实现。

## 引用、致谢与许可证

引用本扩展时，请使用仓库地址及实际使用的提交或版本；[CITATION.cff](CITATION.cff)提供机器可读元数据。使用原框架时也请引用原 rs-embed 论文，并引用所用模型和数据的原始论文。我们的研究论文将在具有公开书目记录后添加独立引用。

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

感谢 rs-embed 贡献者、各模型作者，以及 Google Earth Engine、Google / Google DeepMind、TorchGeo、GeoTessera、TerraTorch、rshf、Microsoft SatCLIP、GeoCLIP、Esri 和地球观测社区。集成不表示这些团队为本项目背书。

库代码采用 [Apache-2.0](LICENSE)，[NOTICE](NOTICE)保留上游署名。第三方代码、权重、数据与字体遵循各自许可证；AlphaEarth 数据采用 CC-BY-4.0，Esri 软件及模型适用独立条款。详见[来源与许可](docs/provenance.md)。
