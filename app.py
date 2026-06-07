import streamlit as st
import random
import yt_dlp

# Page setup and baseline aesthetics
st.set_page_config(page_title="Gleearn Kids 🏠", layout="wide")

# --- All Safe Channel Data ---
SAFE_CHANNELS = {
    "msrachel": "https://www.youtube.com/@msrachel",
    "bluesclues": "https://www.youtube.com/@bluesclues",
    "ChuChuTV": "https://www.youtube.com/@ChuChuTV",
    "SuperLittleEinsteins": "https://www.youtube.com/@SuperLittleEinsteins",
    "TreehouseDirect": "https://www.youtube.com/@TreehouseDirect",
    "SuperbookTV": "https://www.youtube.com/@SuperbookTV",
    "CharlieAndLolaOfficial": "https://www.youtube.com/@CharlieAndLolaOfficial",
    "PeppaPigOfficial": "https://www.youtube.com/@PeppaPigOfficial",
    "DoraOfficial": "https://www.youtube.com/@DoraOfficial",
    "CliffordtheBigRedDogClassic": "https://www.youtube.com/@CliffordtheBigRedDogClassic",
    "nickjr": "https://www.youtube.com/@nickjr",
    "ShauntheSheepOfficial": "https://www.youtube.com/@ShauntheSheepOfficial",
    "BenAndHollyOfficial": "https://www.youtube.com/@BenAndHollyOfficial",
    "ShimmerandShine": "https://www.youtube.com/@ShimmerandShine",
    "StrawberryShortcake": "https://www.youtube.com/@StrawberryShortcake",
    "BubbleGuppies": "https://www.youtube.com/@BubbleGuppies",
    "carebears": "https://www.youtube.com/@carebears",
    "thegarfieldshowofficial": "https://www.youtube.com/@thegarfieldshowofficial",
    "pocoyoenglish": "https://www.youtube.com/@pocoyoenglish",
    "pororoenglish": "https://www.youtube.com/@pororoenglish",
    "winxclub": "https://www.youtube.com/@winxclub",
    "monsterhigh": "https://www.youtube.com/@MonsterHigh",
    "barbielifeinthedreamhouse801": "https://www.youtube.com/@barbielifeinthedreamhouse801",
    "ChooChooTrainKidsVideos": "https://www.youtube.com/@ChooChooTrainKidsVideos",
    "McQueenandFriends": "https://www.youtube.com/@McQueenandFriends",
    "Ben10": "https://www.youtube.com/@Ben10",
    "TheOrganicChemistryTutor": "https://www.youtube.com/@TheOrganicChemistryTutor",
    "gimigugustiucu": "https://www.youtube.com/@gimigugustiucu",
    "LeapFrog": "https://www.youtube.com/@LeapFrog",
    "CodeMonkeyStudios": "https://www.youtube.com/@CodeMonkeyStudios",
    "LearningMole": "https://www.youtube.com/@LearningMole",
    "SmileandLearnEnglish": "https://www.youtube.com/@SmileandLearnEnglish",
    "VooksStorybooks": "https://www.youtube.com/@VooksStorybooks",
    "HomeschoolPop": "https://www.youtube.com/@HomeschoolPop",
    "Minecraft": "https://www.youtube.com/@Minecraft",
    "KidsAcademyCom": "https://www.youtube.com/@KidsAcademyCom",
    "TheAnalystYTs": "https://www.youtube.com/@TheAnalystYTs",
    "amazeorg": "https://www.youtube.com/@amazeorg",
    "Blippi": "https://www.youtube.com/@Blippi",
    "BlippiWonders": "https://www.youtube.com/@BlippiWonders",
    "SesameStreet": "https://www.youtube.com/@SesameStreet",
    "Numberblocks": "https://www.youtube.com/@Numberblocks",
    "artforkidshub": "https://www.youtube.com/@artforkidshub",
    "klunatik": "https://www.youtube.com/@klunatik",
    "user-cx1ru4jx3x": "https://www.youtube.com/@user-cx1ru4jx3x",
    "SpongeBobOfficial": "https://www.youtube.com/@SpongeBobOfficial",
    "JackHartmann": "https://www.youtube.com/@JackHartmann",
    "Peekaboo_Kidz": "https://www.youtube.com/@Peekaboo_Kidz",
    "natgeokids": "https://www.youtube.com/@natgeokids",
    "ThePowerpuffGirls": "https://www.youtube.com/@ThePowerpuffGirls",
    "zackdfilms": "https://www.youtube.com/@zackdfilms",
    "NileRed": "https://www.youtube.com/@NileRed",
    "NileBlue": "https://www.youtube.com/@NileBlue",
    "AmoebaSisters": "https://www.youtube.com/@AmoebaSisters",
    "DiggersForKids": "https://www.youtube.com/@DiggersForKids",
    "NoodleAndPals": "https://www.youtube.com/@NoodleAndPals",
    "LearnBright": "https://www.youtube.com/@LearnBright",
    "happytoddlerlearning": "https://www.youtube.com/@happytoddlerlearning",
    "EnglishFairyTales": "https://www.youtube.com/@EnglishFairyTales",
    "FriendshipIsMagicOfficial": "https://www.youtube.com/@FriendshipIsMagicOfficial",
    "GlobalMartialArtsUniversity": "https://www.youtube.com/@GlobalMartialArtsUniversity",
    "maytathebrownbear": "https://www.youtube.com/@maytathebrownbear",
    "teacherlistv": "https://www.youtube.com/@teacherlistv",
    "zeneiasasmr": "https://www.youtube.com/@zeneiasasmr"
}

