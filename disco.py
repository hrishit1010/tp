import streamlit as st
import re
from datetime import datetime
from deep_translator import GoogleTranslator

# ─────────────────────────────────────────────
# Language Config
# ─────────────────────────────────────────────
LANGUAGES = {
    "🇬🇧 English":    "en",
    "🇮🇳 Hindi":      "hi",
    "🇫🇷 French":     "fr",
    "🇩🇪 German":     "de",
    "🇪🇸 Spanish":    "es",
    "🇵🇹 Portuguese": "pt",
    "🇮🇹 Italian":    "it",
    "🇳🇱 Dutch":      "nl",
    "🇵🇱 Polish":     "pl",
    "🇷🇺 Russian":    "ru",
    "🇸🇪 Swedish":    "sv",
    "🇳🇴 Norwegian":  "no",
    "🇩🇰 Danish":     "da",
    "🇫🇮 Finnish":    "fi",
    "🇬🇷 Greek":      "el",
    "🇨🇿 Czech":      "cs",
    "🇷🇴 Romanian":   "ro",
    "🇭🇺 Hungarian":  "hu",
}

# ─────────────────────────────────────────────
# deep-translator helpers  (no API key needed)
# ─────────────────────────────────────────────
def translate_text(text: str, target_lang: str) -> str:
    """Translate English answer to the chosen language."""
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception as e:
        st.warning(f"⚠️ Translation unavailable: {e}")
        return text

def translate_to_english(text: str) -> str:
    """Auto-detect language of user input and translate it to English."""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text

