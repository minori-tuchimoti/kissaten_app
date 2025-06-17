from flask import Flask, render_template  # Flaskの本体と、HTMLテンプレートを使う機能を読み込む

app = Flask(__name__)  # Flaskアプリケーションの本体を作成。この変数 app がアプリの中核

@app.route('/')  # URLが「/」（＝トップページ）にアクセスされたときの処理を定義
def index():
    areas = ["東京都", "神奈川県", "埼玉県", "千葉県"]  # 都道府県名のリストを作成
    return render_template("index.html", areas=areas)
    # index.html（テンプレート）にareasリストを渡して表示する

@app.route('/area/<area_name>')
def show_area(area_name):
    # 仮データ：都道府県ごとの喫茶店リスト
    kissaten_data = {
        "東京都": ["物豆奇（ものずき）", "新宿珈琲店"],
        "神奈川県": ["横浜カフェ", "川崎喫茶"],
        "埼玉県": ["大宮喫茶", "川越珈琲館"],
        "千葉県": ["千葉珈琲店", "船橋カフェ"]
    }

    shops = kissaten_data.get(area_name, [])  # 対象の都道府県の喫茶店を取得
    return render_template("area.html", area=area_name, shops=shops)

@app.route('/shop/<shop_name>')
def shop_detail(shop_name):
    # サンプル喫茶店データ（名前・説明・緯度・経度）
    shop_info = {
        "物豆奇（ものずき）": {
            "description": """　店名からして一方ならぬこだわりを感じさせる「物豆奇」は、初代が国立にあった喫茶店「邪宗門」をモデルに、自身の趣味をたっぷりと詰め込んで作り上げた店だ。
                              古材を多用した店内には、無数の柱時計やアンティークランプが飾られており、まるで不思議の国に迷い込んだかのような錯覚を覚える。創業時にオーダーメイドで作られたというモダンな鉄製のテーブルがあるかと思えば、奥には囲炉裏もあり、座る席ごとに異なる景色や雰囲気が楽しめる。
                              　コーヒー豆は主に創業時から付き合いのある神保町の「倉木コーヒー」から仕入れ、注文ごとに一杯ずつ丁寧にドリップするのがこだわり。異次元の世界に心を遊ばせながら、非日常のひとときを過ごしたい。""",
            "address": "東京都杉並区西荻南3-17-5",
            "phone": "03-3395-9569",
            "hours": "11:30〜20:00",
            "closed": "不定休",
            "seats": "15席",
            "card": "不可",
            "smoking": "禁煙",
            "access": "JR西荻窪駅より徒歩約5分",
            "images": ["monozuki1.jpg", "monozuki2.jpg", "monozuki3.jpg"],
            "lat": 35.705426,
            "lng": 139.596931,
            "area": "東京都"
        },
        "新宿珈琲店": {
            "description": "新宿駅徒歩2分。昔ながらの喫茶店。",
            "lat": 35.6896,
            "lng": 139.7006,
            "area": "東京都"
        },
        # ここにどんどん追加できます
    }

    info = shop_info.get(shop_name)
    if not info:
        return f"<h1>{shop_name} の情報が見つかりませんでした</h1>", 404

    return render_template("shop.html", shop_name=shop_name, info=info, area=info["area"])

if __name__ == '__main__':  # このファイルが直接実行されたときだけ以下を実行
    app.run(debug=True, host='0.0.0.0')
    # Flaskアプリを起動（debug=Trueでエラーが見やすくなる、0.0.0.0でCloud9からアクセス可能に）