# Core State Initialization
if "theme" not in st.session_state:
    st.session_state.theme = "Teal (Neutral Mode)"
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "videos" not in st.session_state:
    st.session_state.videos = []
if "math_passed" not in st.session_state:
    st.session_state.math_passed = False
if "math_problem" not in st.session_state:
    st.session_state.math_problem = None
if "active_video" not in st.session_state:
    st.session_state.active_video = None
if "pending_video_id" not in st.session_state:
    st.session_state.pending_video_id = None

# --- Dynamic Color Theme Application Engine ---
THEMES = {
    "Teal (Neutral Mode)": {"bg": "#004d4d", "card": "#008080", "accent": "#00cd9a", "text": "#ffffff"},
    "Green (Glee Mode)": {"bg": "#143d14", "card": "#1e5c1e", "accent": "#81c784", "text": "#ffffff"},
    "Blue (Learn Mode)": {"bg": "#0a2540", "card": "#1034a6", "accent": "#42a5f5", "text": "#ffffff"}
}
current_colors = THEMES[st.session_state.theme]

st.markdown(f"""
    <style>
        .stApp {{ background-color: {current_colors['bg']}; color: {current_colors['text']}; }}
        div[data-testid="stMarkdownContainer"] p {{ color: {current_colors['text']}; }}
        .video-card {{
            background-color: {current_colors['card']};
            border: 2px solid {current_colors['accent']};
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 5px;
        }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def fetch_videos():
    videos = []
    sampled_channels = random.sample(list(SAFE_CHANNELS.items()), min(len(SAFE_CHANNELS), 12))
    
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlistend': 4, 'no_warnings': True, 'ignoreerrors': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for name, url in sampled_channels:
            try:
                info = ydl.extract_info(f"{url}/videos", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry and len(videos) < 24:
                            videos.append({
                                'title': entry.get('title', 'Fun Video'),
                                'id': entry.get('id'),
                                'thumb': f"https://img.youtube.com/vi/{entry.get('id')}/mqdefault.jpg",
                                'channel': entry.get('uploader', 'Gleearn Safe Content')
                            })
            except:
                continue
    random.shuffle(videos)
    return videos

if not st.session_state.videos:
    st.session_state.videos = fetch_videos()

def generate_math_problem():
    op = random.choice(['+', '-', '*'])
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    if op == '+': ans = n1 + n2
    elif op == '-': 
        n1, n2 = max(n1, n2), min(n1, n2)
        ans = n1 - n2
    else: ans = n1 * n2
    return {"question": f"{n1} {op} {n2}", "answer": ans}

# --- CONTROL BAR INTERFACES ---
st.title("Gleearn Kids 🏠")
c_theme, c_nav = st.columns(2)
with c_theme:
    st.session_state.theme = st.selectbox("Choose App Palette Theme:", options=list(THEMES.keys()))
with c_nav:
    view_mode = st.radio("Navigation View Target:", ["Main Stream Feed", "My Favorites Vault"], horizontal=True)

# Filter targets
displayed_videos = st.session_state.videos
if view_mode == "My Favorites Vault":
    displayed_videos = [v for v in st.session_state.videos if v['id'] in st.session_state.favorites]

# --- PARENT MATH GATE DIALOGUE (Renders right at the top so it's impossible to miss) ---
if st.session_state.math_problem:
    st.error("⚠️ **Grown-Up Verification Required**")
    st.markdown(f"### Solve this puzzle to unlock the video slot: **{st.session_state.math_problem['question']} = ?**")
    
    user_ans = st.text_input("Your Answer:", key="math_gate_field")
    if st.button("Submit Answer 🔓"):
        try:
            if int(user_ans) == st.session_state.math_problem['answer']:
                st.session_state.math_passed = True
                st.session_state.math_problem = None
                st.success("Correct! Access approved.")
                st.session_state.active_video = st.session_state.pending_video_id
                st.session_state.pending_video_id = None
                st.rerun()
            else:
                st.sidebar.error("Oops! Not quite right. Ask mom/dad for help! 💡")
                st.error("Oops! Not quite right. Ask mom/dad for help! 💡")
        except ValueError:
            st.error("Please enter a valid whole number.")
    st.markdown("---")

# --- CENTRAL THEATER VIEW ---
if st.session_state.active_video and not st.session_state.math_problem:
    st.subheader("📺 Playing Now:")
    st.video(f"https://www.youtube.com/watch?v={st.session_state.active_video}")
    if st.button("Close Video Player ❌"):
        st.session_state.active_video = None
        st.rerun()

# --- MAIN GRIDS ---
if displayed_videos:
    cols = st.columns(3)
    for idx, vid in enumerate(displayed_videos):
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
                <div class='video-card'>
                    <img src="{vid['thumb']}" style='width:100%; border-radius:6px;'>
                    <h5 style='margin:10px 0; height:40px; overflow:hidden;'>{vid['title']}</h5>
                </div>
            """, unsafe_allow_html=True)
            
            is_twelfth = (idx + 1) % 12 == 0
            b_col1, b_col2, b_col3 = st.columns(3)
            
            with b_col1:
                if is_twelfth and not st.session_state.math_passed:
                    if st.button("🔒 Locked", key=f"btn_{vid['id']}"):
                        st.session_state.math_problem = generate_math_problem()
                        st.session_state.pending_video_id = vid['id']
                        st.rerun()
                else:
                    if st.button("▶️ Play", key=f"btn_{vid['id']}"):
                        st.session_state.active_video = vid['id']
                        st.rerun()
                        
            with b_col2:
                if vid['id'] in st.session_state.favorites:
                    if st.button("❤️ Unfav", key=f"fav_{vid['id']}"):
                        st.session_state.favorites.remove(vid['id'])
                        st.rerun()
                else:
                    if st.button("⭐ Fav", key=f"fav_{vid['id']}"):
                        st.session_state.favorites.append(vid['id'])
                        st.rerun()
                        
            with b_col3:
                st.download_button(
                    label="📥 Save",
                    data=f"Video metadata tag link verification check: {vid['id']}",
                    file_name=f"safe_video_{vid['id']}.txt",
                    mime="text/plain",
                    key=f"dl_{vid['id']}"
                )
