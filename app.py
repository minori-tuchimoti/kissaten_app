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
        "東京都": ["銀座カフェ", "新宿珈琲店"],
        "神奈川県": ["横浜カフェ", "川崎喫茶"],
        "埼玉県": ["大宮喫茶", "川越珈琲館"],
        "千葉県": ["千葉珈琲店", "船橋カフェ"]
    }

    shops = kissaten_data.get(area_name, [])  # 対象の都道府県の喫茶店を取得
    return render_template("area.html", area=area_name, shops=shops)

if __name__ == '__main__':  # このファイルが直接実行されたときだけ以下を実行
    app.run(debug=True, host='0.0.0.0')
    # Flaskアプリを起動（debug=Trueでエラーが見やすくなる、0.0.0.0でCloud9からアクセス可能に）
