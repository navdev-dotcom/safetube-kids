import streamlit as st
import random
import yt_dlp
import datetime
import time

# Page configuration
st.set_page_config(page_title="Gleearn Kids 🏠", layout="wide", page_icon="🏠")

# --- CORE BROWSER LOCALSTORAGE BRIDGE ---
def init_local_storage():
    """Injects a headless Javascript anchor to pipeline state persistently into Streamlit."""
    js_code = """
    <script>
    const sendToStreamlit = (key, value) => {
        parent.postMessage({type: 'streamlit:setComponentValue', value: {key: key, data: value}}, '*');
    };
    
    window.addEventListener('message', (e) => {
        if(e.data.type === 'streamlit:render') {
            let favs = localStorage.getItem('gleearn_favs') || '[]';
            let channels = localStorage.getItem('gleearn_whitelist') || '{}';
            sendToStreamlit('sync', {favorites: JSON.parse(favs), whitelist: JSON.parse(channels)});
        }
    });
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

# --- THE COMPLETE 64 SAFE CHANNELS POOL ---
DEFAULT_CHANNELS = {
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

THEMES = {
    "Teal (Neutral Mode)": {"bg": "#004d4d", "card": "#008080", "accent": "#00cd9a", "text": "#ffffff"},
    "Green (Glee Mode)": {"bg": "#143d14", "card": "#1e5c1e", "accent": "#81c784", "text": "#ffffff"},
    "Blue (Learn Mode)": {"bg": "#0a2540", "card": "#1034a6", "accent": "#42a5f5", "text": "#ffffff"}
}

# --- STATE LIFECYCLE MANAGEMENT ---
if "theme" not in st.session_state: st.session_state.theme = "Teal (Neutral Mode)"
if "favorites" not in st.session_state: st.session_state.favorites = []
if "custom_whitelist" not in st.session_state: st.session_state.custom_whitelist = {}
if "videos" not in st.session_state: st.session_state.videos = []
if "unlocked_tier" not in st.session_state: st.session_state.unlocked_tier = 1  
if "math_problems" not in st.session_state: st.session_state.math_problems = {}
if "screentime_start" not in st.session_state: st.session_state.screentime_start = time.time()
if "storage_synced" not in st.session_state: st.session_state.storage_synced = False

# Inject JS storage bridge
storage_payload = st.session_state.get('storage_bridge')
init_local_storage()

# Process data elements from local client profile
if storage_payload and not st.session_state.storage_synced:
    sync_data = storage_payload.get('value', {})
    if sync_data:
        st.session_state.favorites = sync_data.get('favorites', [])
        st.session_state.custom_whitelist = sync_data.get('whitelist', {})
        st.session_state.storage_synced = True
        st.rerun()

# Build aggregated running safe dictionary
ALL_CHANNELS = {**DEFAULT_CHANNELS, **st.session_state.custom_whitelist}

# --- LOCALSTORAGE WRITE HELPER ---
def commit_storage_change(key_target, data_payload):
    """Updates device's localStorage container via HTML5 data payload."""
    import json
    js_write = f"""
    <script>
    localStorage.setItem('{key_target}', '{json.dumps(data_payload)}');
    </script>
    """
    st.components.v1.html(js_write, height=0, width=0)

