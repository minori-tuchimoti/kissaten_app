import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Shop

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # ログインしていない時のリダイレクト先

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('ログイン成功！')
            return redirect(url_for('index'))
        else:
            flash('ユーザー名かパスワードが違います。')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('index'))

# 既存のloginルートの近くに追加するイメージです

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # ユーザー名やメールアドレスの重複チェック
        if User.query.filter_by(username=username).first():
            flash('そのユーザー名は既に使われています。')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('そのメールアドレスは既に使われています。')
            return redirect(url_for('register'))

        # 新規ユーザー作成
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/')
def index():
    areas = ["東京都", "神奈川県", "埼玉県", "千葉県"]

    if current_user.is_authenticated:
        # ログイン済みの場合は名前を表示しつつ、トップページ表示もする例
        welcome_message = f"ようこそ、{current_user.username}さん！"
        return render_template("index.html", areas=areas, welcome_message=welcome_message)
    else:
        # 未ログインの場合
        return render_template("index.html", areas=areas)
    

@app.route('/favorite/<shop_name>', methods=['POST'])
@login_required
def toggle_favorite(shop_name):
    shop = Shop.query.get(shop_name)
    if not shop:
        shop = Shop(name=shop_name)
        db.session.add(shop)

    if shop in current_user.favorites:
        current_user.favorites.remove(shop)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        current_user.favorites.append(shop)
        db.session.commit()
        return jsonify({'status': 'added'})


@app.route('/area/<area_name>')
def show_area(area_name):
    kissaten_data = {
        "東京都": ["物豆奇（ものずき）", "新宿珈琲店"],
        "神奈川県": ["横浜カフェ", "川崎喫茶"],
        "埼玉県": ["大宮喫茶", "川越珈琲館"],
        "千葉県": ["千葉珈琲店", "船橋カフェ"]
    }
    shops = kissaten_data.get(area_name, [])
    return render_template("area.html", area=area_name, shops=shops)

@app.route('/shop/<shop_name>')
def shop_detail(shop_name):
    shop_info = {
        "物豆奇（ものずき）": {
            "description": "〜中略〜",
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
    }
    info = shop_info.get(shop_name)
    if not info:
        return f"<h1>{shop_name} の情報が見つかりませんでした</h1>", 404

    favorite_names = []
    if current_user.is_authenticated:
        favorite_names = [s.name for s in current_user.favorites]

    return render_template("shop.html", shop_name=shop_name, info=info, area=info["area"], favorite_names=favorite_names)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # テーブルがなければ作る
    app.run(debug=True, host='0.0.0.0')