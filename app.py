import os
import base64
from html import escape

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sklearn.ensemble import RandomForestClassifier

# =========================================================
# AI SOIL & SEED MATCHMAKER
# FINAL UPDATE - RIGHT PANEL, TITLE, CHART 0-100, FOOTER NAIK
# Fokus: browser zoom 100%, Windows Scale 150%, sidebar lebih turun, card tidak bertumpuk
# =========================================================

st.set_page_config(
    page_title="AI Soil & Seed Matchmaker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# HELPER GAMBAR
# =========================================================
def img_base64(filename: str) -> str:
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def local_img(filename: str, css_class: str = "") -> str:
    data = img_base64(filename)
    if not data:
        return f"<span class='missing-img'>File {escape(filename)} tidak ditemukan</span>"
    ext = filename.split(".")[-1].lower()
    mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
    cls = f"class='{css_class}'" if css_class else ""
    return f"<img {cls} src='data:image/{mime};base64,{data}'/>"


def plant_file(prediksi: str) -> str:
    return {
        "Akasia": "tanaman_akasia.png",
        "Sengon": "tanaman_sengon.png",
        "Kayu Putih": "tanaman_kayu_putih.png",
        "Trembesi": "tanaman_trembesi.png",
    }.get(prediksi, "tanaman_default.png")


# =========================================================
# CSS FINAL - TANPA OVERLAP
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&display=swap');

:root{
    --sidebar-w:304px;
    --green:#54ff9a;
    --green2:#18c85d;
    --line:rgba(87,255,154,.62);
    --panel:rgba(0,47,25,.78);
    --panel2:rgba(0,25,14,.92);
    --text:#f6fff8;
}

*{box-sizing:border-box;}
html, body, [class*="css"]{font-family:'Inter',sans-serif !important;}
html, body{overflow:hidden !important;}

#MainMenu, footer{visibility:hidden !important;height:0 !important;}
header, [data-testid="stHeader"]{display:none !important;height:0 !important;}

[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"],
button[title="Hide sidebar"],
button[title="Show sidebar"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"]{
    display:none !important;
    visibility:hidden !important;
}

.stApp{
    background:
      radial-gradient(circle at 72% 18%, rgba(85,255,155,.10), transparent 23%),
      radial-gradient(circle at 35% 78%, rgba(85,255,155,.08), transparent 30%),
      linear-gradient(90deg, rgba(0,15,8,.98), rgba(0,50,26,.90), rgba(0,15,8,.98)),
      url("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?q=80&w=2013&auto=format&fit=crop");
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}
.stApp:after{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background-image:
      linear-gradient(rgba(255,255,255,.022) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,.022) 1px, transparent 1px);
    background-size:72px 72px;
    opacity:.38;
    z-index:0;
}
[data-testid="stAppViewContainer"], section.main{position:relative;z-index:1;}

.block-container,
[data-testid="stMainBlockContainer"]{
    max-width:100% !important;
    padding:0.58rem 0.62rem 0.18rem 0.62rem !important;
}

/* =========================================================
   SIDEBAR - COMPACT 100% ZOOM
   ========================================================= */
[data-testid="stSidebar"]{
    width:var(--sidebar-w) !important;
    min-width:var(--sidebar-w) !important;
    max-width:var(--sidebar-w) !important;
    background:
      radial-gradient(circle at 70% 0%, rgba(80,255,150,.11), transparent 30%),
      linear-gradient(180deg, rgba(0,38,20,.99), rgba(0,45,24,.98)) !important;
    border-right:1.35px solid var(--line);
    box-shadow:8px 0 26px rgba(0,0,0,.24);
}
[data-testid="stSidebar"] > div:first-child{
    height:100vh !important;
    overflow:hidden !important;
}
[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] .block-container{
    padding:1.18rem 0.78rem 0.36rem 0.78rem !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:0.22rem !important;}

.side-section{
    color:#f6fff8;
    font-size:0.72rem;
    font-weight:900;
    letter-spacing:1.1px;
    line-height:1.05;
    display:flex;
    align-items:center;
    gap:7px;
    margin:0 0 1.06rem 0;
    padding:0 0 0.42rem 0;
    border-bottom:1px solid rgba(122,255,178,.26);
    white-space:nowrap;
}
.side-section.location{margin-top:0.86rem;margin-bottom:0.78rem;}
.side-icon{font-size:0.98rem;filter:drop-shadow(0 0 5px rgba(100,255,170,.38));}
.side-label{
    color:#f9fff9;
    font-size:0.50rem;
    font-weight:900;
    line-height:1.18;
    margin:0.56rem 0 0.28rem 0;
    padding:0;
    white-space:nowrap;
    opacity:.98;
}

/* semua label native disembunyikan karena kita pakai label manual */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
    display:none !important;
    height:0 !important;
    min-height:0 !important;
    margin:0 !important;
    padding:0 !important;
}
[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stTextInput{
    margin:0 !important;
    padding:0 !important;
}
[data-testid="stSidebar"] input{
    background:#111821 !important;
    color:#ffffff !important;
    border:1px solid rgba(99,255,163,.24) !important;
    border-radius:9px !important;
    min-height:24px !important;
    height:24px !important;
    font-size:0.54rem !important;
    font-weight:850 !important;
    padding:0.22rem 0.52rem !important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.04) !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button{
    background:#121922 !important;
    border-color:rgba(99,255,163,.18) !important;
    color:#ffffff !important;
    min-height:24px !important;
    height:24px !important;
    width:24px !important;
    padding:0 !important;
}
.side-meter{
    width:100%;
    height:3px;
    border-radius:999px;
    background:rgba(255,255,255,.18);
    overflow:hidden;
    margin:0.24rem 0 0.70rem 0;
}
.side-meter-fill{
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#ff5b64,#ffbd4f,#47f28b);
}
.side-meter-fill.blue{background:linear-gradient(90deg,#5ec8ff,#44ffaa);}
.side-meter-fill.green{background:linear-gradient(90deg,#4cf58f,#18c85d);}
.side-meter-fill.red{background:linear-gradient(90deg,#ff4e59,#ff9e59);}

.stButton>button{
    width:100%;
    min-height:27px;
    height:27px;
    border-radius:14px;
    border:1px solid rgba(194,255,217,.78) !important;
    background:linear-gradient(135deg,#78ffb2 0%,#18c85d 100%) !important;
    color:#03180c !important;
    font-weight:900 !important;
    font-size:0.40rem !important;
    box-shadow:0 8px 18px rgba(77,255,152,.24), inset 0 1px 0 rgba(255,255,255,.28);
    margin-top:0.52rem;
    white-space:nowrap;
    letter-spacing:-.55px;
    overflow:hidden !important;
    text-overflow:clip !important;
}
.stButton>button:hover{transform:translateY(-1px);filter:brightness(1.04);}

/* =========================================================
   HEADER
   ========================================================= */
.top-header{
    display:grid;
    grid-template-columns:44px 1fr 44px;
    align-items:center;
    gap:10px;
    width:100%;
    margin:0 0 1.02rem 0;
}
.logo-round{
    width:41px;
    height:41px;
    border-radius:50%;
    background:white;
    padding:5px;
    object-fit:contain;
    justify-self:center;
    box-shadow:0 0 0 3px rgba(255,255,255,.14),0 0 18px rgba(77,255,152,.45);
}
.title-card{
    height:42px;
    border:1.35px solid rgba(94,255,158,.66);
    border-radius:15px;
    background:
      linear-gradient(135deg, rgba(255,255,255,.10), rgba(0,47,25,.66)),
      radial-gradient(circle at 90% 30%, rgba(100,255,165,.10), transparent 27%);
    display:flex;
    align-items:center;
    justify-content:center;
    padding:5px 44px;
    box-shadow:0 9px 22px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.12);
    overflow:hidden;
}
.title-card h1.main-title,
.main-title{
    color:#fff !important;
    text-align:center !important;
    font-size:clamp(1.35rem,1.95vw,1.85rem) !important;
    line-height:0.92 !important;
    font-weight:900 !important;
    letter-spacing:0.32px !important;
    margin:0 !important;
    padding:0 !important;
    text-shadow:0 4px 14px rgba(0,0,0,.70) !important;
    white-space:nowrap !important;
}

/* =========================================================
   METRIC CARDS
   ========================================================= */
.metric-grid{
    display:grid;
    grid-template-columns:repeat(5, minmax(0,1fr));
    gap:0.70rem;
    width:100%;
    margin:0 0 1.08rem 0;
}
.param-card{
    height:58px;
    border:1.1px solid rgba(87,255,150,.56);
    border-radius:12px;
    background:
      radial-gradient(circle at 96% 2%, rgba(138,255,184,.13), transparent 31%),
      linear-gradient(145deg, rgba(18,77,43,.74), rgba(0,24,13,.92));
    padding:7px 9px 6px 9px;
    position:relative;
    overflow:hidden;
    box-shadow:0 8px 18px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.08);
}
.param-card:after{
    content:"";
    position:absolute;
    right:-18px;
    top:-34px;
    width:62px;
    height:58px;
    background:rgba(142,255,186,.13);
    border-radius:50%;
}
.param-top{display:flex;align-items:center;gap:6px;color:#fff;font-weight:900;font-size:.57rem;line-height:1;position:relative;z-index:1;white-space:nowrap;}
.param-icon{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,rgba(87,255,143,.28),rgba(4,37,21,.88));border:1px solid rgba(116,255,172,.50);font-size:.76rem;flex:0 0 auto;}
.param-value{color:#fff;font-size:1.18rem;font-weight:900;margin-top:5px;line-height:1;text-shadow:0 4px 12px rgba(0,0,0,.58);position:relative;z-index:1;}
.param-unit{font-size:.54rem;font-weight:900;margin-left:3px;}
.bar{height:3px;border-radius:999px;background:rgba(255,255,255,.22);overflow:hidden;margin-top:6px;position:relative;z-index:1;}
.fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#69ff9f,#15be58);}

/* =========================================================
   PANEL UMUM
   ========================================================= */
div[data-testid="stVerticalBlock"]{gap:0.86rem !important;}
[data-testid="stSidebar"] div[data-testid="stVerticalBlock"]{gap:0.22rem !important;}
div[data-testid="column"]{padding:0 !important;}
.panel{
    border:1.1px solid rgba(90,255,154,.66);
    border-radius:13px;
    background:
      radial-gradient(circle at 92% 90%, rgba(92,255,151,.06), transparent 25%),
      linear-gradient(135deg, rgba(16,77,43,.69), rgba(0,24,13,.90));
    box-shadow:0 10px 22px rgba(0,0,0,.22), inset 0 0 26px rgba(86,255,150,.045);
    padding:8px 9px;
    overflow:hidden;
    margin-bottom:0.88rem;
}
.panel-title{color:#eafff1;font-size:.75rem;font-weight:900;margin:0 0 3px 0;line-height:1.05;text-shadow:0 2px 10px rgba(0,0,0,.35);}
.panel-sub{color:#fff;font-size:.51rem;line-height:1.16;font-weight:700;margin-bottom:6px;}
.info-panel{height:auto;min-height:138px;}
.gis-info-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;}
.info-box{border:1px solid rgba(112,255,170,.38);border-radius:9px;background:rgba(0,39,20,.50);padding:7px 8px;min-height:41px;}
.info-label{color:#8dffb8;font-size:.46rem;font-weight:900;letter-spacing:.55px;}
.info-value{color:#fff;font-size:.55rem;font-weight:900;margin-top:4px;line-height:1.18;}

/* =========================================================
   CHART HTML - FIXED 0–100 SCALE, LABEL SUMBU Y DI LUAR PLOT
   ========================================================= */
.chart-panel{height:194px;}
.chart-box{
    height:146px;
    display:grid;
    grid-template-columns:24px 26px minmax(0,1fr);
    grid-template-rows:105px 31px;
    column-gap:5px;
    row-gap:0;
    margin-top:4px;
    padding:5px 10px 0 0;
    overflow:visible;
}
.chart-y-label{
    grid-column:1;
    grid-row:1;
    writing-mode:vertical-rl;
    transform:rotate(180deg);
    align-self:center;
    justify-self:end;
    color:#f8fff9;
    font-size:.49rem;
    font-weight:900;
    letter-spacing:.15px;
    white-space:nowrap;
}
.chart-ticks{grid-column:2;grid-row:1;position:relative;height:100%;overflow:visible;}
.chart-tick{position:absolute;right:2px;transform:translateY(-50%);color:#f9fff9;font-size:.49rem;font-weight:850;line-height:1;}
.chart-tick.zero{top:auto !important;bottom:-3px;transform:none;}
.chart-plot{
    grid-column:3;
    grid-row:1;
    position:relative;
    height:100%;
    border-left:1px solid rgba(255,255,255,.38);
    border-bottom:1px solid rgba(255,255,255,.38);
    background:
      linear-gradient(to bottom, rgba(255,255,255,.13) 1px, transparent 1px);
    background-size:100% 20%;
    overflow:visible;
}
.chart-bars{
    position:absolute;
    inset:0 10px 0 10px;
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:10px;
    align-items:end;
}
.chart-item{height:100%;display:flex;align-items:end;justify-content:center;position:relative;}
.chart-bar{width:min(34px,74%);min-height:5px;border-radius:3px 3px 0 0;background:linear-gradient(180deg,#73ffad 0%,#16bd58 100%);box-shadow:0 0 15px rgba(76,255,150,.22);position:relative;}
.chart-bar span{position:absolute;left:50%;transform:translateX(-50%);top:-15px;color:#fff;font-size:.54rem;font-weight:900;text-shadow:0 2px 8px #000;}
.chart-labels{grid-column:3;grid-row:2;display:grid;grid-template-columns:repeat(5,1fr);gap:10px;padding:7px 10px 0 10px;}
.chart-labels div{text-align:center;color:#fff;font-size:.48rem;font-weight:900;line-height:1.02;}

/* =========================================================
   SCORE & REKOMENDASI
   ========================================================= */
.score-card{display:grid;grid-template-columns:86px 1fr;gap:12px;align-items:center;height:108px;}
.gauge{--score:0;width:78px;height:78px;border-radius:50%;background:radial-gradient(circle at center,rgba(0,35,18,.98) 0 54%,transparent 55%),conic-gradient(#4df092 calc(var(--score) * 1%),rgba(255,255,255,.16) 0);display:flex;align-items:center;justify-content:center;color:white;font-size:.92rem;font-weight:900;box-shadow:0 0 18px rgba(76,255,150,.18),inset 0 0 0 1px rgba(255,255,255,.12);}
.score-title{color:#fff;font-size:.58rem;font-weight:850;margin-bottom:4px;}
.score-big{color:#66ffa4;font-size:1.18rem;line-height:1;font-weight:900;margin-bottom:5px;}
.score-ok{color:#79ffad;font-size:.56rem;font-weight:850;margin-bottom:6px;}
.score-desc,.not-yet{color:#fff;font-size:.51rem;line-height:1.28;font-weight:700;}
.recom-card{display:grid;grid-template-columns:86px 1fr;gap:12px;align-items:center;height:116px;}
.plant-large{width:74px;height:74px;object-fit:cover;border-radius:50%;background:white;padding:4px;border:3px solid rgba(189,255,211,.94);box-shadow:0 0 0 3px rgba(85,185,255,.45),0 0 14px rgba(87,255,143,.35);justify-self:center;}
.recom-label{color:#dfffe7;font-size:.58rem;font-weight:850;margin-bottom:5px;}
.recom-name{color:#fff;font-size:1.18rem;line-height:1;font-weight:900;margin:0 0 7px 0;text-shadow:0 3px 12px rgba(0,0,0,.45);}
.recom-text{color:#fff;font-size:.51rem;line-height:1.25;font-weight:700;max-width:450px;}

.footer-card{
    width:100%;
    margin:-0.70rem 0 0 0;
    transform:translateY(-8px);
    position:relative;
    z-index:4;
    border:1.0px solid rgba(95,255,158,.48);
    border-radius:12px;
    background:rgba(0,25,14,.74);
    padding:3px 10px;
    text-align:center;
    color:#fff;
    font-size:.54rem;
    font-weight:900;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:7px;
}
.footer-logo{width:16px;height:16px;border-radius:50%;object-fit:contain;background:#fff;padding:2px;}
.missing-img{color:#ffcccc;font-weight:900;font-size:.60rem;}

/* pengaman agar teks label sidebar tidak terpotong */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stElementContainer"]{
    overflow:visible !important;
}
[data-testid="stSidebar"] .stButton{
    margin-top:0.10rem !important;
}

@media (max-height:760px){
    :root{--sidebar-w:296px;}
    .block-container,[data-testid="stMainBlockContainer"]{padding:0.40rem 0.50rem 0.18rem 0.50rem !important;}
    [data-testid="stSidebarUserContent"],[data-testid="stSidebar"] .block-container{padding:1.04rem 0.74rem 0.30rem 0.74rem !important;}
    .side-section{font-size:.62rem;margin-bottom:.98rem;padding-bottom:.34rem;}
    .side-label{font-size:.47rem;margin:.54rem 0 .24rem 0;}
    [data-testid="stSidebar"] input{height:23px !important;min-height:23px !important;font-size:.52rem !important;}
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button{height:23px !important;min-height:23px !important;width:24px !important;}
    .side-meter{height:3px;margin:.18rem 0 .60rem 0;}
    .stButton>button{height:25px;min-height:25px;font-size:.37rem !important;margin-top:.44rem !important;}
    .top-header{grid-template-columns:40px 1fr 40px;gap:9px;margin-bottom:.70rem;}
    .logo-round{width:37px;height:37px;}
    .title-card{height:38px;border-radius:13px;padding:5px 38px;}
    .title-card h1.main-title,.main-title{font-size:clamp(1.22rem,1.75vw,1.62rem) !important;line-height:.90 !important;letter-spacing:.22px !important;}
    .metric-grid{gap:.62rem;margin-bottom:.96rem;}
    .param-card{height:53px;padding:6px 8px 5px 8px;}
    .param-top{font-size:.52rem;}
    .param-icon{width:18px;height:18px;font-size:.68rem;}
    .param-value{font-size:1.05rem;margin-top:4px;}
    .panel{padding:7px 8px;border-radius:12px;margin-bottom:.84rem;}
    .panel-title{font-size:.68rem;}
    .panel-sub{font-size:.47rem;margin-bottom:5px;}
    .info-panel{height:auto;min-height:132px;}
    .info-box{min-height:40px;padding:6px 7px;}
    .chart-panel{height:180px;}
    .chart-box{height:132px;grid-template-rows:96px 30px;grid-template-columns:22px 24px minmax(0,1fr);column-gap:5px;padding-right:8px;}
    .chart-y-label{font-size:.46rem;}
    .chart-tick{font-size:.46rem;}
    .score-card{height:92px;grid-template-columns:74px 1fr;}
    .gauge{width:66px;height:66px;font-size:.78rem;}
    .score-big{font-size:1.05rem;}
    .recom-card{height:100px;grid-template-columns:74px 1fr;}
    .plant-large{width:62px;height:62px;}
    .recom-name{font-size:1.04rem;}
}

@media (max-width:1120px){
    :root{--sidebar-w:270px;}
    .title-card h1.main-title,.main-title{font-size:1.45rem !important;}
    .metric-grid{grid-template-columns:repeat(5,minmax(95px,1fr));}
}

/* =========================================================
   SIDEBAR ALIGNMENT FINAL PATCH
   Fokus: label lebih jelas, input + tombol minus/plus sejajar,
   dan tombol analisis tidak terpotong.
   ========================================================= */
[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] .block-container{
    padding:0.88rem 0.78rem 0.10rem 0.78rem !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{
    gap:0.12rem !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"]{
    margin:0 !important;
    padding:0 !important;
}

.side-section{
    font-size:0.72rem !important;
    line-height:1.05 !important;
    margin:0 0 0.66rem 0 !important;
    padding:0 0 0.34rem 0 !important;
}
.side-section.location{
    margin-top:0.58rem !important;
    margin-bottom:0.48rem !important;
}
.side-icon{
    font-size:1.02rem !important;
}
.side-label{
    display:block !important;
    color:#ffffff !important;
    font-size:0.57rem !important;
    font-weight:900 !important;
    line-height:1.04 !important;
    letter-spacing:0.10px !important;
    margin:0.26rem 0 0.16rem 0.08rem !important;
    padding:0 !important;
    opacity:1 !important;
    text-shadow:0 1px 5px rgba(0,0,0,.90), 0 0 8px rgba(87,255,154,.16) !important;
}

[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stTextInput{
    width:100% !important;
    margin:0 !important;
    padding:0 !important;
}

[data-testid="stSidebar"] .stNumberInput > div,
[data-testid="stSidebar"] .stTextInput > div{
    width:100% !important;
    min-height:28px !important;
    height:28px !important;
    display:flex !important;
    align-items:center !important;
    margin:0 !important;
    padding:0 !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="input"]{
    width:100% !important;
    min-height:28px !important;
    height:28px !important;
    border-radius:10px !important;
    background:#101821 !important;
    border:1px solid rgba(99,255,163,.34) !important;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.05),
        0 0 0 1px rgba(0,0,0,.12) !important;
    overflow:hidden !important;
}

[data-testid="stSidebar"] input{
    min-height:28px !important;
    height:28px !important;
    color:#ffffff !important;
    font-size:0.58rem !important;
    font-weight:900 !important;
    line-height:28px !important;
    padding:0.18rem 0.60rem !important;
    border:none !important;
    box-shadow:none !important;
    background:transparent !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] button{
    min-height:28px !important;
    height:28px !important;
    width:30px !important;
    min-width:30px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    margin:0 !important;
    padding:0 !important;
    border-radius:0 !important;
    background:#111821 !important;
    border-color:rgba(99,255,163,.22) !important;
    color:#ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg{
    width:13px !important;
    height:13px !important;
}

.side-meter{
    height:3px !important;
    margin:0.13rem 0 0.38rem 0 !important;
}

[data-testid="stSidebar"] .stButton{
    margin-top:0.08rem !important;
    padding-top:0 !important;
}
.stButton>button{
    min-height:28px !important;
    height:28px !important;
    font-size:0.58rem !important;
    line-height:1 !important;
    margin-top:0.06rem !important;
    margin-bottom:0 !important;
    letter-spacing:-0.28px !important;
    padding:0 0.55rem !important;
}



/* =========================================================
   SIDEBAR FINAL PATCH V7
   Fokus: label parameter tampil jelas, input nilai dan tombol -/+ sejajar,
   serta pH Tanah memakai rentang 0–7 pada komponen input.
   ========================================================= */
[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] .block-container{
    padding:0.82rem 0.78rem 0.10rem 0.78rem !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{
    gap:0.08rem !important;
}
[data-testid="stSidebar"] [data-testid="stElementContainer"]{
    margin:0 !important;
    padding:0 !important;
}

/* Tampilkan kembali label bawaan Streamlit agar semua parameter jelas */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    align-items:center !important;
    height:12px !important;
    min-height:12px !important;
    max-height:12px !important;
    margin:0 0 0.13rem 0.08rem !important;
    padding:0 !important;
    overflow:visible !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span{
    color:#ffffff !important;
    font-size:0.56rem !important;
    font-weight:900 !important;
    line-height:1 !important;
    letter-spacing:0.05px !important;
    opacity:1 !important;
    text-shadow:0 1px 5px rgba(0,0,0,.95), 0 0 8px rgba(87,255,154,.18) !important;
}

/* Label manual lama disembunyikan karena label native sudah aktif */
.side-label{display:none !important;}

.side-section{
    font-size:0.72rem !important;
    margin:0 0 0.54rem 0 !important;
    padding:0 0 0.32rem 0 !important;
}
.side-section.location{
    margin-top:0.50rem !important;
    margin-bottom:0.42rem !important;
}

[data-testid="stSidebar"] .stNumberInput,
[data-testid="stSidebar"] .stTextInput{
    width:100% !important;
    margin:0 !important;
    padding:0 !important;
}

/* Satu baris kontrol: input nilai + tombol minus + tombol plus */
[data-testid="stSidebar"] [data-testid="stNumberInput"] > div,
[data-testid="stSidebar"] [data-testid="stTextInput"] > div{
    width:100% !important;
    min-height:27px !important;
    height:27px !important;
    display:flex !important;
    align-items:stretch !important;
    margin:0 !important;
    padding:0 !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="input"]{
    min-height:27px !important;
    height:27px !important;
    border-radius:10px !important;
    background:#101821 !important;
    border:1px solid rgba(99,255,163,.38) !important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.06) !important;
    overflow:hidden !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="input"]{
    border-top-right-radius:0 !important;
    border-bottom-right-radius:0 !important;
}
[data-testid="stSidebar"] input{
    min-height:27px !important;
    height:27px !important;
    color:#ffffff !important;
    font-size:0.58rem !important;
    font-weight:900 !important;
    line-height:27px !important;
    padding:0 0.60rem !important;
    border:none !important;
    box-shadow:none !important;
    background:transparent !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button{
    min-height:27px !important;
    height:27px !important;
    width:29px !important;
    min-width:29px !important;
    max-width:29px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    align-self:stretch !important;
    margin:0 !important;
    padding:0 !important;
    border-radius:0 !important;
    background:#111821 !important;
    border:1px solid rgba(99,255,163,.28) !important;
    color:#ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button:last-child{
    border-top-right-radius:10px !important;
    border-bottom-right-radius:10px !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg{
    width:13px !important;
    height:13px !important;
    stroke-width:3 !important;
}

.side-meter{
    height:3px !important;
    margin:0.12rem 0 0.34rem 0 !important;
}

[data-testid="stSidebar"] .stButton{
    margin-top:0.04rem !important;
    padding-top:0 !important;
}
.stButton>button{
    min-height:29px !important;
    height:29px !important;
    font-size:0.58rem !important;
    line-height:1 !important;
    margin-top:0.04rem !important;
    margin-bottom:0 !important;
    letter-spacing:-0.22px !important;
    padding:0 0.55rem !important;
}

@media (max-height:760px){
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebar"] .block-container{
        padding:0.74rem 0.74rem 0.08rem 0.74rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:0.06rem !important;}
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
        height:11px !important;
        min-height:11px !important;
        max-height:11px !important;
        margin:0 0 0.10rem 0.07rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span{
        font-size:0.52rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stNumberInput"] > div,
    [data-testid="stSidebar"] [data-testid="stTextInput"] > div,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="input"],
    [data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button{
        height:25px !important;
        min-height:25px !important;
    }
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button{
        width:28px !important;
        min-width:28px !important;
        max-width:28px !important;
    }
    .side-meter{margin:0.10rem 0 0.26rem 0 !important;}
    .side-section{margin-bottom:0.46rem !important;padding-bottom:0.28rem !important;}
    .side-section.location{margin-top:0.42rem !important;margin-bottom:0.34rem !important;}
    .stButton>button{height:27px !important;min-height:27px !important;font-size:0.55rem !important;}
}


/* =========================================================
   SIDEBAR LABEL POSITION PATCH V10
   Fokus: semua label parameter turun sedikit; khusus pH Tanah
   diberi jarak lebih lega dari judul KONTROL PARAMETER.
   ========================================================= */
.ph-label-spacer{
    height:0.23rem !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
    height:13px !important;
    min-height:13px !important;
    max-height:13px !important;
    margin:0.24rem 0 0.15rem 0.08rem !important;
    padding:0 !important;
    align-items:center !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span{
    font-size:0.56rem !important;
    line-height:1.05 !important;
}

@media (max-height:760px){
    .ph-label-spacer{
        height:0.18rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
        height:12px !important;
        min-height:12px !important;
        max-height:12px !important;
        margin:0.21rem 0 0.12rem 0.07rem !important;
    }
}


/* =========================================================
   SIDEBAR LOWERING PATCH V11
   Fokus: seluruh isi sidebar dan label diturunkan sedikit
   tanpa mengubah alignment input, tombol -/+, dan meter.
   ========================================================= */
[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] .block-container{
    padding-top:1.08rem !important;
}
.side-section{
    margin-bottom:0.68rem !important;
}
.ph-label-spacer{
    height:0.32rem !important;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
    margin:0.32rem 0 0.17rem 0.08rem !important;
}

@media (max-height:760px){
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebar"] .block-container{
        padding-top:0.96rem !important;
    }
    .side-section{
        margin-bottom:0.56rem !important;
    }
    .ph-label-spacer{
        height:0.26rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
        margin:0.27rem 0 0.14rem 0.07rem !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MODEL
# =========================================================
@st.cache_resource
def train_model():
    try:
        file_path = os.path.join(BASE_DIR, "data_tambang.csv")
        df = pd.read_csv(file_path, sep=None, engine="python")
        df.columns = df.columns.str.strip()
        fitur = [
            "pH_Tanah",
            "Porositas_Persen",
            "Kelembapan_Persen",
            "Suhu_Celcius",
            "Logam_Fe_ppm",
        ]
        X = df[fitur]
        y = df["Target_Tanaman"].astype(str).str.strip()
        model = RandomForestClassifier(n_estimators=180, random_state=42)
        model.fit(X, y)
        return model, fitur, None
    except Exception as e:
        return None, [], str(e)


model, daftar_fitur, model_error = train_model()


# =========================================================
# LOGIC
# =========================================================
def status_ph(v):
    if v < 4.5:
        return "Asam", 42, "warn"
    if v <= 6.5:
        return "Baik", 72, ""
    return "Netral", 86, ""


def status_porositas(v):
    if v < 30:
        return "Rendah", 32, "warn"
    if v <= 60:
        return "Sedang", 55, "warn"
    return "Baik", 78, ""


def status_kelembapan(v):
    if v < 35:
        return "Rendah", 36, "warn"
    if v <= 70:
        return "Cukup", 62, "warn"
    return "Tinggi", 82, ""


def status_suhu(v):
    if v < 28:
        return "Sejuk", 45, ""
    if v <= 35:
        return "Stabil", 66, ""
    return "Panas", 82, "warn"


def status_besi(v):
    if v < 100:
        return "Rendah", 38, ""
    if v <= 250:
        return "Sedang", 55, ""
    return "Tinggi", 78, "warn"


def normalize_score(pH, por, hum, temp, fe):
    ph_score = max(0, 100 - abs(pH - 5.5) * 18)
    por_score = max(0, 100 - abs(por - 50) * 1.5)
    hum_score = max(0, 100 - abs(hum - 60) * 1.2)
    temp_score = max(0, 100 - abs(temp - 31) * 4)
    fe_score = max(0, 100 - abs(fe - 150) * 0.18)
    return round((ph_score + por_score + hum_score + temp_score + fe_score) / 5, 1)


def fallback_predict(pH, por, hum, temp, fe):
    if fe > 260 or pH < 4.3:
        return "Kayu Putih"
    if por >= 55 and hum >= 55:
        return "Trembesi"
    if 4.4 <= pH <= 6.4 and 30 <= por <= 62:
        return "Sengon"
    return "Akasia"


def justification(prediksi):
    if prediksi == "Akasia":
        return "Akasia toleran terhadap tanah miskin hara, pH rendah, dan kondisi awal reklamasi."
    if prediksi == "Kayu Putih":
        return "Kayu Putih sesuai untuk lahan dengan tekanan logam Fe dan mendukung revegetasi."
    if prediksi == "Sengon":
        return "Sengon membantu siklus nitrogen dan memperbaiki porositas tanah melalui perakaran."
    if prediksi == "Trembesi":
        return "Trembesi sesuai untuk lahan stabil, penyerapan karbon, dan pembentukan iklim mikro."
    return "Tanaman ini paling sesuai dengan kombinasi parameter lahan yang dimasukkan."


def meter_html(value, max_value, cls="green"):
    width = max(0, min(100, (float(value) / float(max_value)) * 100))
    return f"<div class='side-meter'><div class='side-meter-fill {cls}' style='width:{width:.1f}%;'></div></div>"


def side_label(text):
    # Label manual dinonaktifkan agar tidak bertumpuk dengan label native Streamlit.
    # Label sekarang ditampilkan langsung dari setiap widget agar lebih sejajar dan simetris.
    return None


def param_card(icon, title, value, unit, status, width):
    return (
        f"<div class='param-card'>"
        f"<div class='param-top'><div class='param-icon'>{icon}</div><div>{title}</div></div>"
        f"<div class='param-value'>{value}<span class='param-unit'>{unit}</span></div>"
        f"<div class='bar'><div class='fill' style='width:{width}%;'></div></div>"
        f"</div>"
    )


def info_box(label, value):
    return (
        f"<div class='info-box'>"
        f"<div class='info-label'>{label}</div>"
        f"<div class='info-value'>{value}</div>"
        f"</div>"
    )


def chart_component(pH, por, hum, temp, fe):
    def clamp_0_100(v):
        return max(0, min(100, float(v)))

    # Tinggi batang selalu memakai skala 0–100.
    # Label di atas batang tetap menampilkan nilai asli agar mudah dibaca.
    items = [
        ("pH<br>Tanah", clamp_0_100((pH / 7) * 100), f"{pH:.1f}"),
        ("Porositas", clamp_0_100(por), f"{por:.0f}"),
        ("Kelembapan", clamp_0_100(hum), f"{hum:.0f}"),
        ("Suhu", clamp_0_100((temp / 50) * 100), f"{temp:.1f}"),
        ("Kadar<br>Besi", clamp_0_100((fe / 500) * 100), f"{fe:.0f}"),
    ]
    bars = "".join(
        f"<div class='chart-item'><div class='chart-bar' style='height:{max(6, height):.1f}%;'><span>{label_value}</span></div></div>"
        for _, height, label_value in items
    )
    labels = "".join(f"<div>{name}</div>" for name, _, _ in items)
    ticks = "".join(
        f"<div class='chart-tick' style='top:{100 - val}%;'>{val}</div>"
        for val in [100, 80, 60, 40, 20]
    ) + "<div class='chart-tick zero'>0</div>"
    return (
        f"<div class='chart-box'>"
        f"<div class='chart-y-label'>Intensitas (%)</div>"
        f"<div class='chart-ticks'>{ticks}</div>"
        f"<div class='chart-plot'><div class='chart-bars'>{bars}</div></div>"
        f"<div class='chart-labels'>{labels}</div>"
        f"</div>"
    )


def score_panel(skor, prediksi, justifikasi):
    if prediksi:
        return (
            f"<div class='panel score-card'>"
            f"<div class='gauge' style='--score:{skor};'>{skor:.1f}%</div>"
            f"<div>"
            f"<div class='score-title'>Skor kesesuaian indikatif</div>"
            f"<div class='score-big'>{skor:.1f}%</div>"
            f"<div class='score-ok'>✅ Lahan layak untuk rekomendasi revegetasi.</div>"
            f"<div class='score-desc'>Hasil tanaman dihitung dari kombinasi parameter tanah dan model Random Forest.</div>"
            f"</div></div>"
        )
    return (
        "<div class='panel score-card'>"
        "<div class='gauge' style='--score:0;'>--</div>"
        "<div>"
        "<div class='score-title'>Skor kesesuaian indikatif</div>"
        "<div class='score-big'>--</div>"
        "<div class='not-yet'>Klik tombol <b>ANALISIS KELAYAKAN LAHAN</b> pada sidebar untuk menampilkan skor akhir dan rekomendasi tanaman.</div>"
        "</div></div>"
    )


def recommendation_panel(prediksi, justifikasi):
    if not prediksi:
        return (
            "<div class='panel recom-card'>"
            "<div class='gauge' style='--score:0;'>🌱</div>"
            "<div>"
            "<div class='recom-label'>Tanaman Rekomendasi</div>"
            "<div class='recom-name'>BELUM DIANALISIS</div>"
            "<div class='recom-text'>Rekomendasi tanaman akan muncul setelah tombol analisis dijalankan.</div>"
            "</div></div>"
        )
    return (
        f"<div class='panel recom-card'>"
        f"<div>{local_img(plant_file(prediksi), 'plant-large')}</div>"
        f"<div>"
        f"<div class='recom-label'>Tanaman Rekomendasi</div>"
        f"<div class='recom-name'>{escape(prediksi.upper())}</div>"
        f"<div class='recom-text'>{escape(justifikasi)}</div>"
        f"</div></div>"
    )


def map_component(latitude, longitude, luas_area, map_height=208):
    p1 = [latitude + 0.00220, longitude - 0.00330]
    p2 = [latitude + 0.00335, longitude + 0.00270]
    p3 = [latitude + 0.00055, longitude + 0.00410]
    p4 = [latitude - 0.00355, longitude + 0.00025]
    p5 = [latitude - 0.00055, longitude - 0.00435]
    polygon_js = f"[[{p1[0]}, {p1[1]}], [{p2[0]}, {p2[1]}], [{p3[0]}, {p3[1]}], [{p4[0]}, {p4[1]}], [{p5[0]}, {p5[1]}]]"
    total_height = map_height + 70

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* {{box-sizing:border-box;}}
html, body {{margin:0;padding:0;overflow:hidden;background:transparent;font-family:Inter, Arial, sans-serif;}}
.map-card {{height:{total_height - 2}px;border:1.1px solid rgba(90,255,154,.66);border-radius:13px;background:linear-gradient(135deg, rgba(16,77,43,.69), rgba(0,24,13,.90));box-shadow:0 10px 22px rgba(0,0,0,.22), inset 0 0 26px rgba(86,255,150,.045);padding:8px 9px;overflow:hidden;}}
.map-title {{color:#eafff1;font-size:13px;font-weight:900;line-height:1;margin:0 0 3px 0;text-shadow:0 2px 10px rgba(0,0,0,.35);}}
.map-sub {{color:#fff;font-size:9px;line-height:1.1;font-weight:700;margin:0 0 6px 0;}}
#map {{position:relative;width:100%;height:{map_height}px;border-radius:10px;overflow:hidden;border:1px solid rgba(111,255,171,.42);background:#07170f;}}
.leaflet-control-attribution {{font-size:8px !important;}}
.leaflet-control-zoom a {{width:24px !important;height:24px !important;line-height:24px !important;font-size:16px !important;font-weight:900 !important;}}
.legend {{position:absolute;left:10px;bottom:10px;z-index:999;display:flex;align-items:center;gap:8px;color:white;background:rgba(9,17,28,.82);padding:6px 9px;border-radius:8px;border:1px solid rgba(255,255,255,.32);font-size:11px;font-weight:800;box-shadow:0 8px 22px rgba(0,0,0,.28);}}
.legend-box {{width:22px;height:14px;border:2px solid rgba(255,255,255,.92);background:rgba(31,220,103,.65);}}

/* =========================================================
   STREAMLIT CLOUD INPUT COLOR PATCH V13
   Fokus: field input sidebar tetap gelap di Streamlit Cloud.
   ========================================================= */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="number"]{
    background:#101821 !important;
    background-color:#101821 !important;
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    caret-color:#ffffff !important;
    border:none !important;
    outline:none !important;
    box-shadow:none !important;
}

[data-testid="stSidebar"] div[data-baseweb="input"],
[data-testid="stSidebar"] div[data-baseweb="base-input"],
[data-testid="stSidebar"] div[data-baseweb="input"] > div,
[data-testid="stSidebar"] div[data-baseweb="base-input"] > div{
    background:#101821 !important;
    background-color:#101821 !important;
    color:#ffffff !important;
}

[data-testid="stSidebar"] input::placeholder{
    color:rgba(255,255,255,.72) !important;
    -webkit-text-fill-color:rgba(255,255,255,.72) !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] button{
    background:#111821 !important;
    background-color:#111821 !important;
    color:#ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="base-input"]{
    border-radius:10px !important;
}

[data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stSidebar"] [data-testid="stNumberInput"] div[data-baseweb="base-input"]{
    border-top-left-radius:10px !important;
    border-bottom-left-radius:10px !important;
    border-top-right-radius:0 !important;
    border-bottom-right-radius:0 !important;
}

</style>
</head>
<body>
<div class="map-card">
  <div class="map-title">🗺️ Peta Lokasi GIS</div>
  <div class="map-sub">Peta menunjukkan area lokasi yang akan dianalisis.</div>
  <div id="map">
    <div class="legend"><div class="legend-box"></div><div>Area Analisis ({luas_area:.2f} ha)</div></div>
  </div>
</div>
<script>
var map = L.map('map', {{ zoomControl:true, attributionControl:true }}).setView([{latitude}, {longitude}], 15);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{maxZoom:19, attribution:'Source: Esri World Imagery'}}).addTo(map);
L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{{z}}/{{y}}/{{x}}', {{maxZoom:19, opacity:0.35}}).addTo(map);
var areaCoords = {polygon_js};
var polygon = L.polygon(areaCoords, {{color:'#ffffff', weight:3, opacity:0.95, fillColor:'#23e46f', fillOpacity:0.56}}).addTo(map);
var greenIcon = L.divIcon({{className:'custom-marker', html:'<div style="width:24px;height:24px;border-radius:50%;background:#13bf59;border:4px solid white;box-shadow:0 0 18px rgba(0,0,0,.60);"></div>', iconSize:[24,24], iconAnchor:[12,12]}});
L.marker([{latitude}, {longitude}], {{icon:greenIcon}}).addTo(map);
map.fitBounds(polygon.getBounds(), {{padding:[22,22]}});
setTimeout(function(){{ map.invalidateSize(); }}, 250);
</script>
</body>
</html>
"""
    components.html(html, height=total_height + 4, scrolling=False)


# =========================================================
# SIDEBAR INPUT - LABEL MANUAL AGAR TIDAK SALING TIMPA
# =========================================================
with st.sidebar:
    st.markdown("<div class='side-section'><span class='side-icon'>⚙️</span><span>KONTROL PARAMETER</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='ph-label-spacer'></div>", unsafe_allow_html=True)

    side_label("pH Tanah")
    input_pH = st.number_input("pH Tanah", min_value=0.0, max_value=7.0, value=4.5, step=0.1, format="%.1f", label_visibility="visible")
    st.markdown(meter_html(input_pH, 7, "green"), unsafe_allow_html=True)

    side_label("Porositas (%)")
    input_porositas = st.number_input("Porositas (%)", min_value=0, max_value=100, value=40, step=1, label_visibility="visible")
    st.markdown(meter_html(input_porositas, 100, "red"), unsafe_allow_html=True)

    side_label("Kelembapan (%)")
    input_kelembapan = st.number_input("Kelembapan (%)", min_value=0, max_value=100, value=50, step=1, label_visibility="visible")
    st.markdown(meter_html(input_kelembapan, 100, "blue"), unsafe_allow_html=True)

    side_label("Suhu (°C)")
    input_suhu = st.number_input("Suhu (°C)", min_value=0.0, max_value=50.0, value=32.0, step=0.5, format="%.1f", label_visibility="visible")
    st.markdown(meter_html(input_suhu, 50, "red"), unsafe_allow_html=True)

    side_label("Kadar Besi (ppm)")
    input_besi = st.number_input("Kadar Besi (ppm)", min_value=0, max_value=500, value=150, step=1, label_visibility="visible")
    st.markdown(meter_html(input_besi, 500, "red"), unsafe_allow_html=True)

    st.markdown("<div class='side-section location'><span class='side-icon'>🗺️</span><span>DATA LOKASI GIS</span></div>", unsafe_allow_html=True)

    side_label("Nama Lokasi")
    lokasi = st.text_input("Nama Lokasi", "Hulawa - Pani Gold Mine", label_visibility="visible")

    side_label("Latitude")
    latitude = st.number_input("Latitude", value=0.548539, format="%.6f", step=0.000100, label_visibility="visible")

    side_label("Longitude")
    longitude = st.number_input("Longitude", value=121.975425, format="%.6f", step=0.000100, label_visibility="visible")

    side_label("Luas Area (ha)")
    luas_area = st.number_input("Luas Area (ha)", value=1.00, min_value=0.01, step=0.10, format="%.2f", label_visibility="visible")

    run_analysis = st.button("🌱 ANALISIS KELAYAKAN LAHAN")


# =========================================================
# HEADER
# =========================================================
st.markdown(
    f"""
<div class="top-header">
  {local_img("logo_ung.png", "logo-round")}
  <div class="title-card"><h1 class="main-title">AI SOIL &amp; SEED MATCHMAKER</h1></div>
  {local_img("logo_klhk.png", "logo-round")}
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# PARAMETER CARDS
# =========================================================
ph_status, ph_bar, _ = status_ph(input_pH)
por_status, por_bar, _ = status_porositas(input_porositas)
hum_status, hum_bar, _ = status_kelembapan(input_kelembapan)
temp_status, temp_bar, _ = status_suhu(input_suhu)
fe_status, fe_bar, _ = status_besi(input_besi)

cards_html = (
    param_card("🌱", "pH Tanah", f"{input_pH:.1f}", "", ph_status, ph_bar)
    + param_card("▦", "Porositas", f"{input_porositas}", "%", por_status, por_bar)
    + param_card("💧", "Kelembapan", f"{input_kelembapan}", "%", hum_status, hum_bar)
    + param_card("🌡️", "Suhu", f"{input_suhu:.1f}", "°C", temp_status, temp_bar)
    + param_card("Fe", "Kadar Besi", f"{input_besi}", "ppm", fe_status, fe_bar)
)
st.markdown(f"<div class='metric-grid'>{cards_html}</div>", unsafe_allow_html=True)


# =========================================================
# ANALYSIS
# =========================================================
skor = normalize_score(input_pH, input_porositas, input_kelembapan, input_suhu, input_besi)
prediksi = None
justifikasi = None

if run_analysis:
    if model is not None:
        user_data = pd.DataFrame(
            [[input_pH, input_porositas, input_kelembapan, input_suhu, input_besi]],
            columns=daftar_fitur,
        )
        prediksi = str(model.predict(user_data)[0]).strip()
    else:
        prediksi = fallback_predict(input_pH, input_porositas, input_kelembapan, input_suhu, input_besi)

    st.session_state["hasil_analisis"] = {
        "prediksi": prediksi,
        "justifikasi": justification(prediksi),
    }

if "hasil_analisis" in st.session_state:
    prediksi = st.session_state["hasil_analisis"]["prediksi"]
    justifikasi = st.session_state["hasil_analisis"]["justifikasi"]


# =========================================================
# MAIN CONTENT
# =========================================================
left, right = st.columns([1.06, 1.00], gap="medium")

with left:
    gis_info_html = (
        info_box("LOKASI", escape(lokasi))
        + info_box("LATITUDE", f"{latitude:.6f}")
        + info_box("LONGITUDE", f"{longitude:.6f}")
        + info_box("LUAS AREA", f"{luas_area:.2f} ha")
        + info_box("STATUS", "Area Analisis")
        + info_box("MODE", "GIS Marker")
    )

    st.markdown(
        f"""
<div class="panel info-panel">
  <div class="panel-title">🗺️ Informasi Lokasi GIS</div>
  <div class="panel-sub">Data lokasi sampel lahan yang dianalisis. Koordinat dapat diubah melalui sidebar.</div>
  <div class="gis-info-grid">{gis_info_html}</div>
</div>
""",
        unsafe_allow_html=True,
    )
    map_component(latitude, longitude, luas_area, map_height=208)

with right:
    st.markdown(
        f"""
<div class="panel chart-panel">
  <div class="panel-title">📊 Grafik Analisis Parameter</div>
  <div class="panel-sub">Intensitas setiap parameter dalam skala 0–100.</div>
  {chart_component(input_pH, input_porositas, input_kelembapan, input_suhu, input_besi)}
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(score_panel(skor, prediksi, justifikasi), unsafe_allow_html=True)
    st.markdown(recommendation_panel(prediksi, justifikasi), unsafe_allow_html=True)


# =========================================================
# FOOTER NORMAL - TIDAK MENIMPA PETA
# =========================================================
st.markdown(
    f"""
<div class="footer-card">
  {local_img("logo_fisika.png", "footer-logo")}
  <span>Program Studi Fisika - Universitas Negeri Gorontalo</span>
</div>
""",
    unsafe_allow_html=True,
)