# ─────────────────────────────────────────────
# eSIM Knowledge Base  (keyword → answer map)
# ─────────────────────────────────────────────
ESIM_KB = [
    {
        "keywords": ["what is esim", "what's esim", "define esim", "explain esim", "esim mean"],
        "answer": (
            "📱 **What is an eSIM?**\n\n"
            "An eSIM (Embedded SIM) is a digital SIM card built directly into your device. "
            "Unlike a physical SIM card, you don't need to insert or swap any card — "
            "you simply scan a QR code or enter an activation code provided by your carrier "
            "to activate a mobile plan. eSIMs support multiple profiles, so you can have "
            "more than one number on the same device."
        ),
    },
    {
        "keywords": ["how does esim work", "how esim works", "esim working", "esim technology"],
        "answer": (
            "⚙️ **How does an eSIM work?**\n\n"
            "1. Your device has a small chip soldered onto the motherboard.\n"
            "2. You choose a carrier plan and receive a QR code or activation code.\n"
            "3. Scan the QR code in your phone's settings — the carrier profile is downloaded wirelessly.\n"
            "4. The eSIM stores multiple carrier profiles, and you can switch between them anytime.\n"
            "5. No physical card needed — everything is done over the air (OTA)."
        ),
    },
    {
        "keywords": ["esim vs sim", "difference between esim", "physical sim vs esim", "esim better than sim"],
        "answer": (
            "🆚 **eSIM vs Physical SIM**\n\n"
            "| Feature | eSIM | Physical SIM |\n"
            "|---|---|---|\n"
            "| Form factor | Built-in chip | Removable card |\n"
            "| Activation | QR code / OTA | Insert card |\n"
            "| Multiple profiles | ✅ Yes | ❌ No |\n"
            "| Switch carriers | Instant, no hardware | Swap card |\n"
            "| Water resistance | Better (no slot) | Slot needed |\n"
            "| Travel use | Excellent | Need local SIM card |"
        ),
    },
    {
        "keywords": ["which phone", "what device", "compatible device", "support esim", "esim phone", "esim iphone", "esim samsung", "esim pixel"],
        "answer": (
            "📱 **Devices that support eSIM:**\n\n"
            "**Apple:** iPhone XS and later (iPhone 14 US models are eSIM-only)\n"
            "**Samsung:** Galaxy S20 and later, Z Fold/Flip series\n"
            "**Google Pixel:** Pixel 3 and later\n"
            "**Other:** Many Motorola, Huawei, and Oppo models also support eSIM\n\n"
            "Check your device settings under **Settings → Mobile Data / Cellular → Add eSIM** "
            "to confirm support."
        ),
    },
    {
        "keywords": ["activate esim", "how to activate", "setup esim", "install esim", "add esim", "esim qr"],
        "answer": (
            "✅ **How to activate an eSIM:**\n\n"
            "**On iPhone:**\n"
            "1. Go to Settings → Cellular → Add Cellular Plan\n"
            "2. Scan the QR code from your carrier\n"
            "3. Follow on-screen instructions\n\n"
            "**On Android (Samsung/Pixel):**\n"
            "1. Go to Settings → Connections → SIM Card Manager\n"
            "2. Tap 'Add Mobile Plan' or 'Add eSIM'\n"
            "3. Scan QR code or enter activation code\n\n"
            "📌 You'll need a Wi-Fi connection for the initial download."
        ),
    },
    {
        "keywords": ["benefit", "advantage", "why use esim", "esim good", "pros of esim"],
        "answer": (
            "🌟 **Benefits of eSIM:**\n\n"
            "✔️ **No physical SIM** — nothing to lose or damage\n"
            "✔️ **Instant activation** — no waiting for a card to arrive\n"
            "✔️ **Multiple plans** — personal + work numbers on one device\n"
            "✔️ **Travel-friendly** — add a local plan abroad without swapping SIMs\n"
            "✔️ **Eco-friendly** — no plastic cards or packaging\n"
            "✔️ **Better device design** — no SIM tray means slimmer, more water-resistant phones"
        ),
    },
    {
        "keywords": ["travel", "international", "roaming", "abroad", "foreign country", "global esim"],
        "answer": (
            "✈️ **Using eSIM for Travel:**\n\n"
            "eSIM is perfect for international travel! Here's how:\n\n"
            "1. Before your trip, purchase an international eSIM plan from providers like "
            "Airalo, Holafly, or your home carrier.\n"
            "2. Add the eSIM profile to your device.\n"
            "3. When you land, switch to the travel eSIM — no need to find a local SIM shop!\n\n"
            "💡 **Tip:** Keep your home eSIM active for calls/SMS and use the travel eSIM for data."
        ),
    },
    {
        "keywords": ["cost", "price", "how much", "expensive", "cheap", "free esim", "esim plan"],
        "answer": (
            "💰 **eSIM Cost:**\n\n"
            "eSIM plan pricing varies by carrier and region:\n"
            "- **Local plans:** Same cost as regular SIM plans (₹0–₹999/month in India)\n"
            "- **International travel eSIMs:** Typically $5–$50 for 7–30 days depending on data\n"
            "- **Activation fee:** Usually free; some carriers charge ₹10–₹25\n\n"
            "Popular eSIM providers: **Airtel, Jio, Vi** (India), **Airalo, Holafly** (global)"
        ),
    },
    {
        "keywords": ["secure", "security", "safe", "hack", "privacy", "esim hacked"],
        "answer": (
            "🔒 **Is eSIM secure?**\n\n"
            "Yes — eSIMs are **more secure** than physical SIMs:\n\n"
            "✅ Cannot be physically stolen or cloned as easily\n"
            "✅ Remote lock/wipe possible if device is lost\n"
            "✅ GSMA-standardized encryption for profile downloads\n"
            "✅ Protected by device PIN/biometrics\n\n"
            "⚠️ However, SIM-swapping fraud (social engineering your carrier) is still a risk — "
            "always use strong account passwords with your carrier."
        ),
    },
    {
        "keywords": ["transfer esim", "move esim", "switch phone", "new phone esim", "change device"],
        "answer": (
            "🔄 **Transferring eSIM to a new phone:**\n\n"
            "You **cannot** directly copy an eSIM — it's locked to one device for security.\n\n"
            "**Steps to transfer:**\n"
            "1. Contact your carrier and request an eSIM transfer\n"
            "2. They will issue a new QR code for your new device\n"
            "3. Scan the QR on your new phone — the old profile will be deactivated\n\n"
            "📌 Some carriers allow self-service transfer via their app or website."
        ),
    },
    {
        "keywords": ["delete esim", "remove esim", "cancel esim", "deactivate esim"],
        "answer": (
            "🗑️ **How to delete/remove an eSIM:**\n\n"
            "**iPhone:** Settings → Cellular → [Plan name] → Remove Cellular Plan\n"
            "**Android:** Settings → SIM Card Manager → [Plan name] → Delete\n\n"
            "⚠️ Once deleted, you'll need your carrier to issue a new QR code to re-add it."
        ),
    },
    {
        "keywords": ["india", "jio", "airtel", "vi", "vodafone", "bsnl", "indian carrier"],
        "answer": (
            "🇮🇳 **eSIM in India:**\n\n"
            "eSIM is available from major Indian carriers:\n\n"
            "| Carrier | eSIM Support | How to Activate |\n"
            "|---|---|---|\n"
            "| **Airtel** | ✅ Yes | My Airtel app or visit store |\n"
            "| **Jio** | ✅ Yes | MyJio app or Jio store |\n"
            "| **Vi (Vodafone Idea)** | ✅ Yes | Vi app or store |\n"
            "| **BSNL** | ❌ Limited | Not widely available |\n\n"
            "You'll need to visit a store or complete KYC digitally to get your eSIM QR code."
        ),
    },
    {
        "keywords": ["dual sim", "two number", "two sim", "esim and physical sim"],
        "answer": (
            "📲 **Dual SIM with eSIM:**\n\n"
            "Many modern phones support **Dual SIM Dual Standby (DSDS)** with:\n"
            "- 1 physical nano-SIM + 1 eSIM, **or**\n"
            "- 2 eSIMs (on newer iPhone/Pixel models)\n\n"
            "This lets you have **two active numbers** simultaneously — great for separating "
            "personal and work lines, or using a local data SIM while keeping your home number active."
        ),
    },
    {
        "keywords": ["not working", "problem", "issue", "error", "can't activate", "failed", "troubleshoot"],
        "answer": (
            "🛠️ **eSIM Troubleshooting:**\n\n"
            "**Common issues & fixes:**\n\n"
            "❌ *QR code not scanning* → Ensure good lighting, or manually enter the activation code\n"
            "❌ *Activation failed* → Check Wi-Fi connection; restart device and retry\n"
            "❌ *No signal after activation* → Toggle airplane mode or restart device\n"
            "❌ *Plan not showing* → Wait 15–30 min; contact carrier if it persists\n"
            "❌ *Device not compatible* → Verify your device supports eSIM in its settings\n\n"
            "💬 If issues persist, contact your carrier's support team with your IMEI number."
        ),
    },
]

