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

# ── 2. MVELO'S SIGNATURE ADAPTIVE AESTHETIC ──────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600&family=Space+Mono&display=swap');

    :root {{
        --gold: #D4A853;
    }}

    .stApp {{ font-family: 'Source Sans 3', sans-serif; }}
    
    h1, h2, h3 {{ font-family: 'Oswald', sans-serif !important; text-transform: uppercase; letter-spacing: -1px; color: var(--gold) !important; }}

    .hero-section {{
        position: relative; height: 500px; width: 100%;
        background-image: url('{hero_b64_tino}');
        background-size: cover; background-position: center;
        display: flex; align-items: center; border-bottom: 2px solid var(--gold);
    }}
    .hero-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(24, 17, 12, 0.6); z-index: 1; }}
    .hero-content {{ position: relative; z-index: 2; padding-left: 60px; border-left: 10px solid var(--gold); margin-left: 40px; }}
    .hero-title {{ font-size: 6rem; line-height: 0.85; letter-spacing: -4px; margin: 0; color: white !important; }}
    .hero-subtitle {{ font-family: 'Space Mono'; font-size: 0.9rem; letter-spacing: 5px; text-transform: uppercase; margin-top: 15px; color: var(--gold) !important; }}

    input[type="text"], input[type="password"], textarea {{
        background-color: rgba(212, 168, 83, 0.1) !important;
        border: 1px solid var(--gold) !important;
        border-radius: 4px !important;
    }}

    .stButton > button {{
        background-color: transparent !important; color: var(--gold) !important;
        border: 2px solid var(--gold) !important; border-radius: 4px !important;
        font-family: 'Oswald', sans-serif !important; text-transform: uppercase !important;
        letter-spacing: 2px !important; padding: 10px 40px !important; font-weight: 600 !important;
    }}
    .stButton > button:hover {{ background-color: var(--gold) !important; color: white !important; }}

    .chat-bubble {{ 
        background: rgba(212, 168, 83, 0.05); 
        padding: 20px; border-radius: 8px; margin: 10px 40px; 
        border-left: 3px solid var(--gold); 
    }}
    
    .card {{ 
        background: rgba(212, 168, 83, 0.05); 
        border: 1px solid rgba(212, 168, 83, 0.2); 
        padding: 20px; border-radius: 6px; margin: 10px 40px; 
        display: flex; justify-content: space-between; 
    }}

    .brief-box {{
        margin: 10px 40px 30px 40px;
        padding: 20px;
        border: 1px dashed var(--gold);
        font-family: 'Space Mono';
        font-size: 0.85rem;
        opacity: 0.8;
    }}
</style>
""", unsafe_allow_html=True)

# ── 3. DATA & INTELLIGENCE ENGINE ─────────────────────────────────────────────
DB_PATH_buz = "the_farm_agent.db"

def get_db_buz():
    conn = sqlite3.connect(DB_PATH_buz)
    conn.row_factory = sqlite3.Row
    return conn

GROQ_API_KEY_tino = st.secrets.get("GROQ_API_KEY", "")
client_buz = Groq(api_key=GROQ_API_KEY_tino)

def ask_groq_buz(user_input, farmer_name, company, location, chat_history):
    try:
        with get_db_buz() as db:
            prods = db.execute("SELECT p_name, category, price FROM Products").fetchall()
        cat_text = "\n".join([f"- {p['p_name']} ({p['category']}): R {p['price']:.2f}" for p in prods])
    except:
        cat_text = "Catalog synchronization error."

    sys_p = f"""You are the Seed2Harvest assistant for {farmer_name} at {company}.
    COMPREHENSION: Understand all slang, but respond in Professional English.
    STRICT ORDER PROTOCOL: 
    1. Discuss pricing and availability freely.
    2. Do NOT confirm or log an order based on interest alone.
    3. You MUST ask: "Would you like me to officially log this order for you?"
    4. ONLY if the user explicitly says "Yes", "Confirm", "Proceed", or "Log it", then you output: [LOG_ORDER: Product Name, Quantity] at the end of your message.
    CATALOGUE: {cat_text}"""

    messages = [{"role": "system", "content": sys_p}]
    for m in chat_history: messages.append(m)
    messages.append({"role": "user", "content": user_input})

    try:
        res = client_buz.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.3)
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ── 4. UI LOGIC ───────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.messages, st.session_state.chat_input_box = False, None, [], ""

st.markdown(f"""
<div class="hero-section">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <h1 class="hero-title">SEED 2<br>HARVEST</h1>
        <p class="hero-subtitle">ELEVATE YOUR EVERYDAY</p>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown('<div style="padding: 60px;"><h3>CLIENT ONBOARDING</h3>', unsafe_allow_html=True)
    f_n = st.text_input("NAME")
    f_c = st.text_input("FARM / COMPANY")
    f_l = st.text_input("LOCATION")
    if st.button("AUTHORIZE ENTRY"):
        if f_n and f_c and f_l:
            with get_db_buz() as db:
                c = db.execute("INSERT INTO Farmers (name, location) VALUES (?, ?)", (f"{f_n} ({f_c})", f_l))
                db.commit()
                st.session_state.user = {"farmer_id": c.lastrowid, "username": f_n, "company": f_c, "location": f_l}
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

