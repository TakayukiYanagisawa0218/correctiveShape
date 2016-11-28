# correctiveShape

deformしているmeshに対しcorrectiveShapeを作成するスクリプトです。  

考え方はChad Vernon氏のcvShapeInverterというplug-inを参考にさせて頂いてます。  
http://www.chadvernon.com/blog/resources/cvshapeinverter/

中身は一部API2.0で書いているのである程度高速だと思います。  
maya2013辺り合わせで作成しましたが上位バージョンでも動作すると思います。（全部のバージョンでは試してないです）  

簡単なスクリプトの流れ  
①baseの頂点の位置を取得  
②baseの頂点のxyz軸をmatrixとして取得  
③targetの頂点の位置を取得  
④3から1の値を減算しローカライズ  
⑤2のmatrixと４の値の積を求める（座標変換）  
⑥originalの頂点に５の値をセット  

# 使い方
```
import correctiveShape
correctiveShape.execute('deformObj', 'scluptObj')
```
もしくは
```
correctiveShape.execute('deformObj', 'scluptObj', 'resultShapeName')
```