FALLBACK = (
    "🤔 I'm not sure about that specific question. Here are topics I can help with:\n\n"
    "- What is eSIM / How it works\n"
    "- eSIM vs Physical SIM\n"
    "- Compatible devices (iPhone, Samsung, Pixel)\n"
    "- How to activate an eSIM\n"
    "- eSIM for travel & international use\n"
    "- eSIM in India (Airtel, Jio, Vi)\n"
    "- eSIM security & privacy\n"
    "- Dual SIM with eSIM\n"
    "- Troubleshooting eSIM issues\n\n"
    "Try asking something like: *'How do I activate an eSIM?'* or *'Is eSIM available on Jio?'*"
)

GREETINGS = ["hi", "hello", "hey", "good morning", "good evening", "howdy", "hii", "helo"]
THANKS    = ["thank", "thanks", "thankyou", "thank you", "great", "awesome", "helpful", "perfect"]


def get_esim_response(user_input: str) -> str:
    """Translate input → EN, match KB, return English answer."""
    # Translate non-English input to English first
    english_input = translate_to_english(user_input)

    text = english_input.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)

    if any(g in text.split() for g in GREETINGS) and len(text.split()) <= 4:
        return "👋 Hi there! I'm your eSIM Assistant. Ask me anything about eSIM — activation, compatibility, plans, travel, and more!"

    if any(t in text for t in THANKS):
        return "😊 You're welcome! Feel free to ask if you have more questions about eSIM."

    best_score  = 0
    best_answer = None
    for entry in ESIM_KB:
        score = sum(1 for kw in entry["keywords"] if kw in text)
        if score > best_score:
            best_score  = score
            best_answer = entry["answer"]

    if best_answer and best_score > 0:
        return best_answer

    for entry in ESIM_KB:
        for kw in entry["keywords"]:
            words = kw.split()
            if any(w in text for w in words if len(w) > 4):
                return entry["answer"]

    return FALLBACK


def get_response_in_language(user_input: str, target_lang: str) -> str:
    """Get KB answer then translate it to the chosen language."""
    answer = get_esim_response(user_input)
    return translate_text(answer, target_lang)


# ─────────────────────────────────────────────
# Streamlit Page Config & CSS
# ─────────────────────────────────────────────
st.set_page_config(page_title="eSIM Assistant", page_icon="📱", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.chat-header {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px;
    padding: 20px 28px;
    margin-bottom: 20px;
    color: white;
}

.lang-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin-top: 6px;
}

.msg-user {
    background: #0077ff;
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    font-size: 0.92rem;
}

.msg-bot {
    background: #f0f4f8;
    color: #1a1a2e;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    max-width: 85%;
    font-size: 0.92rem;
    border-left: 3px solid #0077ff;
}

