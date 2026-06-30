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
# 1. パスワード入力画面（未ログイン時）
# ---------------------------------------------
if not st.session_state.authenticated:
    st.title("🔒 医療用パンフレット（関係者限定）")
    st.write("配布されたQRコードに付属のパスワードを入力してください。")
    st.text_input("パスワード", type="password", key="password_input", on_change=check_password)
    if "password_error" in st.session_state and st.session_state.password_error:
        st.error("パスワードが間違っています。")

# ---------------------------------------------
# 2. ポスター型コンテンツ画面（ログイン成功時）
# ---------------------------------------------
if st.session_state.authenticated:
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("ログアウト"):
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

    # PPTに合わせた改行とフォントサイズ、ハイライト装飾に修正（空行なし）
    poster_html = """<style>
.poster-wrapper { background-color: #ffffff; padding: 20px; font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif; color: #222; line-height: 1.8; font-size: 18px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); max-width: 850px; margin: auto; }
.header { border-bottom: 3px solid #1a365d; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: flex-end; }
.header h2 { margin: 0; font-size: 30px; color: #1a365d; font-weight: 900; letter-spacing: 1px; }
.logo-img { height: 50px; object-fit: contain; }
.bg-section { background-image: url('BG_IMG_HOLDER'); background-size: cover; background-position: center; padding: 35px 25px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); text-align: center; }
.highlight-container { text-align: left; display: inline-block; }
.highlight { background-color: rgba(255, 255, 255, 0.88); padding: 4px 8px; font-size: 1.1em; display: inline; box-decoration-break: clone; -webkit-box-decoration-break: clone; line-height: 1.95; color: #000; }
.bg-section p { margin: 0 0 18px 0; }
.red-box { border: 3px solid #d32f2f; border-radius: 16px; background-color: #ffffff; padding: 25px 25px 15px 25px; margin: 30px 0; }
.red-box h4 { margin: 0 0 8px 0; font-size: 1.3em; color: #d32f2f; font-weight: bold; }
.red-box p { margin: 0 0 20px 25px; font-size: 1.05em; color: #333; line-height: 1.6; }
.bottom-section h3 { font-size: 1.35em; border-left: 6px solid #1a365d; padding-left: 12px; color: #1a365d; margin-bottom: 20px; font-weight: bold; }
.bottom-section ul { padding-left: 30px; margin: 0; }
.bottom-section li { margin-bottom: 15px; font-size: 1.05em; line-height: 1.7; }
@media (max-width: 768px) { .pc-br { display: none; } }
</style>
<div class="poster-wrapper">
<div class="header">
<h2>頭部外傷後の注意</h2>
<img class="logo-img" src="LOGO_IMG_HOLDER" alt="医療機関ロゴ">
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

    final_html = poster_html.replace("LOGO_IMG_HOLDER", logo_src).replace("BG_IMG_HOLDER", bg_src)
    st.markdown(final_html, unsafe_allow_html=True)
