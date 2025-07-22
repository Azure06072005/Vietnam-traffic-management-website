
# ベトナム交通データ分析アプリケーション

このWebアプリケーションは、DashとPythonを使用して開発され、ベトナムの各省市における交通違反や交通事故データを視覚化します。

## 主な機能

- CSVファイルから交通データをアップロードして分析
- GeoJSONファイルからベトナムの地図を表示
- 地理データに基づくヒートマップ（Choroplethマップ）を作成
- 交通違反/事故の多い上位10省市を棒グラフで表示
- 詳細データテーブル（並び替え、フィルタリング機能あり）
- サンプルデータによるデモ表示も可能
- レスポンシブデザイン（モバイル対応）

## ディレクトリ構成

```
├── assets/                         # CSSや静的リソース
│   ├── ico                         # Faviconファイル
│   ├── brandname.css
│   ├── data-buttons.css
│   ├── login.css
│   ├── navigation.css
│   └── style.css                   # メインCSSファイル
├── ho_tro/
│   ├── dieu_khoan.html             # 利用規約
│   ├── huong_dan_su_dung.html      # 使い方ガイド
│   └── thong_bao.html              # お知らせ
├── app.py                          # アプリケーション本体
├── callbacks.py                    # ユーザー操作処理
├── diaphantinh.geojson             # ベトナム各省市のGeoJSONファイル
├── index.html
├── layout.py                       # UIレイアウト定義
├── login.py                        # ログイン機能
├── main.py                         # アプリ起動用
├── project-summary.md              # プロジェクト概要
├── README.md                       # このファイル（使用ガイド）
├── routes.py                       # ルーティング処理
└── vipham.csv                      # 交通違反データCSV
```

## 動作環境

| 項目                | 内容                                                              |
| ----------------- | ---------------------------------------------------------------- |
| Python             | 3.7以上                                                          |
| 必要なライブラリ   | dash, dash-bootstrap-components, plotly, pandas, numpy, flask   |
| GeoJSONファイル    | ベトナムの各省市の地理データ（`ten_tinh`フィールドが必要）         |
| CSVデータ          | 省市名と交通違反・事故データを含む必要あり                        |
| 実行方法           | `main.py`を実行                                                  |
| アクセス           | ブラウザで `http://localhost:8050` にアクセス                     |

## インストール方法

### 1. 環境構築

Python3.7以上をインストールし、以下のライブラリをインストールしてください。

```bash
pip install dash dash-bootstrap-components dash-bootstrap-templates plotly pandas numpy flask
```

### 2. リポジトリのクローン

```bash
git clone https://github.com/Azure06072005/Vietnam-traffic-management-application.git
cd Vietnam-traffic-management-application
```

### 3. アプリケーションの起動

```bash
python main.py
```

### 4. アクセス方法

ブラウザで以下にアクセス：

```
http://localhost:8050
```

### 5. ログイン

初期ユーザー：

```
ユーザー名: admin  
パスワード: 123456
```

> **注意**: セキュリティのため、実運用時はパスワードを変更してください。

---

## 使用方法

### データのアップロード

1. GeoJSONファイル（ベトナム省市の境界情報）をアップロード
2. 交通違反・事故データのCSVファイルをアップロード
3. データ項目の選択：
   - **省市名カラム**: `Ten_Tinh_Thanh`
   - **データタイプ**:
     - 交通違反
     - 交通事故
     - 死亡数
     - 負傷数
     - 罰金額
   - **データカラム**: `MAVP`
4. 「データ処理」ボタンをクリックして、結果を表示

または、「サンプルデータを使用」ボタンでデモを体験できます。

### 表示のカスタマイズ

- 「交通違反」または「交通事故」タブで切り替え
- 地図、棒グラフ、データテーブルの表示/非表示を切り替え可能
- カラーマップを変更可能

## データ仕様

### GeoJSON

- 各`feature`の`properties`に`ten_tinh`が必要（省市名）

### CSV

- 省市名（GeoJSONの`ten_tinh`と一致する必要あり）
- 交通違反データ
- 交通事故データ

---

## 今後の拡張予定

- より高度な統計分析の追加
- 時系列分析（タイムシリーズ）
- 地域・期間ごとの比較機能
- UI/UX改善

## ライセンス

このプロジェクトはMITライセンスで提供されています。

---

## 注意事項と改善提案

- **実運用時はパスワード変更を推奨します**
- データのサンプルファイルは `vipham.csv` と `diaphantinh.geojson` に含まれています
- ご質問やバグ報告は[GitHub Issue](https://github.com/Azure06072005/Vietnam-traffic-management-application/issues)まで