with st.sidebar:
    st.markdown(f"<h3>{st.session_state.user['company'].upper()}</h3><p>{st.session_state.user['username'].upper()}</p>", unsafe_allow_html=True)
    page = st.radio("OPERATIONS", ["💬 CHAT", "🛒 CATALOGUE", "📦 ORDERS"])
    if st.button("TERMINATE"): st.session_state.logged_in = False; st.rerun()

if page == "💬 CHAT":
    st.markdown("<h3 style='margin-left:40px;'>CONSULTING AGENT</h3>", unsafe_allow_html=True)
    
    # ── THE CHAT EXPLANATION (STRATEGIC BRIEF) ──
    st.markdown("""
    <div class="brief-box">
        <b>MISSION:</b> Optimize farm operations through real-time intelligence.<br>
        <b>CAPABILITIES:</b> Instant pricing inquiries, inventory consultation, and automated procurement.<br>
        <b>PROTOCOL:</b> Discuss your needs with the agent. When you are ready to purchase, 
        confirm the request to log an official order directly into the legacy system.
    </div>
    """, unsafe_allow_html=True)

    for m in st.session_state.messages:
        role_label = "CLIENT" if m["role"] == "user" else "AGENT"
        st.markdown(f'<div class="chat-bubble"><b>{role_label}:</b><br>{m["content"]}</div>', unsafe_allow_html=True)

    def process_mvelo():
        q = st.session_state.chat_input_box
        if q:
            u = st.session_state.user
            ans = ask_groq_buz(q, u['username'], u['company'], u['location'], st.session_state.messages)

            match = re.search(r'\[LOG_ORDER:\s*(.*?),\s*(\d+)\]', ans)
            if match:
                with get_db_buz() as db:
                    p = db.execute("SELECT product_id FROM Products WHERE p_name LIKE ?", (f"%{match.group(1).strip()}%",)).fetchone()
                    if p:
                        o = db.execute("INSERT INTO Orders (farmer_id) VALUES (?)", (u['farmer_id'],))
                        db.execute("INSERT INTO Order_Items (order_id, product_id, quantity) VALUES (?, ?, ?)", (o.lastrowid, p['product_id'], int(match.group(2))))
                        db.commit()
                        st.success(f"ORDER FOR {match.group(1).upper()} LOGGED.")
                ans = re.sub(r'\[LOG_ORDER:.*?\]', '', ans).strip()

            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.session_state.chat_input_box = ""

    st.text_input("MESSAGE", key="chat_input_box", on_change=process_mvelo)
    st.button("EXECUTE", on_click=process_mvelo)

elif page == "🛒 CATALOGUE":
    st.markdown("<h3 style='margin-left:40px;'>CATALOGUE</h3>", unsafe_allow_html=True)
    with get_db_buz() as db:
        for p in db.execute("SELECT p_name, category, price FROM Products").fetchall():
            st.markdown(f'<div class="card"><div><b>{p["p_name"]}</b><br>{p["category"]}</div><div style="color:#D4A853;">R{p["price"]:.2f}</div></div>', unsafe_allow_html=True)

elif page == "📦 ORDERS":
    st.markdown("<h3 style='margin-left:40px;'>YOUR ORDER HISTORY</h3>", unsafe_allow_html=True)
    with get_db_buz() as db:
        query = """
            SELECT O.order_id, P.p_name, OI.quantity, P.price, (OI.quantity * P.price) as total
            FROM Orders O
            JOIN Order_Items OI ON O.order_id = OI.order_id
            JOIN Products P ON OI.product_id = P.product_id
            WHERE O.farmer_id = ?
        """
        user_orders = db.execute(query, (st.session_state.user['farmer_id'],)).fetchall()
        
        if not user_orders:
            st.markdown("<p style='margin-left:40px;'>No orders found for this session.</p>", unsafe_allow_html=True)
        for ord in user_orders:
            st.markdown(f"""
            <div class="card">
                <div><b>ID: #{ord['order_id']} | {ord['p_name']}</b><br>Qty: {ord['quantity']}</div>
                <div style="color:#D4A853;">TOTAL: R{ord['total']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ── 5. TEAM LEGACY FOOTER ─────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top: 100px; padding: 60px; border-top: 1px solid rgba(212, 168, 83, 0.2);">
    <div style="font-family:'Oswald'; font-size:1.8rem; color:#D4A853;">BUZUZI INCORPORATED</div>
    <div style="font-family:'Space Mono'; font-size:0.75rem; color:#888; letter-spacing:3px; margin-top:10px;">
        ASHLEY . BUHLE . GOMOLEMO . UTHA . MVELO
    </div>
</div>
""", unsafe_allow_html=True)
