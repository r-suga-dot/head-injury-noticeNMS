import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import datetime
import requests
import extra_streamlit_components as stx

# ページの設定
st.set_page_config(page_title="頭部外傷後の注意 / Precautions", layout="centered")

# ==========================================
# 📝 スプレッドシート記録用の設定
# ==========================================
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeyLSwiQrUYWlQtUCYAc_mc4JZgIwlI6gK149bMQWIfYekZ1A/formResponse"
ENTRY_DOCTOR = "entry.629282236" 
ENTRY_PATIENT = "entry.2140844596" 

# ==========================================
# 🍪 Cookie（ログイン保持）の設定
# ==========================================
cookie_manager = stx.CookieManager(key="cookie_manager")
cookies = cookie_manager.get_all()

# セッション状態の初期化（Cookieに記録があればログイン済みにする）
if "authenticated" not in st.session_state:
    st.session_state.authenticated = cookies.get("auth_status") == "True"

# ---------------------------------------------
# 1. ログイン 兼 案内記録フォーム画面
# ---------------------------------------------
if not st.session_state.authenticated:
    st.title("🔒 頭部外傷パンフレット")
    st.write("関係者用パスワードと、案内記録を入力してください。")
    
    with st.form("login_and_signature_form"):
        st.subheader("🔑 パスワード / Password")
        password_input = st.text_input("パスワードを入力", type="password")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.subheader("📝 案内記録 / Record")
        doctor_name = st.text_input("担当医師名 / Doctor's Name")
        patient_name = st.text_input("患者名（またはカルテ番号） / Patient's Name or ID")
        confirm_check = st.checkbox("パンフレットの内容を案内し、確認しました / I have explained and confirmed the contents.")
        
        submitted = st.form_submit_button("記録を送信してパンフレットを表示 / Submit & View")
        
        if submitted:
            if password_input != "nms1199":
                st.error("パスワードが間違っています。 / Incorrect password.")
            elif not doctor_name or not patient_name or not confirm_check:
                st.error("すべての項目に入力・チェックを入れてください。 / Please fill in all fields.")
            else:
                # ① Googleフォームにデータを送信
                payload = {
                    ENTRY_DOCTOR: doctor_name,
                    ENTRY_PATIENT: patient_name
                }
                try:
                    requests.post(GOOGLE_FORM_URL, data=payload)
                except Exception:
                    pass 
                
                # ② ログイン状態をCookieに記憶（有効期限：365日）
                st.session_state.authenticated = True
                cookie_manager.set("auth_status", "True", expires_at=datetime.datetime.now() + datetime.timedelta(days=365))
                
                st.success("✅ 記録を保存しました。パンフレットを表示します...")
                import time
                time.sleep(1.5)
                st.rerun()

