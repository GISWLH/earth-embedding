<p align="center">
  <picture>
    <source media="(max-width: 760px)" srcset="docs/assets/brand/banner-mobile.svg">
    <img src="docs/assets/brand/banner.svg" width="100%" alt="earth-embedding：画像・位置・プロダクトを一度の Python 呼び出しで地球の埋め込みに">
  </picture>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>日本語</b>
</p>

<p align="center">
  <a href="pyproject.toml"><img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-267b72"></a>
  <a href="#モデル一覧"><img alt="22 models" src="https://img.shields.io/badge/Catalog-22%20models-267b72"></a>
  <a href="https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/GISWLH/earth-embedding/actions/workflows/tests.yml/badge.svg"></a>
  <a href="https://giswlh.github.io/earth-embedding/"><img alt="Docs" src="https://img.shields.io/badge/Docs-online-267b72"></a>
  <a href="docs/model-resources.md"><img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-models%20%26%20data-FFD21E"></a>
</p>

<p align="center">
  <a href="#インストール">インストール</a> ·
  <a href="#クイックスタート">クイックスタート</a> ·
  <a href="#ギャラリー">ギャラリー</a> ·
  <a href="#実データチュートリアル">チュートリアル</a> ·
  <a href="#モデル一覧">モデル一覧</a> ·
  <a href="https://giswlh.github.io/earth-embedding/">ドキュメント</a> ·
  <a href="#引用">引用</a>
</p>

**Earth Embedding** は、3 種類の地球表現モデルから埋め込みとその来歴を、ひとつの Python
インターフェースで取得するライブラリです。場所・期間・出力形式を決めたら、モデル名を替えるだけです。

```python
from earth_embedding import PointBuffer, TemporalSpec, OutputSpec, get_embedding

spatial = PointBuffer(lon=114.41, lat=30.52, buffer_m=640)
temporal = TemporalSpec.range("2021-05-01", "2021-10-31")

emb = get_embedding("prithvi", spatial=spatial, temporal=temporal, output=OutputSpec.grid())
gle = get_embedding("esri_gle", spatial=spatial, output=OutputSpec.grid(), grid_step_m=80)
```

| 画像エンコーダー · 16 | 位置エンコーダー · 3 | 事前計算済みプロダクト · 3 |
| :-- | :-- | :-- |
| 画像 + 期間 → 特徴量。RemoteCLIP、SatMAE、Prithvi-EO-2.0、TerraMind、DOFA、THOR、Galileo、AnySat など。 | 経緯度 → 特徴量。CPU で動作し、画像は不要。SatCLIP、GeoCLIP、Esri GLE。 | 公開済みの埋め込みを読み込み。AlphaEarth / Google Satellite Embedding（GCS から直接取得可）、TESSERA、Copernicus-Embed。 |

- **共通の地理 API：**`get_embedding`、`compare_embeddings`、バッチ出力が同じ `spatial` / `temporal` / `output` 仕様を共有します。
- **検証済みの実データ例：**SHA-256 で検証される湾岸データを同梱し、ノート PC の CPU でオフライン実行できます。
- **明示的な契約：**各結果は `.data` と `.meta`（モデル、取得元、日付、前処理）を持ち、空間的な支持範囲の違いを隠しません。
- **互換性：**既存の `rs_embed` インポートと `rs-embed` コマンドも引き続き利用できます。

