import streamlit as st
import random
import yt_dlp

# --- Page Configuration ---
st.set_page_config(
    page_title="Gleearn Kids 🏠",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Teal Styling to match original background_color='#008080'
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stApp { background-color: #00808022; }
    h1 { color: #008080; }
    </style>
    """, unsafe_allow_html=True)

# --- Full Safe Channel Data ---
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
    "FilipinoFairyTales": "https://www.youtube.com/@FilipinoFairyTales",
    "GlobalMartialArtsUniversity": "https://www.youtube.com/@GlobalMartialArtsUniversity",
    "maytathebrownbear": "https://www.youtube.com/@maytathebrownbear",
    "teacherlistv": "https://www.youtube.com/@teacherlistv",
    "zeneiasasmr": "https://www.youtube.com/@zeneiasasmr"
}

# --- Caching Logic ---
@st.cache_data(ttl=600)  # Cache for 10 mins to keep it snappy
def fetch_safe_videos(query="", sample_size=12):
    videos = []
    # Sample a smaller subset of channels per load to keep speed high
    selected_channels = random.sample(list(SAFE_CHANNELS.values()), min(len(SAFE_CHANNELS), sample_size))
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 5, # Fetch 5 recent videos per channel
        'no_warnings': True,
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in selected_channels:
            try:
                # Append /videos to ensure we get the latest uploads
                info = ydl.extract_info(f"{channel_url}/videos", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'Safe Video')
                            v_id = entry.get('id')
                            # Filter by search query if it exists
                            if not query or query.lower() in title.lower():
                                videos.append({
                                    'title': title,
                                    'id': v_id,
                                    'channel': entry.get('uploader', 'Safe Creator')
                                })
            except:
                continue
    
    random.shuffle(videos)
    return videos

# --- UI Layout ---
st.title("🏠 SafeTube Kids")
st.write("A safe space for kids to explore educational and fun videos.")

# Sidebar Controls
with st.sidebar:
    st.header("Search & Settings")
    query = st.text_input("What do you want to watch?", placeholder="e.g. Science, Peppa...")
    
    if st.button("🔄 Refresh Feed"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.info(f"Currently monitoring **{len(SAFE_CHANNELS)}** verified safe channels.")

# --- Content Area ---
with st.spinner("🔍 Gathering safe videos..."):
    results = fetch_safe_videos(query=query)

if not results:
    st.error("No videos found! Try a different search word or refresh the feed.")
else:
    # Responsive Grid (3 columns)
    cols = st.columns(3)
    for index, video in enumerate(results):
        col_idx = index % 3
        with cols[col_idx]:
            # YouTube Embed
            st.video(f"https://www.youtube.com/watch?v={video['id']}")
            st.caption(f"**{video['title']}**")
            st.markdown(f"*Source: {video['channel']}*")
            st.write("") # Padding