# ---------------------------------------------
# 2. ポスター型コンテンツ画面
# ---------------------------------------------
if st.session_state.authenticated:
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("ログアウト / Logout"):
            cookie_manager.delete("auth_status")
            st.session_state.authenticated = False
            st.rerun()

    def get_image_base64(file_path):
        if os.path.exists(file_path):
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return ""

    logo_b64 = get_image_base64("logo.png")
    bg_b64 = get_image_base64("bg.jpg")

    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""
    bg_src = f"data:image/jpeg;base64,{bg_b64}" if bg_b64 else ""

    # CSSデザイン（1枚に収まるように余白・行間を少し詰める）
    shared_css = """<style>
.poster-wrapper { background-color: #ffffff; padding: 15px; font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif; color: #222; line-height: 1.6; font-size: 16px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); max-width: 850px; margin: auto; }
.header { border-bottom: 3px solid #1a365d; padding-bottom: 10px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: flex-end; }
.header h2 { margin: 0; font-size: 26px; color: #1a365d; font-weight: 900; letter-spacing: 1px; }
.logo-img { height: 40px; object-fit: contain; }
.bg-section { background-image: url('BG_IMG_HOLDER'); background-size: cover; background-position: center; padding: 25px 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); text-align: center; }
.highlight-container { text-align: left; display: inline-block; }
.highlight { background-color: rgba(255, 255, 255, 0.88); padding: 2px 6px; font-size: 1.05em; display: inline; box-decoration-break: clone; -webkit-box-decoration-break: clone; line-height: 1.8; color: #000; }
.bg-section p { margin: 0 0 12px 0; }
.red-box { border: 3px solid #d32f2f; border-radius: 12px; background-color: #ffffff; padding: 15px 20px 10px 20px; margin: 20px 0; }
.red-box h4 { margin: 0 0 5px 0; font-size: 1.2em; color: #d32f2f; font-weight: bold; }
.red-box p { margin: 0 0 12px 20px; font-size: 0.95em; color: #333; line-height: 1.5; }
.bottom-section h3 { font-size: 1.2em; border-left: 6px solid #1a365d; padding-left: 10px; color: #1a365d; margin-bottom: 12px; font-weight: bold; }
.bottom-section ul { padding-left: 25px; margin: 0; }
.bottom-section li { margin-bottom: 8px; font-size: 0.95em; line-height: 1.6; }

@media (max-width: 768px) { 
    .pc-br { display: none; }
    .poster-wrapper { font-size: 14px; padding: 10px; }
    .header { flex-direction: column; align-items: center; gap: 8px; padding-bottom: 8px; margin-bottom: 12px; }
    .header h2 { font-size: 20px; text-align: center; }
    .logo-img { height: 35px; } 
    .bg-section { padding: 15px 12px; margin-bottom: 15px; }
    .highlight { font-size: 1em; padding: 2px 4px; line-height: 1.6; }
    .red-box { padding: 12px 15px 8px 15px; margin: 15px 0; }
    .red-box h4 { font-size: 1.1em; }
    .red-box p { margin: 0 0 10px 15px; font-size: 0.9em; }
    .bottom-section h3 { font-size: 1.1em; margin-bottom: 10px; }
    .bottom-section ul { padding-left: 20px; }
    .bottom-section li { font-size: 0.9em; margin-bottom: 8px; }
}

/* PDF保存時の設定（A4・1枚に収める工夫） */
@media print {
    @page { size: A4 portrait; margin: 10mm; }
    button, .stTabs [data-baseweb="tab-list"], iframe { display: none !important; }
    .poster-wrapper { box-shadow: none; border: none; padding: 0; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>"""

    ja_html = """
<div class="poster-wrapper">
<div class="header">
<h2>頭部外傷後の注意</h2>
<img class="logo-img" src="LOGO_IMG_HOLDER" alt="病院ロゴ">
</div>
<div class="bg-section">
<div class="highlight-container">
<p><span class="highlight">頭を打った時には、脳にいろいろな変化が起ります。<br class="pc-br">数は少ないのですが、<strong>頭蓋骨（あたまの骨）の内側に出血が</strong><br class="pc-br"><strong>起ると生命に危険</strong>をおよぼすことがありますので注意が必要です。</span></p>
<p><span class="highlight">このような頭蓋内出血（頭の中の出血）の症状は、<br class="pc-br">頭を打った後すぐ起る、ときには数日、数ヶ月も経ってから<br class="pc-br">起ることもあります。ですから<strong>現在何も症状がなくても十分</strong><br class="pc-br"><strong>注意しなければなりません。</strong></span></p>
<p><span class="highlight">頭を打ったのち、元気だった人が急に死亡したりすることが<br class="pc-br">あるのは、このような頭蓋内出血のためです。頭の骨に異常がない<br class="pc-br">からといって安心はできません。</span></p>
<p><span class="highlight">そこで次に書いた注意をよく読んで、手おくれにならぬ内に、<br class="pc-br">患者さんを病院につれてくることが非常に重要です。</span></p>
</div>
</div>
<div class="red-box">
<h4>１．頭痛がだんだん強くなる時</h4>
<h4>２．吐き気や嘔吐が起る時</h4>
<p>（食べたものを吐いたり、何も食べないのに物を吐く）<br>（小児の場合は嘔吐をすぐしますが、それが数回にもおよぶ時）</p>
<h4>３．手足が動きにくくなったり、しびれたり、<br class="pc-br">  手に持ったものを取り落すことが多くなったりした時</h4>
<h4>４．ぼんやりしてくる時、あるいはほっておくと<br class="pc-br">  すぐ眠ってしまい起してもなかなか起きない時</h4>
<p>＊特に頭部打撲当日の夜は一度刺激をして起こして見て下さい。<br>（お子様は寝ついてしまうとわかりにくく注意が必要です。）</p>
<h4>５．全身・手・足等のけいれん（ひきつけ）が起る時</h4>
</div>
<div class="bottom-section">
<h3>頭部打撲後の注意</h3>
<ul>
<li>小さい子供さんは、相当強く頭を打った時でも、症状が出にくいことが多いので、たとえ元気にしていても１〜２日は目をはなさないことが大切です。</li>
<li>あたまを打ったのちは、少なくとも２〜３日は安静を保ち、１人で外出したり、過労をしないように注意して下さい。</li>
<li>また病院へ患者さんを運ぶ時には、出来れば前もって連絡し、出来るだけ振動の少ない乗物で、短時間に運んで下さい。<br>神経質になることはいりませんが、以上の注意をお守り下さい。</li>
</ul>
</div>
</div>"""

    en_html = """
<div class="poster-wrapper">
<div class="header">
<h2>Precautions After a Head Injury</h2>
<img class="logo-img" src="LOGO_IMG_HOLDER" alt="Hospital Logo">
</div>
<div class="bg-section">
<div class="highlight-container">
<p><span class="highlight">Various changes can occur in the brain when you hit your head.<br class="pc-br">Although rare, <strong>bleeding inside the skull can be life-threatening</strong>,<br class="pc-br">so caution is required.</span></p>
<p><span class="highlight">Symptoms of such intracranial hemorrhage (bleeding inside the head)<br class="pc-br">may appear immediately after hitting the head, 1 to 2 days later, or even much later.<br class="pc-br">Therefore, <strong>you must be very careful even if you currently have no symptoms.</strong></span></p>
<p><span class="highlight">This type of intracranial hemorrhage is the reason why someone who<br class="pc-br">seemed fine might suddenly pass away. You cannot let your guard down<br class="pc-br">just because there are no bone abnormalities.</span></p>
<p><span class="highlight">Therefore, it is extremely important to carefully read the precautions<br class="pc-br">below and bring the patient to the hospital before it is too late.</span></p>
</div>
</div>
<div class="red-box">
<h4>1. When a headache gradually worsens</h4>
<h4>2. When experiencing nausea or vomiting</h4>
<p>(Throwing up food, or retching even when eating nothing)<br>(Children often vomit easily, but pay attention if it happens multiple times)</p>
<h4>3. When arms or legs become difficult to move, feel numb,<br class="pc-br">  or if the patient frequently drops things they are holding</h4>
<h4>4. When the patient becomes dazed, or falls asleep immediately<br class="pc-br">  if left alone and is difficult to wake up</h4>
<p>* Especially on the night of the head injury, please try to wake them up once by gently stimulating them.<br>(Caution is needed with children, as it can be difficult to tell once they fall asleep.)</p>
<h4>5. When convulsions (seizures) occur</h4>
</div>
<div class="bottom-section">
<h3>Precautions After Hitting Your Head</h3>
<ul>
<li>Small children often do not show symptoms easily even when they hit their heads quite hard. Therefore, it is important to keep a close eye on them for 1 to 2 days, even if they seem fine.</li>
<li>After hitting your head, please rest for at least 2 to 3 days, and avoid going out alone or overexerting yourself.</li>
<li>When bringing the patient to the hospital, please contact the hospital in advance if possible, and transport them quickly using a vehicle with as little vibration as possible.<br>There is no need to be overly anxious, but please be sure to follow the above precautions.</li>
</ul>
</div>
</div>"""

    final_ja = (shared_css + ja_html).replace("LOGO_IMG_HOLDER", logo_src).replace("BG_IMG_HOLDER", bg_src)
    final_en = (shared_css + en_html).replace("LOGO_IMG_HOLDER", logo_src).replace("BG_IMG_HOLDER", bg_src)

    tab_ja, tab_en = st.tabs(["日本語", "English"])
    
    with tab_ja:
        st.markdown(final_ja, unsafe_allow_html=True)
        
    with tab_en:
        st.markdown(final_en, unsafe_allow_html=True)

    # ---------------------------------------------
    # 3. PDF保存ボタンの追加（文言変更）
    # ---------------------------------------------
    st.write("") # スペース空け
    components.html(
        """
        <div style="text-align: center; margin-top: 10px;">
            <button onclick="window.parent.print()" style="padding: 12px 24px; font-size: 16px; border-radius: 8px; background-color: #1a365d; color: white; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                📄 画面をPDFで保存する / Save as PDF
            </button>
            <p style="font-size: 12px; color: #666; margin-top: 10px; font-family: sans-serif;">
                ※スマートフォンの場合は、表示されるメニューから「PDFに保存」を選択してください。
            </p>
        </div>
        """,
        height=100
    )
