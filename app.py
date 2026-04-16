import os
import sqlite3
import base64
import re
import streamlit as st
from groq import Groq

# ── ASHLEY & TEAM ELITE PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(page_title="Seed2Harvest | Buzuzi & Co.", page_icon="🌾", layout="wide",
                   initial_sidebar_state="expanded")

# ── 1. ASSET ENGINE ───────────────────────────────────────────────────────────
def get_hero_b64_buz():
    paths_mvelo = ["modern_hero.png", "images/modern_hero.png", "images/maxresdefault.jpg"]
    for p_tino in paths_mvelo:
        if os.path.exists(p_tino):
            with open(p_tino, "rb") as f_buz:
                return f"data:image/png;base64,{base64.b64encode(f_buz.read()).decode()}"
    return ""

hero_b64_tino = get_hero_b64_buz()

# ── 2. ADAPTIVE AESTHETIC & BASKET STYLING ──────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600&family=Space+Mono&display=swap');
    :root {{ --gold: #D4A853; }}
    .stApp {{ font-family: 'Source Sans 3', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: -1px; color: var(--gold) !important; }}

    .hero-section {{
        position: relative; height: 400px; width: 100%;
        background-image: url('{hero_b64_tino}');
        background-size: cover; background-position: center;
        display: flex; align-items: center; border-bottom: 2px solid var(--gold);
    }}
    .hero-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(24, 17, 12, 0.6); z-index: 1; }}
    .hero-content {{ position: relative; z-index: 2; padding-left: 60px; border-left: 10px solid var(--gold); margin-left: 40px; }}
    .hero-title {{ font-size: 5rem; line-height: 0.85; letter-spacing: -4px; margin: 0; color: white !important; }}
    
    input[type="text"], textarea {{ background-color: rgba(212, 168, 83, 0.1) !important; border: 1px solid var(--gold) !important; color: inherit !important; }}
    
    .chat-bubble {{ background: rgba(212, 168, 83, 0.05); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 3px solid var(--gold); }}
    
    .receipt-box {{
        background: #fdfdfd; color: #111; padding: 30px; border: 1px solid #ddd;
        font-family: 'Space Mono', monospace; text-transform: uppercase;
        box-shadow: 10px 10px 0px var(--gold); margin: 20px 0;
    }}

    .buhle-quote {{ font-style: italic; color: var(--gold); font-size: 0.8rem; margin-top: 5px; }}
