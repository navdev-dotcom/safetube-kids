import streamlit as st
import random
import yt_dlp
import io
import urllib.request

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
if "unlocked_tier" not in st.session_state:
    st.session_state.unlocked_tier = 1  
if "math_problems" not in st.session_state:
    st.session_state.math_problems = {}

# --- Dynamic Color Theme Application Engine ---
THEMES = {
    "Teal (Neutral Mode)": {"bg": "#004d4d", "card": "#008080", "accent": "#00cd9a", "text": "#ffffff"},
    "Green (Glee Mode)": {"bg": "#143d14", "card": "#1e5c1e", "accent": "#81c784", "text": "#ffffff"},
    "Blue (Learn Mode)": {"bg": "#0a2540", "card": "#1034a6", "accent": "#42a5f5", "text": "#ffffff"}
}

# --- SIDEBAR INTERFACE COMPONENT PACKING ---
with st.sidebar:
    st.header("⚙️ App Controls")
    st.session_state.theme = st.selectbox("Choose App Palette Theme:", options=list(THEMES.keys()))
    current_colors = THEMES[st.session_state.theme]
    st.markdown("---")
    view_mode = st.radio("Navigation View Target:", ["Main Stream Feed", "My Favorites Vault"])
    st.markdown("---")
    search_query = st.text_input("🔍 Search Videos:", value="", placeholder="Type video keywords here...")
    st.markdown("---")
    if st.button("🔄 Refresh Feed & Clear Cache", use_container_width=True):
        st.session_state.videos = []
        st.session_state.unlocked_tier = 1
        st.session_state.math_problems = {}
        st.cache_data.clear()
        st.rerun()

# Apply the custom styles based on selection
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
        .video-card h5 {{
            margin: 10px 0;
            color: {current_colors['text']};
            word-wrap: break-word;
            white-space: normal;
        }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def fetch_all_pool_videos():
    videos = []
    sampled_channels = random.sample(list(SAFE_CHANNELS.items()), min(len(SAFE_CHANNELS), 25))
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlistend': 5, 'no_warnings': True, 'ignoreerrors': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for name, url in sampled_channels:
            try:
                info = ydl.extract_info(f"{url}/videos", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry and len(videos) < 60:
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
    st.session_state.videos = fetch_all_pool_videos()

# --- SAFE DOWNLOAD CHECKER ENGINE ---
def download_video_bytes(video_id):
    """Fetches video data or handles rate limits safely."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 4  
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info.get('url')
            if stream_url:
                with urllib.request.urlopen(stream_url, timeout=4) as response:
                    return response.read()
    except:
        return None
    return None

def generate_math_problem():
    op = random.choice(['+', '-', '*'])
    n1, n2 = random.randint(1, 10), random.randint(1, 10)
    if op == '+': ans = n1 + n2
    elif op == '-': 
        n1, n2 = max(n1, n2), min(n1, n2)
        ans = n1 - n2
    else: ans = n1 * n2
    return {"question": f"{n1} {op} {n2}", "answer": ans}

st.title("Gleearn Kids 🏠")

master_list = st.session_state.videos
if view_mode == "My Favorites Vault":
    master_list = [v for v in st.session_state.videos if v['id'] in st.session_state.favorites]

if search_query:
    master_list = [v for v in master_list if search_query.lower() in v['title'].lower()]

if master_list:
    chunk_size = 12
    total_available_chunks = (len(master_list) + chunk_size - 1) // chunk_size
    visible_chunks_count = total_available_chunks if view_mode == "My Favorites Vault" else st.session_state.unlocked_tier
    
    for tier_idx in range(visible_chunks_count):
        start_idx = tier_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(master_list))
        chunk_videos = master_list[start_idx:end_idx]
        
        cols = st.columns(3)
        for sub_idx, vid in enumerate(chunk_videos):
            global_idx = start_idx + sub_idx
            col = cols[sub_idx % 3]
            
            with col:
                st.markdown(f"""
                    <div class='video-card'>
                        <img src="{vid['thumb']}" style='width:100%; border-radius:6px;'>
                        <h5>{vid['title']}</h5>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.get(f"play_active_{vid['id']}", False):
                    st.video(f"https://www.youtube.com/watch?v={vid['id']}")
                    if st.button("❌ Close Video", key=f"close_{vid['id']}"):
                        st.session_state[f"play_active_{vid['id']}"] = False
                        st.rerun()

                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    if st.button("▶️ Play", key=f"btn_{vid['id']}"):
                        st.session_state[f"play_active_{vid['id']}"] = True
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
                    video_bytes = None
                    try:
                        video_bytes = download_video_bytes(vid['id'])
                    except:
                        pass
                    
                    if video_bytes is None:
                        st.markdown(
                            f'<a href="https://ssyoutube.com/en141/youtube-video-downloader?q=https://www.youtube.com/watch?v={vid["id"]}" '
                            f'target="_blank"><button style="width:100%; border-radius:5px; border:2px solid {current_colors["accent"]}; '
                            f'background-color:transparent; color:{current_colors["text"]}; padding:4px; cursor:pointer;">📥 Save</button></a>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.download_button(
                            label="📥 Save",
                            data=video_bytes,
                            file_name=f"{vid['id']}.mp4",
                            mime="video/mp4",
                            key=f"dl_{vid['id']}"
                        )
        
        next_tier_has_content = len(master_list) > end_idx
        next_tier_is_locked = st.session_state.unlocked_tier == (tier_idx + 1)
        
        if view_mode != "My Favorites Vault" and next_tier_has_content and next_tier_is_locked:
            st.markdown("---")
            st.markdown(f"<center><h3>🛑 Checkpoint reached after {end_idx} videos! Solve to unlock next row</h3></center>", unsafe_allow_html=True)
            
            if tier_idx not in st.session_state.math_problems:
                st.session_state.math_problems[tier_idx] = generate_math_problem()
                
            problem = st.session_state.math_problems[tier_idx]
            st.info(f"**Grown-Up Verification Puzzle:** Calculate:  ` {problem['question']} = ? `")
            
            col_ans, col_sub = st.columns([3, 1])
            with col_ans:
                user_input = st.text_input("Type answer here:", key=f"gate_input_{tier_idx}", label_visibility="collapsed")
            with col_sub:
                if st.button("Unlock Next Feed 🔓", key=f"gate_btn_{tier_idx}", use_container_width=True):
                    try:
                        if int(user_input) == problem['answer']:
                            st.session_state.unlocked_tier += 1  
                            st.toast("Success! Next row loaded down below...", icon="🎉")
                            st.rerun()
                        else:
                            st.error("Oops! Not quite right. Ask mom/dad for help! 💡")
                    except ValueError:
                        st.error("Please provide a valid whole number value.")
            st.markdown("---")
else:
    st.info("No child-safe video content entries match your active filter paths.")
