import pyxel # pyxelライブラリをインポート（使えるように）します
class Ball: # Ball（ボール）の設計図となるクラスを定義します
    speed = 1 # クラス変数speedを1で初期化します。すべてのボールでこの速度を共有します
    
    def __init__(self): # Ballクラスのインスタンス（実体）が作られるときに呼ばれる初期化メソッドです
        self.restart() # インスタンス作成時にrestartメソッドを呼び出し、ボールを初期位置にセットします
        
    def move(self): # ボールを動かす処理をまとめたメソッドです
        self.x += self.vx * Ball.speed # ボールのx座標を、x方向の速度(vx)と共有speedを掛けた分だけ動かします
        self.y += self.vy * Ball.speed # ボールのy座標を、y方向の速度(vy)と共有speedを掛けた分だけ動かします
        if (self.x < 0) or (self.x >= field_size): # もしボールが左壁(0未満)または右壁(field_size以上)に当たったら
            self.vx = -self.vx # x方向の速度(vx)を反転させます（跳ね返り）
    def restart(self): # ボールをリセット（初期位置に戻す）するメソッドです
        self.x = pyxel.rndi(0, field_size - 1) # x座標を、0からfield_size-1の間のランダムな整数に設定します
        self.y = 0 # y座標を、画面の一番上(0)に設定します
        angle = pyxel.rndi(30, 150) # 角度を30度から150度の間のランダムな整数に設定します (下向きの範囲)
        self.vx = pyxel.cos(angle) # その角度のコサイン(cos)を計算し、x方向の速度(vx)とします
        self.vy = pyxel.sin(angle) # その角度のサイン(sin)を計算し、y方向の速度(vy)とします
        
class Pad: # Pad（プレイヤーが操作するパッド）の設計図となるクラスを定義します
    def __init__(self): # Padクラスのインスタンスが作られるときに呼ばれる初期化メソッドです
        self.x = field_size / 2 # パッドの初期x座標を、フィールドの中央に設定します
        self.size = field_size / 5 # パッドの幅(size)を、フィールドサイズの 1/5 に設定します
    def catch(self, ball): #受け取れたらTrue, そうでなければFalseを返す (ボールをキャッチしたか判定するメソッドです)
        if ball.y >= field_size-field_size/40 and (self.x-self.size/2 <= ball.x <= self.x+self.size/2): # もしボールのy座標がパッドの位置にあり、かつボールのx座標がパッドの範囲内（パッドの左端から右端の間）なら
            pyxel.play(0, 0) # チャンネル0でサウンド0（キャッチ音）を再生します
            ball.restart() # キャッチしたボール(ball)のrestartメソッドを呼び出します
            return True # キャッチ成功としてTrue（真）を返します
        else: # 上記ifの条件に当てはまらない（キャッチしていない）場合
            return False # キャッチ失敗としてFalse（偽）を返します
field_size = 150 # ゲーム画面のサイズ（幅・高さ）を150ピクセルに設定する変数
pyxel.init(field_size,field_size) # 150x150ピクセルのpyxelウィンドウを作成（初期化）します
pyxel.sound(0).set(notes='A2C3', tones='TT', volumes='33', effects='NN', speed=10) # サウンドID 0番（キャッチ音）の音色等を設定します
pyxel.sound(1).set(notes='C2', tones='N', volumes='3', effects='S', speed=30) # サウンドID 1番（ミス音）の音色等を設定します
balls = [Ball()] # Ballクラスのインスタンスを1つだけ入れたリスト `balls` を作成します
pad = Pad() # Padクラスのインスタンスを1つ作成し、変数 `pad` に入れます
alive = True # ゲームが続行中かどうかを示すフラグ（True = 続行中）を管理する変数
life = 10 # プレイヤーの残りライフを10で初期化する変数
receive = 0 # ボールを連続でキャッチした回数を記録する変数
score = 0 # プレイヤーのスコアを0で初期化する変数
def update(): # 毎フレームのゲーム状態の更新処理を定義する関数
    global balls, pad, score, alive, life, receive # 関数内でグローバル変数（関数の外で定義された変数）を変更することを宣言します
    if not alive: # もし `alive` が True でない（= False ゲームオーバー）なら
        return # このupdate関数をここで終了します（以下の処理は行いません）
    pad.x = pyxel.mouse_x # `pad` のx座標を、現在のマウスカーソルのx座標に更新します
    for b in balls: # `balls` リストに入っているすべてのボール（b）に対して繰り返し処理を行います
        b.move() # そのボール（b）のmoveメソッドを呼び出して動かします
        
        if pad.catch(b): #受け取れたら (もし `pad` がそのボール(b)をキャッチしたら)
            Ball.speed += 0.2 # すべてのボールで共有している `speed` を 0.2 増やします
            score += 1 # スコアを 1 点加算します
            receive += 1 # 連続キャッチ回数を 1 増やします
            if receive >= 10: # もし連続キャッチ回数が 10 回以上になったら
                Ball.speed = 1 # ボールの `speed` を 1 にリセットします
                receive = 0 # 連続キャッチ回数を 0 にリセットします
                balls.append(Ball()) # `balls` リストに新しい `Ball` インスタンスを追加します（ボールが増える）
        
        elif b.y >= field_size: # (キャッチできず) もしボールのy座標が画面下端(field_size)以上になったら
            pyxel.play(0, 1) # チャンネル0でサウンド1（ミス音）を再生します
            b.restart() # そのボール（b）のrestartメソッドを呼び出してリセットします
            Ball.speed += 0.2 # ボールの `speed` を 0.2 増やします（ミスしても速くなる仕様）
            life -= 1 # ライフを 1 減らします
            alive = (life > 0) # ライフが 0 より大きいか判定し、結果を `alive` に代入します (0以下になるとFalse)
        
def draw(): # 毎フレームの描画処理を定義する関数
    global balls, pad, score, alive # 関数内でグローバル変数を参照することを宣言します
    if alive: # もし `alive` が True（ゲーム続行中）なら
        pyxel.cls(7) # 画面全体を色 7 (デフォルトでは白) で塗りつぶします
        for b in balls: # `balls` リストに入っているすべてのボール（b）に対して繰り返し処理を行います
            pyxel.circ(b.x, b.y, field_size/20, 6) # ボール(b)を (x, y) 座標に、半径 (field_size/20)、色 6 (赤) の円として描画します
        pyxel.rect(pad.x-pad.size/2, field_size-field_size/40, pad.size, 5, 14) # パッドを描画します (左上のx, 左上のy, 幅, 高さ, 色 14 (黄))
        pyxel.text(5, 5, "score: " + str(score), 0) # 座標 (5, 5) に "score: " と現在のスコアを文字列にして、色 0 (黒) で描画します
    else: # もし `alive` が False（ゲームオーバー）なら
        pyxel.text(field_size/2-20, field_size/2-20, "Game Over!!!", 0) # 画面中央付近に "Game Over!!!" と色 0 (黒) で描画します
pyxel.run(update, draw) # `update` 関数を更新処理、`draw` 関数を描画処理として登録し、pyxelアプリケーションを実行（ゲームスタート）します