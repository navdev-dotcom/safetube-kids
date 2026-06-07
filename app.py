import streamlit as st
import random
import yt_dlp
import os

# Set up page configurations and baseline aesthetic styles
st.set_page_config(page_title="SafeTube Kids 🏠", layout="wide")

# --- Safe Channel Data ---
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

# Initialize session parameters to track across re-renders
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

# --- Dynamic Color Theme Application Engine ---
THEMES = {
    "Teal (Neutral Mode)": {"bg": "#004d4d", "card": "#008080", "accent": "#00cd9a", "text": "#ffffff"},
    "Green (Glee Mode)": {"bg": "#143d14", "card": "#1e5c1e", "accent": "#81c784", "text": "#ffffff"},
    "Blue (Learn Mode)": {"bg": "#0a2540", "card": "#1034a6", "accent": "#42a5f5", "text": "#ffffff"}
}
current_colors = THEMES[st.session_state.theme]

# Inject matching styles directly into Streamlit components
st.markdown(f"""
    <style>
        .stApp {{ background-color: {current_colors['bg']}; color: {current_colors['text']}; }}
        div[data-testid="stMarkdownContainer"] p {{ color: {current_colors['text']}; }}
        .video-card {{
            background-color: {current_colors['card']};
            border: 2px solid {current_colors['accent']};
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# --- Video Fetch Engine Engine via yt_dlp ---
def fetch_videos(query="", sample_size=6, max_results=24):
    videos = []
    selected_urls = random.sample(list(SAFE_CHANNELS.values()), min(len(SAFE_CHANNELS), sample_size))
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 5,
        'no_warnings': True,
        'ignoreerrors': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for base_url in selected_urls:
            try:
                info = ydl.extract_info(f"{base_url}/videos", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'Video Asset')
                            video_id = entry.get('id')
                            if not query or query.lower() in title.lower():
                                if video_id:
                                    thumb = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                                    videos.append({
                                        'title': title,
                                        'id': video_id,
                                        'thumb': thumb,
                                        'channel': entry.get('uploader', 'Safe Content')
                                    })
            except:
                continue
    random.shuffle(videos)
    return videos[:max_results]

# --- Math Question Generation Logic ---
def generate_math_problem():
    ops = ['+', '-', '*', '/']
    op = random.choice(ops)
    if op == '/':
        num2 = random.randint(1, 5)
        ans = random.randint(1, 6)
        num1 = num2 * ans # Ensures cleanly divisible whole integers
    elif op == '*':
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        ans = num1 * num2
    elif op == '-':
        num1 = random.randint(5, 20)
        num2 = random.randint(1, num1)
        ans = num1 - num2
    else:
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        ans = num1 + num2
    return {"question": f"{num1} {op} {num2}", "answer": ans}

# --- Action Bar UI Layout ---
st.title("SafeTube Kids 🏠")
col_search, col_theme, col_nav = st.columns([3, 2, 2])

with col_theme:
    st.session_state.theme = st.selectbox(
        "Choose App Palette Theme:", 
        options=["Teal (Neutral Mode)", "Green (Glee Mode)", "Blue (Learn Mode)"]
    )

with col_search:
    search_query = st.text_input("Search child-safe content details:", placeholder="Type keywords here...")
    if st.button("🔍 Search Engine Go"):
        st.session_state.videos = fetch_videos(query=search_query)
        st.session_state.math_passed = False # Reset gate flags upon search generation changes

with col_nav:
    view_mode = st.radio("Navigation View Target:", ["Main Stream Feed", "My Favorites Vault"])
    if st.button("🔄 Refresh Data Streams") or not st.session_state.videos:
        st.session_state.videos = fetch_videos()
        st.session_state.math_passed = False

# Filter downstream parameters based on structural selection
displayed_videos = st.session_state.videos
if view_mode == "My Favorites Vault":
    displayed_videos = [v for v in st.session_state.videos if v['id'] in st.session_state.favorites]

# --- Structural Core Video Grid Engine Render ---
if not displayed_videos:
    st.info("No video profiles found under chosen filter conditions.")
else:
    # Iterate dynamically using 3 columns
    cols = st.columns(3)
    for index, vid in enumerate(displayed_videos):
        col_target = cols[index % 3]
        
        with col_target:
            st.markdown(f"""
                <div class='video-card'>
                    <img src="{vid['thumb']}" style='width:100%; border-radius:6px;'>
                    <h4 style='margin: 10px 0 5px 0; height: 45px; overflow: hidden;'>{vid['title']}</h4>
                    <p style='color: {current_colors['accent']}; font-size: 0.85em;'>{vid['channel']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Action controls row
            c1, c2, c3 = st.columns([1, 1, 1])
            
            # ⚠️ Math Gate Evaluation Condition Triggers Every 12th Element (index 11, 23, etc)
            is_twelfth_video = (index + 1) % 12 == 0
            
            with c1:
                if is_twelfth_video and not st.session_state.math_passed:
                    if st.button("🔓 Unlock", key=f"lock_{vid['id']}"):
                        st.session_state.math_problem = generate_math_problem()
                        st.rerun()
                else:
                    if st.button("▶️ Play", key=f"play_{vid['id']}"):
                        st.video(f"https://www.youtube.com/watch?v={vid['id']}")
                        
            with c2:
                if vid['id'] in st.session_state.favorites:
                    if st.button("❤️ Unfav", key=f"fav_{vid['id']}"):
                        st.session_state.favorites.remove(vid['id'])
                        st.rerun()
                else:
                    if st.button("⭐ Fav", key=f"fav_{vid['id']}"):
                        st.session_state.favorites.append(vid['id'])
                        st.rerun()
                        
            with c3:
                # Direct Simulated Web Safe Downloading Proxy Mechanism
                st.download_button(
                    label="📥 Save",
                    data=f"Video ID Meta Reference: {vid['id']}",
                    file_name=f"safetube_{vid['id']}.txt",
                    mime="text/plain",
                    key=f"dl_{vid['id']}"
                )

# --- Math Verification Floating Dialogue Box Panel ---
if st.session_state.math_problem is not None and not st.session_state.math_passed:
    st.markdown("---")
    st.subheader("🧠 Verification Gate Challenge!")
    st.write(f"Solve this math equation to securely parse the target payload content stream: **{st.session_state.math_problem['question']}**")
    
    user_ans = st.number_input("Enter calculation result:", step=1, key="math_gate_input")
    
    if st.button("Verify Answer"):
        if user_ans == st.session_state.math_problem['answer']:
            st.success("Correct! Fetching next index blocks.")
            st.session_state.math_passed = True
            st.session_state.math_problem = None
            st.session_state.videos += fetch_videos(sample_size=4) # Appends additional fresh video feeds
            st.rerun()
        else:
            st.error("Oops! Not quite right. Ask mom/dad for help! 💡")