</style>
""", unsafe_allow_html=True)

# ── 3. DATA ENGINE ─────────────────────────────────────────────────────────────
DB_PATH_buz = "the_farm_agent.db"

def get_db_buz():
    conn = sqlite3.connect(DB_PATH_buz)
    conn.row_factory = sqlite3.Row
    return conn

GROQ_API_KEY_tino = st.secrets.get("GROQ_API_KEY", "")
client_buz = Groq(api_key=GROQ_API_KEY_tino)

def ask_groq_buz(user_input, farmer_name, company, chat_history, basket):
    try:
        with get_db_buz() as db:
            prods = db.execute("SELECT p_name, category, price FROM Products").fetchall()
        cat_text = "\n".join([f"- {p['p_name']} (R {p['price']:.2f})" for p in prods])
    except: cat_text = "Catalog error."

    basket_context = "User currently has nothing in basket."
    if basket:
        basket_context = "User's current basket contains: " + ", ".join([f"{v}x {k}" for k, v in basket.items()])

    sys_p = f"""You are the Seed2Harvest assistant for {farmer_name} at {company}.
    BASKET STATE: {basket_context}
    CATALOGUE: {cat_text}
    INSTRUCTION: If the user asks to 'checkout' or 'finalize basket', output [CHECKOUT] at the end. 
    Be helpful and professional."""

    messages = [{"role": "system", "content": sys_p}] + chat_history + [{"role": "user", "content": user_input}]
    try:
        res = client_buz.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.3)
        return res.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

# ── 4. STATE MANAGEMENT ───────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.update({"logged_in": False, "user": None, "messages": [], "basket": {}, "chat_input_box": ""})

# ── 5. AUTH & COMPLIANCE ──────────────────────────────────────────────────────
st.markdown('<div class="hero-section"><div class="hero-overlay"></div><div class="hero-content"><h1 class="hero-title">SEED 2<br>HARVEST</h1><p style="color:var(--gold); letter-spacing:5px;">ELEVATE YOUR EVERYDAY</p></div></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown('<div style="padding: 60px;"><h3>CLIENT ONBOARDING</h3>', unsafe_allow_html=True)
    f_n = st.text_input("NAME")
    f_c = st.text_input("FARM / COMPANY")
    f_l = st.text_input("LOCATION")
    
    st.markdown("---")
    st.warning("Hello fellow farmer. For the agent to work effectively we need permission to work with your data. Click yes to continue or leave.")
    st.markdown(f'<p class="buhle-quote">"ubumfihlo ngundoqo" — Buhle</p>', unsafe_allow_html=True)
    consent = st.checkbox("I GRANT PERMISSION")

    if st.button("AUTHORIZE ENTRY"):
        if f_n and f_c and f_l and consent:
            with get_db_buz() as db:
                c = db.execute("INSERT INTO Farmers (name, location) VALUES (?, ?)", (f"{f_n} ({f_c})", f_l))
                db.commit()
                st.session_state.user = {"farmer_id": c.lastrowid, "username": f_n, "company": f_c, "location": f_l}
                st.session_state.logged_in = True
                st.rerun()
        elif not consent:
            st.error("Access Denied: Compliance consent required.")
    st.stop()

# ── 6. MAIN INTERFACE ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h3>{st.session_state.user['company'].upper()}</h3>", unsafe_allow_html=True)
    page = st.radio("OPERATIONS", ["💬 CHAT", "🛒 CATALOGUE", "📦 GLOBAL FEED"])
    
    st.markdown("---")
    st.markdown("### 🧺 YOUR BASKET")
    if not st.session_state.basket: st.write("Empty")
    for item, qty in st.session_state.basket.items():
        st.write(f"{qty}x {item}")
    if st.button("CLEAR BASKET"): st.session_state.basket = {}; st.rerun()
    
    st.markdown("---")
    if st.button("TERMINATE"): st.session_state.logged_in = False; st.rerun()

# ── PAGE: CHAT ──
if page == "💬 CHAT":
    st.markdown("<h3>CONSULTING AGENT</h3>", unsafe_allow_html=True)
    for m in st.session_state.messages:
        role = "CLIENT" if m["role"] == "user" else "AGENT"
        st.markdown(f'<div class="chat-bubble"><b>{role}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    def handle_chat():
        q = st.session_state.chat_input_box
        if q:
            u = st.session_state.user
            ans = ask_groq_buz(q, u['username'], u['company'], st.session_state.messages, st.session_state.basket)
            
            if "[CHECKOUT]" in ans:
                st.session_state.checkout_triggered = True
                ans = ans.replace("[CHECKOUT]", "").strip()
            
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.session_state.chat_input_box = ""

    st.text_input("MESSAGE", key="chat_input_box", on_change=handle_chat)

    if st.session_state.get("checkout_triggered"):
        st.markdown('<div class="receipt-box">', unsafe_allow_html=True)
        st.markdown(f"**SEED 2 HARVEST**<br>*ELEVATE YOUR EVERYDAY*<br>COMPANY: {st.session_state.user['company']}<br>---", unsafe_allow_html=True)
        total = 0
        with get_db_buz() as db:
            for item, qty in st.session_state.basket.items():
                p = db.execute("SELECT price FROM Products WHERE p_name = ?", (item,)).fetchone()
                sub = p['price'] * qty
                total += sub
                st.markdown(f"{item} x{qty} ... R{sub:.2f}", unsafe_allow_html=True)
        st.markdown(f"---<br>**TOTAL AMOUNT: R{total:.2f}**<br>THANK YOU, FELLOW FARMER.", unsafe_allow_html=True)
        if st.button("CONFIRM & LOG ORDER"):
            # Logic to save to DB (Orders table) goes here
            st.session_state.basket = {}
            st.session_state.checkout_triggered = False
            st.success("ORDER ARCHIVED")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE: CATALOGUE ──
elif page == "🛒 CATALOGUE":
    st.markdown("<h3>PRODUCT SELECTION</h3>", unsafe_allow_html=True)
    with get_db_buz() as db:
        prods = db.execute("SELECT p_name, category, price FROM Products").fetchall()
        for p in prods:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f'<div class="card"><b>{p["p_name"]}</b><br>{p["category"]} - R{p["price"]:.2f}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("ADD", key=p["p_name"]):
                    st.session_state.basket[p["p_name"]] = st.session_state.basket.get(p["p_name"], 0) + 1
                    st.toast(f"{p['p_name']} added to basket")

# ── PAGE: GLOBAL FEED ──
elif page == "📦 GLOBAL FEED":
    st.markdown("<h3>PREVIOUS ORDERS (COMMUNITY)</h3>", unsafe_allow_html=True)
    with get_db_buz() as db:
        feed = db.execute("""
            SELECT F.name, P.p_name, OI.quantity 
            FROM Order_Items OI 
            JOIN Orders O ON OI.order_id = O.order_id 
            JOIN Farmers F ON O.farmer_id = F.farmer_id 
            JOIN Products P ON OI.product_id = P.product_id 
            ORDER BY O.order_id DESC LIMIT 10
        """).fetchall()
        for f in feed:
            st.markdown(f'<div class="chat-bubble">🚜 <b>{f["name"]}</b> acquired {f["quantity"]}x {f["p_name"]}</div>', unsafe_allow_html=True)

# ── 7. FOOTER & SOCIALS ───────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top: 100px; padding: 60px; border-top: 1px solid rgba(212, 168, 83, 0.2); text-align: center;">
    <div style="font-family:'Oswald'; font-size:1.8rem; color:#D4A853;">BUZUZI INCORPORATED</div>
    <p style="color:#888;">FOLLOW ON SOCIALS: @SEED2HARVEST_GLOBAL</p>
    <div style="font-family:'Space Mono'; font-size:0.75rem; color:#666; letter-spacing:3px; margin-top:10px;">
        ASHLEY . BUHLE . GOMOLEMO . UTHA . MVELO
    </div>
</div>
""", unsafe_allow_html=True)
