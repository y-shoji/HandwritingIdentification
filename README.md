# 筆跡鑑定アプリα  

## 原理  
1. フーリエ級数展開にて、文字を三角関数の式として保存  
2. 文字の平均化のパラメータを調整する事によって、2~3回書いた文字から、筆跡の特徴の同じ文字を複製   
3. 深層学習で筆跡判定(改良中)  

文字の平均化は`demo`にて紹介

## セットアップ
### 動作確認  
Macbook Air 2018モデル macOS Catalina10.15  
pyhton 3.7.5  
### 手順
1. [学習済みモデル](https://www.dropbox.com/s/qxubpa5f3oiano6/Get%20Started%20with%20Dropbox%20Paper.url?dl=0)をダウンロード&`app.py`と同じフォルダにおく  
2. 必要ライブラリのインストール`pip install -r requirement.txt`  
3. アプリの実行`python app.py`  

