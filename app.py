import streamlit as st
import base64
import os

# ページの設定
st.set_page_config(page_title="頭部外傷後の注意", layout="centered")

# セッション状態の初期化
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# パスワード確認の関数
def check_password():
    CORRECT_PASSWORD = "nms1199" 
    if st.session_state.password_input == CORRECT_PASSWORD:
        st.session_state.authenticated = True
        st.session_state.password_error = False
    else:
        st.session_state.authenticated = False
        st.session_state.password_error = True

# ---------------------------------------------
# 1. パスワード入力画面
# ---------------------------------------------
if not st.session_state.authenticated:
    st.title("🔒 医療用パンフレット（関係者限定）")
    st.write("配布されたQRコードに付属のパスワードを入力してください。")
    st.text_input("パスワード / Password", type="password", key="password_input", on_change=check_password)
    if "password_error" in st.session_state and st.session_state.password_error:
        st.error("パスワードが間違っています。 / Incorrect password.")

# ---------------------------------------------
# 2. ポスター型コンテンツ画面
# ---------------------------------------------
if st.session_state.authenticated:
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("ログアウト / Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # 画像読み込み関数（念のためパス確認を強化）
    def get_image_base64(file_path):
        if os.path.exists(file_path):
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            return "" # ファイルが見つからない場合は空文字

    # 画像データを取得
    logo_base64 = get_image_base64("logo.png")
    bg_base64 = get_image_base64("bg.jpg")
    
    logo_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
    bg_src = f"data:image/jpeg;base64,{bg_base64}" if bg_base64 else ""

    # CSSデザイン（背景を確実に表示）
    shared_css = """<style>
.poster-wrapper { background-color: #ffffff; padding: 20px; font-family: 'Helvetica Neue', Arial, sans-serif; color: #222; line-height: 1.8; font-size: 18px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); max-width: 850px; margin: auto; }
.header { border-bottom: 3px solid #1a365d; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: flex-end; }
.header h2 { margin: 0; font-size: 30px; color: #1a365d; font-weight: 900; }
.logo-img { height: 50px; object-fit: contain; }
.bg-section { background-image: url('BG_IMG_DATA'); background-size: cover; background-position: center; padding: 35px 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); text-align: center; }
.highlight { background-color: rgba(255, 255, 255, 0.85); padding: 5px 10px; display: inline-block; font-size: 1.1em; color: #000; border-radius: 4px; text-align: left; }
.red-box { border: 3px solid #d32f2f; border-radius: 16px; background-color: #ffffff; padding: 25px 25px 15px 25px; margin: 30px 0; }
.red-box h4 { margin: 0 0 8px 0; font-size: 1.3em; color: #d32f2f; font-weight: bold; }
.red-box p { margin: 0 0 20px 25px; font-size: 1.05em; color: #333; line-height: 1.6; }
.bottom-section h3 { font-size: 1.35em; border-left: 6px solid #1a365d; padding-left: 12px; color: #1a365d; margin-bottom: 20px; font-weight: bold; }
.bottom-section ul { padding-left: 30px; margin: 0; }
.bottom-section li { margin-bottom: 15px; font-size: 1.05em; line-height: 1.7; }
</style>"""

    # 日本語コンテンツ
    ja_content = f"""<div class="poster-wrapper"><div class="header"><h2>頭部外傷後の注意</h2><img class="logo-img" src="{logo_src}"></div>
    <div class="bg-section"><div class="highlight">頭を打った時には、脳にいろいろな変化が起ります。数は少ないのですが、<strong>頭蓋骨（あたまの骨）の内側に出血が起ると生命に危険</strong>をおよぼすことがありますので注意が必要です。<br><br>このような頭蓋内出血（頭の中の出血）の症状は、頭を打った後すぐ起る、ときには数日、数ヶ月も経ってから起ることもあります。ですから<strong>現在何も症状がなくても十分注意しなければなりません。</strong><br><br>頭を打ったのち、元気だった人が急に死亡したりすることがあるのは、このような頭蓋内出血のためです。頭の骨に異常がないからといって安心はできません。<br><br>そこで次に書いた注意をよく読んで、手おくれにならぬ内に、患者さんを病院につれてくることが非常に重要です。</div></div>
    <div class="red-box"><h4>１．頭痛がだんだん強くなる時</h4><h4>２．吐き気や嘔吐が起る時</h4><p>（食べたものを吐いたり、何も食べないのに物を吐く）<br>（小児の場合は嘔吐をすぐしますが、それが数回にもおよぶ時）</p><h4>３．手足が動きにくくなったり、しびれたり、手に持ったものを取り落すことが多くなったりした時</h4><h4>４．ぼんやりしてくる時、あるいはほっておくとすぐ眠ってしまい起してもなかなか起きない時</h4><p>＊特に頭部打撲当日の夜は一度刺激をして起こして見て下さい。<br>（お子様は寝ついてしまうとわかりにくく注意が必要です。）</p><h4>５．全身・手・足等のけいれん（ひきつけ）が起る時</h4></div>
    <div class="bottom-section"><h3>頭部打撲後の注意</h3><ul><li>小さい子供さんは、相当強く頭を打った時でも、症状が出にくいことが多いので、たとえ元気にしていても１〜２日は目をはなさないことが大切です。</li><li>あたまを打ったのちは、少なくとも２〜３日は安静を保ち、１人で外出したり、過労をしないように注意して下さい。</li><li>また病院へ患者さんを運ぶ時には、出来れば前もって連絡し、出来るだけ振動の少ない乗物で、短時間に運んで下さい。<br>神経質になることはいりませんが、以上の注意をお守り下さい。</li></ul></div></div>"""

    # 英語コンテンツ
    en_content = f"""<div class="poster-wrapper"><div class="header"><h2>Precautions After a Head Injury</h2><img class="logo-img" src="{logo_src}"></div>
    <div class="bg-section"><div class="highlight">Various changes can occur in the brain when you hit your head. Although rare, <strong>bleeding inside the skull can be life-threatening</strong>, so caution is required.<br><br>Symptoms of such intracranial hemorrhage (bleeding inside the head) may appear immediately after hitting the head, 1 to 2 days later, or even much later. Therefore, <strong>you must be very careful even if you currently have no symptoms.</strong><br><br>This type of intracranial hemorrhage is the reason why someone who seemed fine might suddenly pass away. You cannot let your guard down just because there are no bone abnormalities.<br><br>Therefore, it is extremely important to carefully read the precautions below and bring the patient to the hospital before it is too late.</div></div>
    <div class="red-box"><h4>1. When a headache gradually worsens</h4><h4>2. When experiencing nausea or vomiting</h4><p>(Throwing up food, or retching even when eating nothing)<br>(Children often vomit easily, but pay attention if it happens multiple times)</p><h4>3. When arms or legs become difficult to move, feel numb, or if the patient frequently drops things they are holding</h4><h4>4. When the patient becomes dazed, or falls asleep immediately if left alone and is difficult to wake up</h4><p>* Especially on the night of the head injury, please try to wake them up once by gently stimulating them.<br>(Caution is needed with children, as it can be difficult to tell once they fall asleep.)</p><h4>5. When convulsions (seizures) occur</h4></div>
    <div class="bottom-section"><h3>Precautions After Hitting Your Head</h3><ul><li>Small children often do not show symptoms easily even when they hit their heads quite hard. Therefore, it is important to keep a close eye on them for 1 to 2 days, even if they seem fine.</li><li>After hitting your head, please rest for at least 2 to 3 days, and avoid going out alone or overexerting yourself.</li><li>When bringing the patient to the hospital, please contact the hospital in advance if possible, and transport them quickly using a vehicle with as little vibration as possible.<br>There is no need to be overly anxious, but please be sure to follow the above precautions.</li></ul></div></div>"""

    # HTMLの組み立て（ここで背景画像を注入）
    final_ja = shared_css + ja_content.replace("BG_IMG_DATA", bg_src)
    final_en = shared_css + en_content.replace("BG_IMG_DATA", bg_src)

    # タブ名変更
    tab_ja, tab_en = st.tabs(["日本語", "English"])
    
    with tab_ja:
        st.markdown(final_ja, unsafe_allow_html=True)
        
    with tab_en:
        st.markdown(final_en, unsafe_allow_html=True)
