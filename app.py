import streamlit as st
import base64
import os
import csv
from datetime import datetime, timezone, timedelta

# ページの設定
st.set_page_config(page_title="頭部外傷後の注意 / Precautions", layout="centered")

# 画像読み込み関数
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    return ""

logo_base64 = get_image_base64("logo.png")
bg_base64 = get_image_base64("bg.jpg")

logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
bg_src = f"data:image/jpeg;base64,{bg_base64}" if bg_base64 else ""

# ---------------------------------------------
# ★ 画面全体に背景画像を広げるCSS
# ---------------------------------------------
page_bg_css = f"""
<style>
/* 画面全体（背景）の設定 */
[data-testid="stAppViewContainer"] {{
    background-image: url('{bg_src}');
    background-size: cover;      
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed; 
}}
/* 上部の余白（ヘッダー）を透明にする */
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
/* ログインフォームのデザイン */
div[data-testid="stForm"] {{
    background-color: rgba(255, 255, 255, 0.92);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2);
    border: none;
    margin-top: 5vh;
}}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# URLパラメータによる自動ログイン（QRコードから直接アクセスした場合）
if "pwd" in st.query_params and st.query_params["pwd"] == "nms1199":
    st.session_state.authenticated = True

# ---------------------------------------------
# 1. ロック画面 兼 案内記録フォーム
# ---------------------------------------------
if not st.session_state.authenticated:
    with st.form("login_and_record_form"):
        st.markdown("<h2 style='text-align: center; color: #1a365d;'>🔒 医療用パンフレット</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 14px;'>関係者用パスワードと、案内記録を入力してください。</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("#### 🔑 パスワード / Password")
        pwd_input = st.text_input("パスワードを入力", type="password", label_visibility="collapsed")
        
        st.markdown("<br>#### 📝 案内記録 / Record", unsafe_allow_html=True)
        doc_name = st.text_input("担当医師名 / Doctor's Name")
        pat_name = st.text_input("患者名（またはカルテ番号） / Patient's Name or ID")
        
        confirmed = st.checkbox("パンフレットの内容を案内し、確認しました / I have explained and confirmed the contents.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("記録を追加してパンフレットを表示 / Submit & View", use_container_width=True)
        
        if submit_btn:
            if pwd_input == "nms1199":
                # 入力チェック
                if not doc_name or not pat_name:
                    st.error("⚠️ 担当医師名と患者名を入力してください。")
                elif not confirmed:
                    st.error("⚠️ 確認のチェックボックスにチェックを入れてください。")
                else:
                    # Python標準機能を使ったCSV保存処理
                    JST = timezone(timedelta(hours=+9), 'JST') # 日本時間を設定
                    current_time = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
                    
                    csv_path = "records.csv"
                    file_exists = os.path.exists(csv_path)
                    
                    # CSVファイルに追記
                    with open(csv_path, mode='a', newline='', encoding='utf-8-sig') as f:
                        writer = csv.writer(f)
                        if not file_exists:
                            writer.writerow(["確認日時", "患者名", "担当医"]) # ヘッダー作成
                        writer.writerow([current_time, pat_name, doc_name]) # データ追記
                    
                    # 認証成功・画面切り替え
                    st.session_state.authenticated = True
                    st.rerun()
            else:
                st.error("❌ パスワードが間違っています。 / Incorrect password.")

# ---------------------------------------------
# 2. ポスター型コンテンツ画面（ログイン成功後）
# ---------------------------------------------
if st.session_state.authenticated:
    
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("ログアウト / Logout"):
            st.session_state.authenticated = False
            st.query_params.clear() # URLのパスワードを消去
            st.rerun()

    # CSSデザイン
    shared_css = """<style>