> **開発の経緯。** Earth Embedding は、Dingqi Ye 氏とコントリビューターによる
> [CyberGIS rs-embed](https://github.com/cybergis/rs-embed) を基に独立して保守される拡張です。
> Apache-2.0 ライセンス、API、アダプターを継承しています。[来歴と謝辞](#来歴と謝辞)をご覧ください。

## インストール

Python 3.12 以降。リポジトリから直接インストールします（PyPI 公開は前提にしません）。

```bash
python -m pip install "earth-embedding @ git+https://github.com/GISWLH/earth-embedding.git"
```

チュートリアル、任意の統合、開発にはクローンして追加依存を入れます。

```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[demo,location,aef]"
```

<details>
<summary><b>追加依存</b>と Earth Engine の設定</summary>

| 追加依存 | 用途 |
| --- | --- |
| `.[demo]` | 描画、線形プローブ、ガイド付き Notebook の実行 |
| `.[location]` | GeoCLIP の公式パッケージ。SatCLIP と Esri GLE は同梱ランタイムを使用 |
| `.[aef]` | Rasterio / PyArrow による AlphaEarth COG の直接サンプリングと Parquet インデックス |
| `.[benchmark]` | 空間ホールドアウト評価例のための Scikit-learn と SciPy |
| `.[terratorch]` | TerraMind 用の TerraTorch。Prithvi は同梱ランタイムを使用 |
| `.[dev,full,location,aef,benchmark]` | 開発用チェックとすべての任意統合 |

PyTorch はハードウェアに合わせて用意してください。重みは初回にダウンロードされ、大きな画像モデルには
十分なメモリが必要です。カタログの確認では推論は実行されません。

```bash
earth-embedding models --json
earth-embedding describe satclip
```

Earth Engine を使う画像・プロダクトの取得には `earthengine authenticate` と、利用資格のある Cloud
プロジェクト（必要に応じて `EE_PROJECT`）が必要です。位置エンコーダーと AlphaEarth の GCS 直接取得は
Earth Engine を初期化しません。

</details>

## クイックスタート

### 経緯度 → 埋め込み

画像も日付も不要です。座標は WGS84 の度単位で、順序は **`[経度, 緯度]`** です。

```python
from earth_embedding import get_location_embeddings

locations = [[-122.42, 37.77], [139.76, 35.68], [-0.12, 51.51]]
satclip = get_location_embeddings("satclip", locations, device="cpu")  # (3, 256)
esri = get_location_embeddings("esri_gle", locations, device="cpu")   # (3, 256), ~3.7 MB weights
geoclip = get_location_embeddings("geoclip", locations, device="cpu") # (3, 512), needs .[location]
print(satclip.data.shape, satclip.meta)
```

Esri GLE は公式の重みを PyTorch で直接実行します。ArcGIS や ArcPy は不要です。ダウンロードは SHA-256
で検証され、ローカルの `.dlpk` や `satclip.pth` でオフライン利用もできます。Esri のモデル利用条件が別途
適用されます（[設定](docs/models/esri_gle.md)）。位置埋め込みは学習済みの地理的事前情報であり、年を変えても
新しい観測にはなりません。

### 場所 + 期間 → 画像の埋め込み

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

この経路は Earth Engine から画像を取得し、モデルの重みと実行時依存が必要です。手元に画像がある場合は
`get_image_embedding(model, pixels, spatial=..., temporal=..., sensor=..., device=...)` に CHW / TCHW 配列を
渡せます。ただしアダプターのバンド順と数値単位に従う必要があります（[API](docs/api.md)、[モデル](docs/models.md)）。

### Cloud Storage から AlphaEarth を直接取得

```bash
curl -L -o aef_index.parquet https://storage.googleapis.com/alphaearth_foundations/satellite_embedding/v1/annual/aef_index.parquet
```

```python
from earth_embedding import BBox, find_aef_tiles, sample_aef

tiles = find_aef_tiles("aef_index.parquet", spatial=BBox(-122.43, 37.76, -122.41, 37.78), year=2021)
result = sample_aef([[-122.42, 37.77]], tiles=tiles)
print(result.data.shape, result.meta["source_for_point"])  # (1, 64)
```

サンプラーは CRS 変換、COG のバイト範囲読み込み、int8 の逆量子化、欠損値を処理します。未被覆の地点は既定で
エラーとなり、`strict=False` では NaN として残します。Google の[公式 GCS ガイド](https://developers.google.com/earth-engine/guides/aef_on_gcs_readme)
では 2026 年 7 月以降は提供者負担のアクセスで、年次データは 2017～2025 年です。インデックスと出典表記は
[データアクセス](docs/data-access.md)をご覧ください。

## ギャラリー

### 22 モデルを同じ地域で

![同じ武漢地域における Sentinel-2 参照画像と 22 のモデル構成](docs/assets/comparison/all-models.webp)

画像エンコーダー、位置エンコーダー、事前計算済みプロダクトを並べて表示します。各パネルの PCA 色は独立で、
空間的な支持範囲もそのまま残しています。同じ色が同じ特徴やクラスを意味するわけではなく、順位付けの図でも
ありません。画像・プロダクトのパネルは検証済みの武漢の過去出力を再利用し（日付の違いは図中に表示）、
位置パネルは新たに推論しました。[入力と再現方法](docs/tutorials/model-comparison.md)。

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

`models=None` でカタログ全体を選べます。[`examples/compare_models.py`](examples/compare_models.py) は年次プロダクトの
年を自動設定し、図・特徴量配列・実行レポートを保存します（`--models satclip geoclip esri_gle --device cpu` は
画像も Earth Engine も不要）。

### 2 つのスケールでの位置エンコーダー

![全球と武漢の座標グリッドにおける SatCLIP、GeoCLIP、Esri GLE](docs/assets/comparison/location-encoders.png)

位置エンコーダーの入力は経緯度だけで、模様は学習された地理的事前情報です。領域と間隔は `spatial` と
`grid_step_m` で変更できます。

<!-- REAL_DEMOS_START -->
## 実データチュートリアル

CPU で実行でき、Earth Engine 認証は不要です。SHA-256 で検証されるサンフランシスコ湾岸の
**完全な 72 × 88 グリッド**（AlphaEarth（AEF）2021 公式 **1,280 m** オーバービュー、約 92 × 113 km、
6,336 セル、2.3 MB）を同梱しています。インストール：`python -m pip install -e ".[demo,aef]"`。

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/brand/demo-workflow-mobile.svg">
  <img src="docs/assets/brand/demo-workflow.svg" width="100%" alt="領域または座標から埋め込み、地図へ。特徴量とラベルから空間分割、線形分類器、地図と指標へ">
</picture>

**1 · AEF 2021 → PCA マップ**（オフライン）

```python
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("aef")
colors = pca_colors(data.features)
fig = plot_map(data.samples, colors, title="San Francisco Bay Area · AEF 2021 · PCA RGB")
fig.savefig("aef-pca.png", dpi=160)
```

**2 · Esri GLE → 位置の埋め込みマップ**（初回のみ約 3.7 MB の重み）

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
    <td width="50%"><img src="docs/assets/demos/aef-pca.png" alt="サンフランシスコ湾岸の AEF 2021 PCA マップ"></td>
    <td width="50%"><img src="docs/assets/demos/esri-gle-pca.png" alt="同じ 6,336 地点の Esri GLE PCA マップ"></td>
  </tr>
  <tr>
    <td><b>AEF 2021</b>：観測に基づく埋め込み。湾、尾根、市街地、デルタの農地が分かれます。</td>
    <td><b>Esri GLE</b>：同じセルを座標だけから表現。観測年のない滑らかな地理的事前情報です。</td>
  </tr>
</table>

RGB は 3 つの記述的な主成分であり、**土地被覆クラスではありません**。2 枚の色同士も比較できません。
`fetch_aef_demo()` で公式 GCS から再取得できます。

**3 · 埋め込み + ラベル → ホールドアウト分類**

```python
from earth_embedding.demo import classify_demo, plot_classification
result = classify_demo()
print({k: result["metrics"][k] for k in ("oa", "macro_f1", "balanced_accuracy")})
fig = plot_classification(result)
fig.savefig("bayarea-classification.png", dpi=160)
```

![湾岸の WorldCover 参照、フォールド外予測、誤り、混同行列](docs/assets/demos/bayarea-classification.png)

| OA | Macro-F1 | Balanced accuracy | 評価 / 緩衝帯 / 評価外 |
| ---: | ---: | ---: | --- |
| 93.64% | 91.64% | 92.63% | 5,806 / 528 / 裸地 2 |

2 つの空間フォールド：西半分だけで学習したモデルが東半分を予測し、その逆も行うため、評価対象のすべての
セルにホールドアウト予測があります。7.68 km の緩衝帯は学習にも評価にも使いません。ラベルは ESA WorldCover
2021（建物域・植生・農地・水域）、推定器は標準化 + クラス均衡ロジスティック回帰です。地域の**ソフトウェア実演**
であり、論文のベンチマークではありません。[分割、クラス数、出典、制約](docs/tutorials/real-demos.md)。

| Notebook | 内容 |
| --- | --- |
| [01 · 最初の埋め込みマップ](examples/notebooks/01_first_embedding_map.ipynb) | 検証済み AEF サンプルを読み込み PCA マップを描く |
| [02 · Esri GLE の位置](examples/notebooks/02_esri_locations.ipynb) | 位置エンコーダーのバッチ処理、キャッシュ、オフライン再実行 |
| [03 · 地域分類](examples/notebooks/03_regional_classification.ipynb) | 2 フォールド空間ホールドアウト、地図と指標 |
| [04 · 出力と再利用](examples/notebooks/04_export_and_reuse.ipynb) | ID 付きバッチ出力と安全な再整列 |
| [05 · モデル比較](examples/notebooks/05_compare_models.ipynb) | 3 モデルの CPU 比較とカタログ全体のセル |

すべての Notebook に実際の出力を保存しています（[実行記録](docs/validation/demo-notebooks.json)）。
<!-- REAL_DEMOS_END -->

## 仕組み

<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/brand/how-it-works-mobile.svg">
  <img src="docs/assets/brand/how-it-works.svg" width="100%" alt="画像エンコーダー、位置エンコーダー、事前計算済みプロダクトが共通の Python API を通じて地図化・検索・下流学習につながる">
</picture>

モデルは利用者が実際に受け取るオブジェクトで分類します：**A** 画像エンコーダー（A1 RGB、A2 固定バンド、
A3 チャンネル適応、A4 多時期）、**B** 位置エンコーダー、**C** 事前計算済みプロダクト（C1 グリッド、C2 サンプリング）。
アーキテクチャ、解像度、学習信号は別の属性です。

| 段階 | API | 確認事項 |
| --- | --- | --- |
| モデルの選択 | `earth-embedding models --json`、`describe MODEL` | 入力要件、出力、任意依存 |
| 画像の確認 | `inspect_provider_patch(...)` | 被覆、バンド、値、形状、観測期間 |
| 画像の符号化 | `get_embedding(...)`、`get_image_embedding(...)` | プロバイダー経由かローカルか、正しい前処理 |
| 位置の符号化 | `get_location_embeddings(...)` | WGS84 `[経度, 緯度]`、重み、デバイス |
| AEF の取得 | `find_aef_tiles(...)`、`sample_aef(...)` | 年、被覆、CRS、欠損値、取得元 |
| 大規模化 | `get_embeddings_batch(...)`、`export_batch(...)` | 構成の統一、キャッシュ、メタデータ、失敗記録 |
| 評価 | [`examples/evaluate_embeddings.py`](examples/evaluate_embeddings.py) | 空間分割、漏洩、支持範囲の整合 |

`.data` と `.meta` は一緒に保存してください。特徴次元と空間的な支持範囲はモデルごとに異なり、共通 API によって
別のエンコーダーのベクトルが交換可能になるわけではありません。

## モデル一覧

| モデル ID | 分類 | アダプター入力 | 上流 | 重み・プロダクト |
| --- | --- | --- | --- | --- |
| [`remoteclip`](docs/models/remoteclip.md) | A1 · 画像 | Sentinel-2 RGB | [コード](https://github.com/ChenDelong1999/RemoteCLIP) | [🤗 モデル](https://huggingface.co/MVRL/remote-clip-vit-base-patch32) |
| [`satmae`](docs/models/satmae.md) | A1 · 画像 | Sentinel-2 RGB | [コード](https://github.com/sustainlab-group/SatMAE) | [🤗 モデル](https://huggingface.co/MVRL/satmae-vitlarge-fmow-pretrain-800) |
| [`satmaepp`](docs/models/satmaepp.md) | A1 · 画像 | Sentinel-2 RGB | [コード](https://github.com/techmn/satmae_pp) | [🤗 モデル](https://huggingface.co/MVRL/satmaepp_ViT-L_pretrain_fmow_rgb) |
| [`scalemae`](docs/models/scalemae.md) | A1 · 画像 | Sentinel-2 RGB + 地上解像度 | [コード](https://github.com/bair-climate-initiative/scale-mae) | [🤗 モデル](https://huggingface.co/MVRL/scalemae-vitlarge-800) |
| [`wildsat`](docs/models/wildsat.md) | A1 · 画像 | Sentinel-2 RGB | [コード](https://github.com/cvl-umass/wildsat) | [公式](https://github.com/cvl-umass/wildsat#quickstart) |
| [`satmaepp_s2_10b`](docs/models/satmaepp.md) | A2 · 画像 | Sentinel-2 10 バンド | [コード](https://github.com/techmn/satmae_pp) | [🤗 モデル](https://huggingface.co/mubashir04/checkpoint_ViT-L_pretrain_fmow_sentinel) |
| [`prithvi`](docs/models/prithvi.md) | A2 · 画像 | Sentinel-2 6 バンド + 時間・位置 | [コード](https://github.com/NASA-IMPACT/Prithvi-EO-2.0) | [🤗 モデル](https://huggingface.co/ibm-nasa-geospatial/Prithvi-EO-2.0-100M-TL) |
| [`terrafm`](docs/models/terrafm.md) | A2 · 画像 | Sentinel-2 12 バンドまたは Sentinel-1 VV/VH | [コード](https://github.com/mbzuai-oryx/TerraFM) | [🤗 モデル](https://huggingface.co/MBZUAI/TerraFM) |
| [`terramind`](docs/models/terramind.md) | A2 · 画像 | Sentinel-2 12 バンド | [コード](https://github.com/IBM/terramind) | [🤗 モデル](https://huggingface.co/ibm-esa-geospatial/TerraMind-1.0-small) |
| [`satvision`](docs/models/satvision.md) | A2 · 画像 | 14 チャンネル MODIS TOA | [コード](https://github.com/nasa-nccs-hpda/pytorch-caney) | [🤗 モデル](https://huggingface.co/nasa-cisto-data-science-group/satvision-toa-giant-patch8-window8-128) |
| [`dofa`](docs/models/dofa.md) | A3 · 画像 | マルチスペクトル画像 + 波長 | [コード](https://github.com/zhu-xlab/DOFA) | [🤗 モデル](https://huggingface.co/earthflow/DOFA) |
| [`fomo`](docs/models/fomo.md) | A3 · 画像 | Sentinel-2 12 バンド | [コード](https://github.com/RolnickLab/FoMo-Bench) | [公式](https://github.com/RolnickLab/FoMo-Bench#loading-pretrained-fomo-net) |
| [`thor`](docs/models/thor.md) | A3 · 画像 | Sentinel-2 10 バンド | [コード](https://github.com/FM4CS/THOR) | [🤗 モデル](https://huggingface.co/FM4CS/THOR-1.0-base) |
| [`galileo`](docs/models/galileo.md) | A4 · 画像 | Sentinel-2 10 バンド時系列 | [コード](https://github.com/nasaharvest/galileo) | [🤗 モデル](https://huggingface.co/nasaharvest/galileo) |
| [`anysat`](docs/models/anysat.md) | A4 · 画像 | Sentinel-2 10 バンド時系列 | [コード](https://github.com/gastruc/anysat) | [🤗 モデル](https://huggingface.co/g-astruc/AnySat) |
| [`agrifm`](docs/models/agrifm.md) | A4 · 画像 | Sentinel-2 10 バンド時系列 | [コード](https://github.com/flyakon/AgriFM) | [公式](https://github.com/flyakon/AgriFM#model-training) |
| [`satclip`](docs/models/satclip.md) | B · 位置 | 経緯度、256 次元 | [コード](https://github.com/microsoft/satclip) | [🤗 モデル](https://huggingface.co/microsoft/SatCLIP-ViT16-L40) |
| [`geoclip`](docs/models/geoclip.md) | B · 位置 | 経緯度、512 次元 | [コード](https://github.com/VicenteVivan/geo-clip) | [公式](https://github.com/VicenteVivan/geo-clip#usage-pre-trained-location-encoder) |
| [`esri_gle`](docs/models/esri_gle.md) | B · 位置 | 経緯度、256 次元 | [文書](https://doc.arcgis.com/en/pretrained-models/latest/vector/introduction-to-global-location-encoder-sentinel-2-.htm) | [公式](https://www.arcgis.com/home/item.html?id=b0664ef297c04d4aaa44191cf21e07f3) |
| [`gse`](docs/models/gse.md) | C1 · プロダクト | 年次 Google Satellite Embedding、10 m、64 次元 | [カタログ](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) | [公式](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) |
| [`tessera`](docs/models/tessera.md) | C1 · プロダクト | GeoTessera 公開タイル、10 m | [コード](https://github.com/ucam-eo/geotessera) | [公式](https://github.com/ucam-eo/geotessera#dataset-versions-and-variants) |
| [`copernicus`](docs/models/copernicus.md) | C1 · プロダクト | 0.25° 埋め込みグリッド | [出典](https://huggingface.co/datasets/wangyi111/Copernicus-Embed-025deg) | [🤗 データセット](https://huggingface.co/datasets/torchgeo/copernicus_embed) |

これらは上流のリソースであり、本プロジェクトは重みを再配布しません（[形式、既定の版、利用条件](docs/model-resources.md#which-artifact-am-i-opening)）。
アダプターは統合の入り口であり、データへのアクセスやお使いの環境での動作を保証するものではありません。
[検証記録](docs/validation.md)をご覧ください。分類体系には **C2 サンプリング型コレクション**もありますが、
C2 アダプターの実装はまだ主張していません。

## 研究の背景と制約

研究原稿の作業から、公開形態の分類、比較可能な入出力契約、評価の来歴記録を取り込んでいます。固定済みの
論文ベンチマークは **20 システム（A16 + B1 SatCLIP + C3）**です。GeoCLIP と Esri GLE は後から追加した
ソフトウェア統合であり、その評価対象を広げるものではありません。原稿は準備中で、採択、最終ランキング、
科学的な順位を主張するものではありません（[研究範囲](docs/research.md)）。

データ提供者によっては認証、クォータ、利用条件への同意が必要です。大きな重みを要するモデルもあります。
位置エンコーダーは時系列観測を持たず、粗いプロダクトを再サンプリングしても 10 m の場にはなりません。
比較を設計する前に[制約](docs/limitations.md)を確認してください。

## ドキュメント案内

| 入門 | 詳細 |
| --- | --- |
| [クイックスタート](docs/quickstart.md) | [API リファレンス](docs/api.md) |
| [モデル](docs/models.md) · [リソース](docs/model-resources.md) | [入力と出力の概念](docs/concepts.md) |
| [実データチュートリアル](docs/tutorials/real-demos.md) | [抽出ワークフロー](docs/workflows.md) |
| [モデル比較](docs/tutorials/model-comparison.md) | [検証記録](docs/validation.md) |
| [AlphaEarth データ取得](docs/data-access.md) | [アダプターの追加](docs/extending.md) |
| [例](examples/) | [変更履歴](CHANGELOG.md) |

## コントリビューション

入力契約が明確なアダプター、再現可能な不具合報告、小さな実行例、データ取得の修正、英語・中国語・日本語の
文書改善を歓迎します。[CONTRIBUTING.md](CONTRIBUTING.md) を読むか、公式ソース、ライセンス、重み、具体的な
用途を添えて [Issue](https://github.com/GISWLH/earth-embedding/issues) を作成してください。バナー、ロゴ、図は
編集可能な Excalidraw ソースです（[アートワークガイド](docs/assets/brand/README.md)）。

## 来歴と謝辞

Earth Embedding は、Dingqi Ye 氏とコントリビューターが作成した [CyberGIS rs-embed](https://github.com/cybergis/rs-embed)
を基に独立して保守される拡張です。Apache-2.0 ライセンスを維持し、その API、アダプター、実装基盤に感謝します。
[rs-embed 論文](https://arxiv.org/abs/2602.23678)は rs-embed を説明するもので、本プロジェクトの原稿と拡張は別の成果です
（[来歴](docs/provenance.md)）。

rs-embed の貢献者、各モデル・データセットの著者、Google Earth Engine、Google / Google DeepMind、TorchGeo、
GeoTessera、TerraTorch、rshf、Microsoft SatCLIP、GeoCLIP、Esri、地球観測コミュニティに感謝します。
統合は推薦を意味しません。

## 引用

使用したコミットまたはリリースとともに本ソフトウェアを引用してください（[CITATION.cff](CITATION.cff)）。
元のフレームワークを使う場合は rs-embed 論文を、分析に用いたモデルとデータの原著も引用してください。

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

## ライセンス

ライブラリのコードは [Apache-2.0](LICENSE) で、元の帰属は [NOTICE](NOTICE) に保持しています。外部コード、
モデル重み、データ、フォントにはそれぞれのライセンスが適用されます。AlphaEarth データと ESA WorldCover は
CC-BY-4.0、Esri のソフトウェアとモデルは独自の条件に従います。[来歴とライセンス](docs/provenance.md)をご覧ください。
