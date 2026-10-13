"""Keep the three README demo blocks on identical runnable code and results."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
install = """```bash
git clone https://github.com/GISWLH/earth-embedding.git
cd earth-embedding
python -m pip install -e ".[demo,aef]"
```
"""
aef = """```python
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("aef")
colors = pca_colors(data.features)
fig = plot_map(data.samples, colors, title="San Francisco Bay Area | AEF 2021 | PCA RGB")
fig.savefig("aef-pca.png", dpi=160)
```

![AEF 2021 PCA](docs/assets/demos/aef-pca.png)
"""
gle = """```python
from earth_embedding import get_location_embeddings
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("bayarea")
points = data.samples[["center_lon", "center_lat"]].to_numpy()
gle = get_location_embeddings("esri_gle", points, device="cpu", batch_size=128)
fig = plot_map(data.samples, pca_colors(gle.data), title="San Francisco Bay Area | Esri GLE | PCA RGB")
fig.savefig("esri-gle-pca.png", dpi=160)
```

![Esri GLE PCA](docs/assets/demos/esri-gle-pca.png)
"""
classification = """```python
from earth_embedding.demo import classify_demo, plot_classification
result = classify_demo()
print({k: result["metrics"][k] for k in ("oa", "macro_f1", "balanced_accuracy")})
fig = plot_classification(result)
fig.savefig("bayarea-classification.png", dpi=160)
```

![San Francisco Bay Area reference, held-out predictions, errors and confusion matrix](docs/assets/demos/bayarea-classification.png)

| OA | Macro-F1 | Balanced Accuracy | Train / test / buffer / excluded |
| ---: | ---: | ---: | --- |
| METRICS_ROW |
"""
workflow = """<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/earth-embedding-demos-mobile.svg">
  <img src="docs/assets/earth-embedding-demos.svg" width="100%" alt="Location to embedding to map; features and labels to spatial holdout, classifier and measured results.">
