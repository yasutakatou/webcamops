# handmouse

**「影絵でオペレーション」**ってなやつです。<br>
ジェスチャーではなく、あくまで形を認識して定義されたオペレーションを実行します。

![demo](https://github.com/yasutakatou/handmouse/blob/pic/handmouse.gif)

最初にアクションさせたい画像をアノテーションします。

```
python record.py
```

を起動させます。引数を二つ渡せます。画像のX/Yのサイズです。

1-9のキーで保存するファイル名を変更できます。1を押したら1.png、2なら2.pngって具合です。実際のカメラとフィルター後の形を見て、アノテーションしてください。1-9なので9個まで定義できます。

![1](https://github.com/yasutakatou/handmouse/blob/pic/1.png)
![2](https://github.com/yasutakatou/handmouse/blob/pic/2.png)
![3](https://github.com/yasutakatou/handmouse/blob/pic/3.png)

次にconfigファイルに画像に紐づく、マウスの操作なり、キー入力を定義します。<br>
定義はcsvです。**画像のファイル名＋動作**で定義します。

```
1,right
```

であれば1.pngに似た場合に「マウスカーソルを右に移動」になります。<br>
以下はマウス用の特殊定義です。

|定義名|操作|
|:---|:---|
|right|カーソルを右に移動|
|left|カーソルを左に移動|
|up|カーソルを上に移動|
|down|カーソルを下に移動|
|click|左クリック|
|rclick|右クリック|
|dclick|左ダブルクリック|

キー入力させたい場合は特殊定義以外の英字を書きます。<br>
 , で区切ることで～を押しながらのショートカットキー操作を定義できます。

```
8,ctrl,c
```

であれば8.pngに似た場合に「Ctrl+c」をキー入力します。<br>
以下はキーボード用の特殊定義です。

|定義名|操作|
|:---|:---|
|shift|shiftを押しながら|
|ctrl|ctrlを押しながら|
|alt|altを押しながら|
|enter|エンターキー|
|space|スペースキー|

定義が出来たら本体を起動させます。<br>
OpenCVで算出した画像類似度の閾値を満たせば定義にそって操作してくれます。

```
python handmouse.py
```

こちらも引数を二つ渡せます。画像のX/Yのサイズです。<br>
フィルターされたカメラ画像以外にTrackbarsの窓が出てきます。以下の意味です。

|項目|効果|
|:---|:---|
|actionValue|閾値ですカメラの解像度で頻繁に検知する場合は値を上げてください|
|moveValue|マウスの移動量です。大きいほど一度に多く移動します|
|Horizon|カメラ画像を水平反転します|
|Vetical|カメラ画像を垂直反転します|
|Stop|操作を一時停止します。再開はもう一度押してください|
|Exit|プログラムを停止します|

あくまで影絵システムなので手や体以外の形でも操作できます。

![pine](https://github.com/yasutakatou/handmouse/blob/pic/pine.png)