.poster-wrapper { background-color: #ffffff; padding: 20px; font-family: 'Helvetica Neue', Arial, sans-serif; color: #222; line-height: 1.8; font-size: 18px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); max-width: 850px; margin: auto; }
.header { border-bottom: 3px solid #1a365d; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: flex-end; }
.header h2 { margin: 0; font-size: 30px; color: #1a365d; font-weight: 900; }
.logo-img { height: 50px; object-fit: contain; }
.bg-section { background-image: url('BG_IMG_DATA'); background-size: cover; background-position: center; padding: 35px 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); text-align: center; }
.highlight { background-color: rgba(255, 255, 255, 0.75); padding: 15px; display: inline-block; font-size: 1.1em; line-height: 1.6; color: #000; border-radius: 8px; border: 1px solid rgba(255,255,255,0.3); text-align: left; }
.red-box { border: 3px solid #d32f2f; border-radius: 16px; background-color: #ffffff; padding: 25px 25px 15px 25px; margin: 30px 0; }
.red-box h4 { margin: 0 0 8px 0; font-size: 1.3em; color: #d32f2f; font-weight: bold; }
.red-box p { margin: 0 0 20px 25px; font-size: 1.05em; color: #333; line-height: 1.6; }
.bottom-section h3 { font-size: 1.35em; border-left: 6px solid #1a365d; padding-left: 12px; color: #1a365d; margin-bottom: 20px; font-weight: bold; }
.bottom-section ul { padding-left: 30px; margin: 0; }
.bottom-section li { margin-bottom: 15px; font-size: 1.05em; line-height: 1.7; }
@media (max-width: 768px) { 
    .pc-br { display: none; }
    .poster-wrapper { font-size: 15px; padding: 15px; }
    .header { flex-direction: column; align-items: center; gap: 10px; }
    .header h2 { font-size: 24px; text-align: center; }
    .logo-img { height: 40px; } 
    .bg-section { padding: 20px 15px; }
    .highlight { font-size: 1.05em; padding: 10px; }
    .red-box { padding: 15px; }
    .red-box p { margin: 0 0 15px 10px; }
}
</style>"""

    ja_content = f"""<div class="poster-wrapper"><div class="header"><h2>頭部外傷後の注意</h2><img class="logo-img" src="{logo_src}"></div>
    <div class="bg-section"><div class="highlight">頭を打った時には、脳にいろいろな変化が起ります。<br class="pc-br">数は少ないのですが、<strong>頭蓋骨（あたまの骨）の内側に出血が起ると<br class="pc-br">生命に危険</strong>をおよぼすことがありますので注意が必要です。<br><br>このような頭蓋内出血（頭の中の出血）の症状は、頭を打った後すぐ起る、<br class="pc-br">ときには数日、数ヶ月も経ってから起ることもあります。<br class="pc-br">ですから<strong>現在何も症状がなくても十分注意しなければなりません。</strong><br><br>頭を打ったのち、元気だった人が急に死亡したりすることがあるのは、<br class="pc-br">このような頭蓋内出血のためです。頭の骨に異常がないからといって<br class="pc-br">安心はできません。<br><br>そこで次に書いた注意をよく読んで、手おくれにならぬ内に、<br class="pc-br">患者さんを病院につれてくることが非常に重要です。</div></div>
    <div class="red-box"><h4>１．頭痛がだんだん強くなる時</h4><h4>２．吐き気や嘔吐が起る時</h4><p>（食べたものを吐いたり、何も食べないのに物を吐く）<br>（小児の場合は嘔吐をすぐしますが、それが数回にもおよぶ時）</p><h4>３．手足が動きにくくなったり、しびれたり、手に持ったものを取り落すことが多くなったりした時</h4><h4>４．ぼんやりしてくる時、あるいはほっておくとすぐ眠ってしまい起してもなかなか起きない時</h4><p>＊特に頭部打撲当日の夜は一度刺激をして起こして見て下さい。<br>（お子様は寝ついてしまうとわかりにくく注意が必要です。）</p><h4>５．全身・手・足等のけいれん（ひきつけ）が起る時</h4></div>
    <div class="bottom-section"><h3>頭部打撲後の注意</h3><ul><li>小さい子供さんは、相当強く頭を打った時でも、症状が出にくいことが多いので、たとえ元気にしていても１〜２日は目をはなさないことが大切です。</li><li>あたまを打ったのちは、少なくとも２〜３日は安静を保ち、１人で外出したり、過労をしないように注意して下さい。</li><li>また病院へ患者さんを運ぶ時には、出来れば前もって連絡し、出来るだけ振動の少ない乗物で、短時間に運んで下さい。<br>神経質になることはいりませんが、以上の注意をお守り下さい。</li></ul></div></div>"""

    en_content = f"""<div class="poster-wrapper"><div class="header"><h2>Precautions After a Head Injury</h2><img class="logo-img" src="{logo_src}"></div>
    <div class="bg-section"><div class="highlight">Various changes can occur in the brain when you hit your head.<br class="pc-br">Although rare, <strong>bleeding inside the skull can be life-threatening</strong>,<br class="pc-br">so caution is required.<br><br>Symptoms of such intracranial hemorrhage (bleeding inside the head)<br class="pc-br">may appear immediately after hitting the head, 1 to 2 days later, or even much later.<br class="pc-br">Therefore, <strong>you must be very careful even if you currently have no symptoms.</strong><br><br>This type of intracranial hemorrhage is the reason why someone who<br class="pc-br">seemed fine might suddenly pass away. You cannot let your guard down<br class="pc-br">just because there are no bone abnormalities.<br><br>Therefore, it is extremely important to carefully read the precautions<br class="pc-br">below and bring the patient to the hospital before it is too late.</div></div>
    <div class="red-box"><h4>1. When a headache gradually worsens</h4><h4>2. When experiencing nausea or vomiting</h4><p>(Throwing up food, or retching even when eating nothing)<br>(Children often vomit easily, but pay attention if it happens multiple times)</p><h4>3. When arms or legs become difficult to move, feel numb, or if the patient frequently drops things they are holding</h4><h4>4. When the patient becomes dazed, or falls asleep immediately if left alone and is difficult to wake up</h4><p>* Especially on the night of the head injury, please try to wake them up once by gently stimulating them.<br>(Caution is needed with children, as it can be difficult to tell once they fall asleep.)</p><h4>5. When convulsions (seizures) occur</h4></div>
    <div class="bottom-section"><h3>Precautions After Hitting Your Head</h3><ul><li>Small children often do not show symptoms easily even when they hit their heads quite hard. Therefore, it is important to keep a close eye on them for 1 to 2 days, even if they seem fine.</li><li>After hitting your head, please rest for at least 2 to 3 days, and avoid going out alone or overexerting yourself.</li><li>When bringing the patient to the hospital, please contact the hospital in advance if possible, and transport them quickly using a vehicle with as little vibration as possible.<br>There is no need to be overly anxious, but please be sure to follow the above precautions.</li></ul></div></div>"""

    final_ja = shared_css + ja_content.replace("BG_IMG_DATA", bg_src)
    final_en = shared_css + en_content.replace("BG_IMG_DATA", bg_src)

    tab_ja, tab_en = st.tabs(["日本語", "English"])
    with tab_ja:
        st.markdown(final_ja, unsafe_allow_html=True)
    with tab_en:
        st.markdown(final_en, unsafe_allow_html=True)

    # ---------------------------------------------
    # 3. CSVダウンロードエリア（スタッフ用）
    # ---------------------------------------------
    if os.path.exists("records.csv"):
        st.markdown("<br><br>", unsafe_allow_html=True)
        with open("records.csv", "rb") as f:
            st.download_button("📥 【医療スタッフ用】説明記録データ(CSV)をダウンロード", f, file_name="records.csv")