.timestamp { font-size: 0.7rem; opacity: 0.5; margin-top: 4px; }

.stTextInput > div > div > input {
    border-radius: 30px !important;
    border: 2px solid #0077ff !important;
    padding: 10px 20px !important;
}

.stButton > button {
    border-radius: 30px !important;
    background: #0077ff !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
}

/* Language selector pill styling */
div[data-testid="stSelectbox"] > div {
    border-radius: 30px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session state defaults
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "text": "👋 Hello! I'm your eSIM Assistant. I can answer questions about eSIM activation, compatibility, plans, travel, and more. What would you like to know?",
            "time": datetime.now().strftime("%H:%M"),
        }
    ]
if "selected_lang_label" not in st.session_state:
    st.session_state.selected_lang_label = "🇬🇧 English"

# ─────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────
col1, col2 = st.columns([1, 2])

# ── Sidebar panel ──────────────────────────────
with col1:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0f2027,#2c5364);border-radius:16px;padding:24px;color:white;">
        <h2 style="margin-top:0">📱 eSIM Guide</h2>
        <p style="opacity:0.75;font-size:0.85rem;">Your multilingual eSIM assistant!</p>
        <hr style="border-color:rgba(255,255,255,0.2)">
        <h4>💬 Try asking:</h4>
        <ul style="font-size:0.85rem;opacity:0.85;line-height:2">
            <li>What is eSIM?</li>
            <li>How do I activate an eSIM?</li>
            <li>Is eSIM available on Jio?</li>
            <li>eSIM vs physical SIM</li>
            <li>Which phones support eSIM?</li>
            <li>Can I use eSIM abroad?</li>
            <li>Is eSIM secure?</li>
            <li>How to transfer eSIM?</li>
        </ul>
        <hr style="border-color:rgba(255,255,255,0.2)">
        <p style="font-size:0.75rem;opacity:0.6">🌐 Powered by deep-translator · Hindi + 16 European languages</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Language Selector ──
    st.markdown("### 🌐 Response Language")
    selected_label = st.selectbox(
        "Choose language",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(st.session_state.selected_lang_label),
        label_visibility="collapsed",
    )
    st.session_state.selected_lang_label = selected_label
    selected_lang_code = LANGUAGES[selected_label]

    st.info(
        f"Responses will be translated to **{selected_label}**.\n\n"
        "You can type your question in **any language** — it will be auto-detected and understood.",
        icon="🌍",
    )

# ── Chat panel ─────────────────────────────────
with col2:
    current_lang_name = st.session_state.selected_lang_label
    st.markdown(f"""
    <div class="chat-header">
        <span style="font-size:2rem">🤖</span>
        <h2 style="margin:0">eSIM Assistant</h2>
        <p style="margin:4px 0 0;opacity:0.75;font-size:0.85rem">● Online — Ask me anything about eSIM</p>
        <span class="lang-badge">🌐 {current_lang_name}</span>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="msg-user">{msg["text"]}<div class="timestamp">{msg["time"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="msg-bot">{msg["text"]}<div class="timestamp">{msg["time"]}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick suggestion buttons
    st.markdown("**Quick Questions:**")
    quick_questions = [
        "What is eSIM?",
        "How to activate eSIM?",
        "eSIM on Jio/Airtel?",
        "eSIM for travel?",
        "eSIM vs SIM?",
    ]
    cols = st.columns(len(quick_questions))
    for i, q in enumerate(quick_questions):
        with cols[i]:
            if st.button(q, key=f"quick_{i}"):
                now = datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "text": q, "time": now})
                reply = get_response_in_language(q, selected_lang_code)
                st.session_state.messages.append({"role": "bot", "text": reply, "time": now})
                st.rerun()

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "Type your question…",
                placeholder="e.g. How do I activate eSIM on iPhone?  |  eSIM कैसे activate करें?",
                label_visibility="collapsed",
            )
        with btn_col:
            submitted = st.form_submit_button("Send 🚀")

    if submitted and user_input.strip():
        now = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "text": user_input.strip(), "time": now})
        with st.spinner("Translating…"):
            reply = get_response_in_language(user_input.strip(), selected_lang_code)
        st.session_state.messages.append({"role": "bot", "text": reply, "time": now})
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "bot",
                "text": "👋 Chat cleared! Ask me anything about eSIM.",
                "time": datetime.now().strftime("%H:%M"),
            }
        ]
        st.rerun()
