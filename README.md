# correctiveShape

deformしているmeshに対しcorrectiveShapeを作成するスクリプトです。

考え方はChad Vernon氏のcvShapeInverterというplug-inを参考にさせて頂いてます。

http://www.chadvernon.com/blog/resources/cvshapeinverter/

中身は一部API2.0で書いているのである程度高速だと思います。
maya2013辺り合わせで作成しましたが上位バージョンでも動作すると思います。（全部のバージョンでは試してないです）

簡単なスクリプトの流れ
1．baseの頂点の位置を取得
2．baseの頂点のxyz軸をmatrixとして取得
3．targetの頂点の位置を取得
4．3から1の値を減算しローカライズ
5．2のmatrixと４の値の積を求める（座標変換）
6．originalの頂点に５の値をセット

# 使い方
import correctiveShape
correctiveShape.execute('deformObj', 'scluptObj')
もしくは
correctiveShape.execute('deformObj', 'scluptObj', 'resultShapeName')
