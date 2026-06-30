import streamlit as st

# ページの設定（スマホでも見やすいように設定）
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

    # 文字サイズ拡大と背景画像・ロゴ画像の読み込みを追加（空行なし）
    poster_html = """<style>
.poster-wrapper { background-color: #f4f4f4; padding: 20px; font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif; color: #222; line-height: 1.6; font-size: 18px; }
.header { border-bottom: 2px dotted #999; padding-bottom: 10px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: flex-end; }
.header h2 { margin: 0; font-size: 28px; color: #000; }
.logo-img { height: 45px; object-fit: contain; }
.bg-section { background-image: url('https://raw.githubusercontent.com/r-suga-dot/head-injury-noticeNMS/main/bg.jpg'); background-size: cover; background-position: center; padding: 25px 15px; border-radius: 8px; margin-bottom: 20px; }
.highlight { background-color: rgba(255, 255, 255, 0.9); padding: 4px 8px; display: inline; font-size: 1.05em; box-decoration-break: clone; -webkit-box-decoration-break: clone; line-height: 1.8; }
.red-box { border: 3px solid #d32f2f; border-radius: 15px; background-color: #fff9e6; padding: 20px 20px 10px 20px; margin: 20px 0; }
.red-box h4 { margin: 0 0 8px 0; font-size: 1.25em; color: #000; font-weight: bold; }
.red-box p { margin: 0 0 18px 20px; font-size: 1em; color: #333; }
.bottom-section h3 { font-size: 1.3em; border-bottom: 1px solid #ccc; padding-bottom: 5px; font-weight: bold; }
.bottom-section ul { padding-left: 25px; }
.bottom-section li { margin-bottom: 12px; font-size: 1em; }
</style>
<div class="poster-wrapper">
<div class="header">
<h2>頭部外傷後の注意</h2>
<img class="logo-img" src="https://raw.githubusercontent.com/r-suga-dot/head-injury-noticeNMS/main/logo.png" alt="日本医科大学付属病院">
</div>
<div class="bg-section">
<p><span class="highlight">頭を打った時には、脳にいろいろな変化が起ります。</span><br><span class="highlight">数は少ないのですが、<strong>頭蓋骨（あたまの骨）の内側に出血が<br>起ると生命に危険</strong>をおよぼすことがありますので注意が必要です。</span></p>
<p><span class="highlight">このような頭蓋内出血（頭の中の出血）の症状は、<br>頭を打った後すぐ起る、ときには数日、数ヶ月も経ってから<br>起ることもあります。ですから<strong>現在何も症状がなくても十分<br>注意しなければなりません。</strong></span></p>
<p><span class="highlight">頭を打ったのち、元気だった人が急に死亡したりすることが<br>あるのは、このような頭蓋内出血のためです。頭の骨に異常がない<br>からといって安心はできません。</span></p>
<p><span class="highlight">そこで次に書いた注意をよく読んで、手おくれにならぬ内に、<br>患者さんを病院につれてくることが非常に重要です。</span></p>
</div>
<div class="red-box">
<h4>１．頭痛がだんだん強くなる時</h4>
<h4>２．吐き気や嘔吐が起る時</h4>
<p>（食べたものを吐いたり、何も食べないのに物を吐く）<br>（小児の場合は嘔吐をすぐしますが、それが数回にもおよぶ時）</p>
<h4>３．手足が動きにくくなったり、しびれたり、<br>  手に持ったものを取り落すことが多くなったりした時</h4>
<h4>４．ぼんやりしてくる時、あるいはほっておくと<br>  すぐ眠ってしまい起してもなかなか起きない時</h4>
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
    
    st.markdown(poster_html, unsafe_allow_html=True)
