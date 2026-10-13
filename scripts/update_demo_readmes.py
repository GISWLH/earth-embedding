"""Keep the three README demo blocks on identical runnable code and results."""

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
fig = plot_map(data.samples, colors, title="Wuhan | AEF 2021 | PCA RGB")
fig.savefig("aef-pca.png", dpi=160)
```

![AEF 2021 PCA](docs/assets/demos/aef-pca.png)
"""
gle = """```python
from earth_embedding import get_location_embeddings
from earth_embedding.demo import load_demo, pca_colors, plot_map
data = load_demo("wuhan")
points = data.samples[["center_lon", "center_lat"]].to_numpy()
gle = get_location_embeddings("esri_gle", points, device="cpu", batch_size=128)
fig = plot_map(data.samples, pca_colors(gle.data), title="Wuhan | Esri GLE | PCA RGB")
fig.savefig("esri-gle-pca.png", dpi=160)
```

![Esri GLE PCA](docs/assets/demos/esri-gle-pca.png)
"""
classification = """```python
from earth_embedding.demo import classify_demo, plot_classification
result = classify_demo()
print({k: result["metrics"][k] for k in ("oa", "macro_f1", "balanced_accuracy")})
fig = plot_classification(result)
fig.savefig("wuhan-classification.png", dpi=160)
```

![Wuhan reference, held-out predictions, errors and confusion matrix](docs/assets/demos/wuhan-classification.png)

| OA | Macro-F1 | Balanced Accuracy | Train / test / buffer / excluded |
| ---: | ---: | ---: | --- |
| 93.81% | 91.92% | 90.52% | 310 / 210 / 42 / 5 |
"""
workflow = """<picture>
  <source media="(max-width: 760px)" srcset="docs/assets/earth-embedding-demos-mobile.svg">
  <img src="docs/assets/earth-embedding-demos.svg" width="100%" alt="Location to embedding to map; features and labels to spatial holdout, classifier and measured results.">
</picture>
"""
notebooks = """[01 · AEF](examples/notebooks/01_first_embedding_map.ipynb) ·
[02 · Esri GLE](examples/notebooks/02_esri_locations.ipynb) ·
[03 · Classification](examples/notebooks/03_wuhan_classification.ipynb) ·
[04 · Export / reuse](examples/notebooks/04_export_and_reuse.ipynb)
"""
texts = {
    "README.md": [
        "## Five lines to a real map",
        "Python 3.12+, CPU. Install from this Git repository; no PyPI release is assumed. The small real samples are bundled and SHA-256 verified. No Earth Engine login or private paths are needed.",
        "### 1. AEF 2021 → PCA map",
        "Wuhan, 114.40–114.42° E / 30.51–30.53° N. A 64 × 64 sample of real Google / Google DeepMind AEF 2021 vectors. RGB shows descriptive principal components, **not land-cover classes**. Sampling and licenses: [full tutorial](docs/tutorials/real-demos.md). To repeat official GCS reads use `fetch_aef_demo()` from `earth_embedding.demo`; the first map above works offline.",
        "### 2. Esri GLE → location map",
        "567 Wuhan locations; official ~3.7 MB weights download once and run directly in PyTorch. No ArcGIS/ArcPy. GLE has **no observation year**; colors show a geographic prior, not a dated land-cover map.",
        "### 3. Embeddings + labels → classification",
        "Newly computed historical Wuhan **software demo**, not current global paper results. Three classes: built, vegetation, water. East trains, west tests, two columns buffer; five rare cropland cells are excluded. Scaler and Logistic Regression fit training rows only (seed 42). Gray cells are unscored. [Class counts, source/license, split, metrics and limits](docs/tutorials/real-demos.md).",
        "### Four executed notebooks",
        "Each notebook contains real execution outputs and maps. [Execution receipt](docs/validation/demo-notebooks.json) · [Complete tutorial](docs/tutorials/real-demos.md) · [Editable Excalidraw](docs/assets/earth-embedding-demos.excalidraw). Notebook 04 exports and safely reloads batches; it does not rank products with unequal spatial support.",
    ],
    "README.zh-CN.md": [
        "## 五行代码，得到第一张真实地图",
        "Python 3.12+，CPU 可运行。从本 Git 仓库安装，不假设已发布到 PyPI。小型真实样例随包提供，读取时验证 SHA-256；无需 Earth Engine 登录或私人路径。",
        "### 1. AEF 2021 → PCA 空间图",
        "武汉，东经 114.40–114.42°、北纬 30.51–30.53°。64 × 64 个真实 Google / Google DeepMind AEF 2021 向量；RGB 表示描述性主成分，**不代表地物类别**。抽样和许可见[完整教程](docs/tutorials/real-demos.md)。如需重新读取官方 GCS，可调用 `earth_embedding.demo` 中的 `fetch_aef_demo()`；上面的第一张地图可离线生成。",
        "### 2. Esri GLE → 经纬度嵌入地图",
        "批量编码武汉 567 个位置；首次下载约 3.7 MB 官方权重，直接使用 PyTorch，无需 ArcGIS/ArcPy。GLE **没有观测年份**，颜色展示位置先验，不能视为某一年的土地覆盖图。",
        "### 3. 嵌入 + 标签 → 分类结果",
        "本次重新计算的历史武汉**软件演示**，不是当前论文全球实验结果。建成区、植被、水体三分类；东部训练、西部测试，中间两列为缓冲，5 个稀有耕地格网排除。标准化和逻辑回归仅用训练集拟合（种子 42）。灰色区域不评分。[类别数量、来源许可、划分和限制](docs/tutorials/real-demos.md)。",
        "### 四个已执行的导览 Notebook",
        "均保存真实运行输出和图像。[执行记录](docs/validation/demo-notebooks.json) · [完整教程](docs/tutorials/real-demos.md) · [可编辑 Excalidraw](docs/assets/earth-embedding-demos.excalidraw)。第 04 个演示分批导出和按 ID 安全复用，不对空间支持范围不一致的产品进行排名。",
    ],
    "README.ja.md": [
        "## 5 行で最初の実データ地図を作る",
        "Python 3.12 以降、CPU で実行できます。この Git リポジトリからインストールし、PyPI 公開は前提にしません。小さな実データを同梱し、読み込み時に SHA-256 を検証します。Earth Engine 認証や個人環境のパスは不要です。",
        "### 1. AEF 2021 → PCA マップ",
        "武漢、東経 114.40–114.42° / 北緯 30.51–30.53°。Google / Google DeepMind AEF 2021 の実際のベクトルを 64 × 64 点でサンプリングしました。RGB は記述的な主成分であり、**土地被覆クラスではありません**。[取得方法とライセンス](docs/tutorials/real-demos.md)。公式 GCS を再取得する場合は `earth_embedding.demo` の `fetch_aef_demo()` を使用します。上の例はオフラインで動作します。",
        "### 2. Esri GLE → 位置の埋め込みマップ",
        "武漢の 567 地点をバッチ処理します。初回のみ約 3.7 MB の公式重みを取得し、PyTorch で直接推論します。ArcGIS/ArcPy は不要です。GLE に**観測年はなく**、色は位置の事前表現であり、特定年の土地被覆図ではありません。",
        "### 3. 埋め込み + ラベル → 分類",
        "今回再計算した過去の武漢データによる**ソフトウェア実演**であり、現在の論文の全球結果ではありません。建物域・植生・水域の 3 クラス。東部を学習、西部をテスト、2 列をバッファとし、希少な農地 5 セルを除外します。標準化とロジスティック回帰は学習データだけで推定します（seed 42）。灰色部分は評価対象外です。[クラス数・出典・分割・制約](docs/tutorials/real-demos.md)。",
        "### 実行済みの 4 つの Notebook",
        "実際の出力と地図を保存しています。[実行記録](docs/validation/demo-notebooks.json) · [詳細チュートリアル](docs/tutorials/real-demos.md) · [編集可能な Excalidraw](docs/assets/earth-embedding-demos.excalidraw)。04 は分割出力と ID による再利用を扱い、空間的な支持範囲が異なる製品の順位付けは行いません。",
    ],
}
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