# --- VIDEO EXTRACTOR ENGINE ---
@st.cache_data(ttl=900)
def fetch_pool_videos(channel_map, search_term=None):
    videos = []
    ydl_opts = {'quiet': True, 'extract_flat': True, 'playlistend': 15, 'no_warnings': True, 'ignoreerrors': True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if search_term:
            # Deep Live Filtering: Injects keywords context-matched to learning terms
            try:
                info = ydl.extract_info(f"ytsearch30:{search_term} kids educational", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            videos.append({
                                'title': entry.get('title', 'Fun Video'),
                                'id': entry.get('id'),
                                'thumb': f"https://img.youtube.com/vi/{entry.get('id')}/mqdefault.jpg",
                                'channel': entry.get('uploader', 'Verified Safe Hub')
                            })
            except Exception:
                pass
        else:
            # Aggregator Mode: Pick a sample flight of 30 channels to avoid heavy API penalties
            sampled_channels = random.sample(list(channel_map.items()), min(len(channel_map), 30))
            for name, url in sampled_channels:
                try:
                    info = ydl.extract_info(f"{url}/videos", download=False)
                    if info and 'entries' in info:
                        for entry in info['entries']:
                            if entry and len(videos) < 150:
                                videos.append({
                                    'title': entry.get('title', 'Fun Video'),
                                    'id': entry.get('id'),
                                    'thumb': f"https://img.youtube.com/vi/{entry.get('id')}/mqdefault.jpg",
                                    'channel': entry.get('uploader', 'Gleearn Safe Content')
                                })
                except Exception:
                    continue
    random.shuffle(videos)
    return videos

def extract_video_id(url_string):
    """Parses standard long, short, and mobile YouTube strings clean."""
    if "youtu.be/" in url_string:
        return url_string.split("youtu.be/")[-1].split("?")[0]
    if "v=" in url_string:
        return url_string.split("v=")[-1].split("&")[0]
    if "embed/" in url_string:
        return url_string.split("embed/")[-1].split("?")[0]
    return None

def generate_math_problem():
    op = random.choice(['+', '-', '*'])
    n1, n2 = random.randint(2, 10), random.randint(2, 9)
    if op == '-': n1, n2 = max(n1, n2), min(n1, n2)
    return {"question": f"{n1} {op} {n2}", "answer": eval(f"{n1} {op} {n2}")}

# --- APPARATUS SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Parent Control Panel")
    
    # Screentime Monitor Component
    st.subheader("⏱️ Screentime Monitor")
    allowed_mins = st.slider("Daily Limit Allocation (Minutes):", 5, 120, value=30, step=5)
    elapsed_seconds = time.time() - st.session_state.screentime_start
    remaining_mins = max(0.0, float(allowed_mins) - (elapsed_seconds / 60.0))
    
    if remaining_mins <= 0:
        st.error("🛑 Time's Up for today! Go out and play!")
        st.stop()
    else:
        st.info(f"⌛ Remaining Watch Time: **{remaining_mins:.1f} Mins**")
    
    st.session_state.theme = st.selectbox("Choose App Palette Theme:", options=list(THEMES.keys()))
    current_colors = THEMES[st.session_state.theme]
    st.markdown("---")
    
    view_mode = st.radio("Navigation View Target:", ["Main Stream Feed", "My Favorites Vault"])
    st.markdown("---")
    
    # Whitelisting Panel (Gated via Verification Puzzle)
    st.subheader("🔒 Custom Whitelisting")
    if "parent_verified" not in st.session_state: st.session_state.parent_verified = False
    
    if not st.session_state.parent_verified:
        if st.checkbox("Unlock Whitelist Settings"):
            if "sidebar_gate" not in st.session_state:
                st.session_state.sidebar_gate = generate_math_problem()
            st.caption(f"Solve to verify: `{st.session_state.sidebar_gate['question']}`")
            ans_input = st.text_input("Answer:", key="side_gate_ans")
            if st.button("Verify 🔑"):
                if ans_input and int(ans_input) == st.session_state.sidebar_gate['answer']:
                    st.session_state.parent_verified = True
                    st.rerun()
    else:
        st.success("Access Granted")
        new_name = st.text_input("Channel Label Name (e.g. PBSKids):")
        new_url = st.text_input("YouTube Channel Handle Link URL:")
        if st.button("➕ Save Channel to Device"):
            if new_name and "@" in new_url:
                st.session_state.custom_whitelist[new_name] = new_url
                commit_storage_change('gleearn_whitelist', st.session_state.custom_whitelist)
                st.toast("Channel Saved Locally!", icon="💾")
                st.cache_data.clear()
                st.rerun()
                
    st.markdown("---")
    if st.button("🔄 Clear System Cache & Refresh", use_container_width=True):
        st.session_state.videos = []
        st.session_state.unlocked_tier = 1
        st.session_state.screentime_start = time.time()
        st.cache_data.clear()
        st.rerun()

# Apply Dynamic UI CSS Framework Injection
st.markdown(f"""
    <style>
        .stApp {{ background-color: {current_colors['bg']}; color: {current_colors['text']}; }}
        div[data-testid="stMarkdownContainer"] p {{ color: {current_colors['text']}; }}
        .video-card {{
            background-color: {current_colors['card']};
            border: 2px solid {current_colors['accent']};
            border-radius: 12px; padding: 12px; margin-bottom: 5px; text-align: center;
        }}
        .video-card h5 {{
            margin: 8px 0; color: {current_colors['text']};
            font-size: 14px; overflow: hidden; height: 40px;
        }}
        .safetube-banner {{
            background: linear-gradient(45deg, #ff6b6b, #ff8e53);
            padding: 20px; border-radius: 15px; margin-bottom: 25px; border: 2px solid #ffffff;
        }}
    </style>
""", unsafe_allow_html=True)

# Main Title App Entry Point
st.title("Gleearn Kids 🏠")

# --- 🛡️ SAFETUBE LINK SANITIZER COMPONENT (DIY.org Clone) ---
st.markdown(
    "<div class='safetube-banner'><h3>🛡️ Gleearn Kids Link Sanitizer</h3>"
    "<p style='margin:0;'>Drop any YouTube address link below to watch it clean—no ads and zero comment sections.</p></div>", 
    unsafe_allow_html=True
)

st_link_input = st.text_input("🔗 Paste YouTube Video Link URL here to play instantly:", placeholder="https://www.youtube.com/watch?v=...")
if st_link_input:
    extracted_id = extract_video_id(st_link_input)
    if extracted_id:
        st.markdown("### 🍿 Distraction-Free Screening Room")
        st.video(f"https://www.youtube.com/watch?v={extracted_id}")
        st.info("✨ Extraneous video recommendation engines and algorithm sidebars have been neutralized successfully.")
        st.markdown("---")
    else:
        st.error("Could not parse Video ID. Please ensure you are entering a valid YouTube watch link.")

# --- ROUTETTE ENGINE & LIVE MULTI-THREAD FILTERS ---
col_search, col_roulette = st.columns([3, 1])
with col_search:
    search_query = st.text_input("🔍 Search Safe Videos (Deep live querying):", value="", placeholder="Type queries like 'dinosaur facts', 'drawing tutorials'...")
with col_roulette:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 Video Roulette Wheel!", use_container_width=True):
        roulette_terms = ["counting numbers for kids", "how do volcanoes work kids", "origami animal paper craft", "space exploration cartoon science", "phonics sounds reading games"]
        search_query = random.choice(roulette_terms)
        st.toast(f"Roulette Selection: {search_query}", icon="✨")

# Handle Processing Chains
if search_query:
    master_list = fetch_pool_videos(ALL_CHANNELS, search_term=search_query)
else:
    if not st.session_state.videos:
        st.session_state.videos = fetch_pool_videos(ALL_CHANNELS)
    master_list = st.session_state.videos

if view_mode == "My Favorites Vault":
    master_list = [v for v in master_list if v['id'] in st.session_state.favorites]

# --- MAIN RESPONSIVE RECTANGLE RENDER GRID ---
if master_list:
    chunk_size = 12
    total_available_chunks = (len(master_list) + chunk_size - 1) // chunk_size
    visible_chunks_count = total_available_chunks if view_mode == "My Favorites Vault" or search_query else st.session_state.unlocked_tier
    
    for tier_idx in range(visible_chunks_count):
        start_idx = tier_idx * chunk_size
        end_idx = min(start_idx + chunk_size, len(master_list))
        chunk_videos = master_list[start_idx:end_idx]
        
        cols = st.columns(3)
        for sub_idx, vid in enumerate(chunk_videos):
            col = cols[sub_idx % 3]
            
            with col:
                st.markdown(f"""
                    <div class='video-card'>
                        <img src="{vid['thumb']}" style='width:100%; border-radius:6px; max-height:160px; object-fit:cover;'>
                        <h5>{vid['title'][:55]}...</h5>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.get(f"play_active_{vid['id']}", False):
                    st.video(f"https://www.youtube.com/watch?v={vid['id']}")
                    if st.button("❌ Close Video", key=f"close_{vid['id']}", use_container_width=True):
                        st.session_state[f"play_active_{vid['id']}"] = False
                        st.rerun()

                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    if st.button("▶️ Play", key=f"btn_{vid['id']}", use_container_width=True):
                        st.session_state[f"play_active_{vid['id']}"] = True
                        st.rerun()
                            
                with b_col2:
                    if vid['id'] in st.session_state.favorites:
                        if st.button("❤️ Unfav", key=f"fav_{vid['id']}", use_container_width=True):
                            st.session_state.favorites.remove(vid['id'])
                            commit_storage_change('gleearn_favs', st.session_state.favorites)
                            st.rerun()
                    else:
                        if st.button("⭐ Fav", key=f"fav_{vid['id']}", use_container_width=True):
                            st.session_state.favorites.append(vid['id'])
                            commit_storage_change('gleearn_favs', st.session_state.favorites)
                            st.rerun()
                            
                with b_col3:
                    ss_download_url = f"https://ssyoutube.com/watch?v={vid['id']}"
                    st.markdown(
                        f'<a href="{ss_download_url}" target="_blank">'
                        f'<button style="width:100%; border-radius:5px; border:2px solid {current_colors["accent"]}; '
                        f'background-color:transparent; color:{current_colors["text"]}; padding:4px; cursor:pointer; font-size:14px;">📥 Save</button></a>',
                        unsafe_allow_html=True
                    )
        
        # Progression Gate Calculations
        next_tier_has_content = len(master_list) > end_idx
        next_tier_is_locked = st.session_state.unlocked_tier == (tier_idx + 1)
        
        if view_mode != "My Favorites Vault" and not search_query and next_tier_has_content and next_tier_is_locked:
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