</picture>
"""
notebooks = """[01 · AEF](examples/notebooks/01_first_embedding_map.ipynb) ·
[02 · Esri GLE](examples/notebooks/02_esri_locations.ipynb) ·
[03 · Classification](examples/notebooks/03_regional_classification.ipynb) ·
[04 · Export / reuse](examples/notebooks/04_export_and_reuse.ipynb)
"""
texts = {
    "README.md": [
        "## Five lines to a real map",
        "Python 3.12+, CPU. Install from this Git repository; no PyPI release is assumed. The small real samples are bundled and SHA-256 verified. No Earth Engine login or private paths are needed.",
        "### 1. AEF 2021 → PCA map",
        "San Francisco Bay Area and surroundings, 122.6–121.6° W / 37.3–38.3° N, about **88 × 111 km**. 5,933 real Google / Google DeepMind AEF 2021 overview cells at **1,280 m** support; the checked bundle is 2.1 MB. RGB shows descriptive principal components, **not land-cover classes**. Sampling and licenses: [full tutorial](docs/tutorials/real-demos.md). To repeat official GCS reads use `fetch_aef_demo()` from `earth_embedding.demo`; the first map above works offline.",
        "### 2. Esri GLE → location map",
        "5,933 San Francisco Bay Area locations; official ~3.7 MB weights download once and run directly in PyTorch. No ArcGIS/ArcPy. GLE has **no observation year**; colors show a geographic prior, not a dated land-cover map.",
        "### 3. Embeddings + labels → classification",
        "Newly computed regional **software demo**, not current global paper results. Four classes: built, vegetation, cropland, water. South trains, north tests, with a ≥5.5 km geographic gap; two bare cells are excluded. There are only 9 cropland training cells, so class imbalance limits this fixed holdout. Scaler and Logistic Regression fit training rows only (seed 42). Gray cells are unscored. [Class counts, source/license, split, metrics and limits](docs/tutorials/real-demos.md).",
        "### Four executed notebooks",
        "Each notebook contains real execution outputs and maps. [Execution receipt](docs/validation/demo-notebooks.json) · [Complete tutorial](docs/tutorials/real-demos.md) · [Editable Excalidraw](docs/assets/earth-embedding-demos.excalidraw). Notebook 04 exports and safely reloads batches; it does not rank products with unequal spatial support.",
    ],
    "README.zh-CN.md": [
        "## 五行代码，得到第一张真实地图",
        "Python 3.12+，CPU 可运行。从本 Git 仓库安装，不假设已发布到 PyPI。小型真实样例随包提供，读取时验证 SHA-256；无需 Earth Engine 登录或私人路径。",
        "### 1. AEF 2021 → PCA 空间图",
        "旧金山湾区及周边，西经 122.6–121.6°、北纬 37.3–38.3°，约 **88 × 111 公里**。5,933 个真实 Google / Google DeepMind AEF 2021 金字塔网格，空间支持范围为 **1,280 米**；校验后的小型数据包约 2.1 MB。RGB 表示描述性主成分，**不代表地物类别**。抽样和许可见[完整教程](docs/tutorials/real-demos.md)。如需重新读取官方 GCS，可调用 `earth_embedding.demo` 中的 `fetch_aef_demo()`；上面的第一张地图可离线生成。",
        "### 2. Esri GLE → 经纬度嵌入地图",
        "批量编码旧金山湾区 5,933 个位置；首次下载约 3.7 MB 官方权重，直接使用 PyTorch，无需 ArcGIS/ArcPy。GLE **没有观测年份**，颜色展示位置先验，不能视为某一年的土地覆盖图。",
        "### 3. 嵌入 + 标签 → 分类结果",
        "本次实际运行的区域**软件演示**，不是当前论文全球实验结果。建成区、植被、耕地、水体四分类；南部训练、北部测试，中间保留至少约 5.5 公里的隔离带，排除 2 个裸地网格。训练区仅有 9 个耕地网格，固定空间留出存在明显类别不平衡。标准化和逻辑回归仅用训练集拟合（种子 42）。灰色区域不评分。[类别数量、来源许可、划分和限制](docs/tutorials/real-demos.md)。",
        "### 四个已执行的导览 Notebook",
        "均保存真实运行输出和图像。[执行记录](docs/validation/demo-notebooks.json) · [完整教程](docs/tutorials/real-demos.md) · [可编辑 Excalidraw](docs/assets/earth-embedding-demos.excalidraw)。第 04 个演示分批导出和按 ID 安全复用，不对空间支持范围不一致的产品进行排名。",
    ],
    "README.ja.md": [
        "## 5 行で最初の実データ地図を作る",
        "Python 3.12 以降、CPU で実行できます。この Git リポジトリからインストールし、PyPI 公開は前提にしません。小さな実データを同梱し、読み込み時に SHA-256 を検証します。Earth Engine 認証や個人環境のパスは不要です。",
        "### 1. AEF 2021 → PCA マップ",
        "サンフランシスコ湾岸と周辺、西経 122.6–121.6° / 北緯 37.3–38.3°、約 **88 × 111 km**。Google / Google DeepMind AEF 2021 の **1,280 m** オーバービューから 5,933 セルを同梱しています。検証付きデータは約 2.1 MB です。RGB は記述的な主成分であり、**土地被覆クラスではありません**。[取得方法とライセンス](docs/tutorials/real-demos.md)。公式 GCS を再取得する場合は `earth_embedding.demo` の `fetch_aef_demo()` を使用します。上の例はオフラインで動作します。",
        "### 2. Esri GLE → 位置の埋め込みマップ",
        "湾岸の 5,933 地点をバッチ処理します。初回のみ約 3.7 MB の公式重みを取得し、PyTorch で直接推論します。ArcGIS/ArcPy は不要です。GLE に**観測年はなく**、色は位置の事前表現であり、特定年の土地被覆図ではありません。",
        "### 3. 埋め込み + ラベル → 分類",
        "今回実行した地域データの**ソフトウェア実演**であり、論文の全球結果ではありません。建物域・植生・農地・水域の 4 クラス。南部を学習、北部をテストとし、約 5.5 km 以上の間隔を設け、裸地 2 セルを除外します。学習用の農地は 9 セルしかなく、固定した空間分割にはクラス不均衡があります。標準化とロジスティック回帰は学習データだけで推定します（seed 42）。灰色部分は評価対象外です。[クラス数・出典・分割・制約](docs/tutorials/real-demos.md)。",
        "### 実行済みの 4 つの Notebook",
        "実際の出力と地図を保存しています。[実行記録](docs/validation/demo-notebooks.json) · [詳細チュートリアル](docs/tutorials/real-demos.md) · [編集可能な Excalidraw](docs/assets/earth-embedding-demos.excalidraw)。04 は分割出力と ID による再利用を扱い、空間的な支持範囲が異なる製品の順位付けは行いません。",
    ],
}
metrics = json.loads((root / "docs/assets/demos/classification-metrics.json").read_text())
classification = classification.replace(
    "METRICS_ROW",
    f"{metrics['oa']:.2%} | {metrics['macro_f1']:.2%} | {metrics['balanced_accuracy']:.2%} | 3383 / 2173 / 375 / 2",
)
for name, t in texts.items():
    block = "\n\n".join(
        [
            t[0],
            t[1],
            install,
            workflow,
            t[2],
            aef,
            t[3],
            t[4],
            gle,
            t[5],
            t[6],
            classification,
            t[7],
            t[8],
            notebooks,
            t[9],
        ]
    )
    block = "<!-- REAL_DEMOS_START -->\n" + block + "\n<!-- REAL_DEMOS_END -->\n\n"
    path = root / name
    original = path.read_text(encoding="utf-8")
    if "<!-- REAL_DEMOS_START -->" in original:
        start = original.index("<!-- REAL_DEMOS_START -->")
        end = original.index("<!-- REAL_DEMOS_END -->") + len("<!-- REAL_DEMOS_END -->\n\n")
        updated = original[:start] + block + original[end:]
    else:
        start = original.index("\n## ")
        updated = original[:start] + "\n" + block + original[start:]
    path.write_text(updated, encoding="utf-8")
