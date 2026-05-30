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

# --- Theme Configuration (Green, Blue, Teal) ---
# Initialize theme settings in session state if not present
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "Neutral Mode (Teal)"

# Theme color configurations
THEME_STYLES = {
    "Calm Mode (Green)": {"bg": "#e8f5e9", "primary": "#2e7d32", "accent": "#a5d6a744"},
    "Learning Mode (Blue)": {"bg": "#e3f2fd", "primary": "#1565c0", "accent": "#90caf944"},
    "Neutral Mode (Teal)": {"bg": "#e0f2f1", "primary": "#008080", "accent": "#00808022"}
}

selected_theme = st.session_state.app_theme
theme_colors = THEME_STYLES[selected_theme]

# Inject Dynamic Styles
st.markdown(f"""
    <style>
    .stApp {{ background-color: {theme_colors['accent']}; }}
    h1, h2, h3 {{ color: {theme_colors['primary']} !important; }}
    .stButton>button {{
        background-color: {theme_colors['primary']};
        color: white;
        border-radius: 8px;
    }}
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
    "EnglishFairyTales": "https://www.youtube.com/@EnglishFairyTales",
    "FriendshipIsMagicOfficial": "https://www.youtube.com/@FriendshipIsMagicOfficial",
    "GlobalMartialArtsUniversity": "https://www.youtube.com/@GlobalMartialArtsUniversity",
    "maytathebrownbear": "https://www.youtube.com/@maytathebrownbear",
    "teacherlistv": "https://www.youtube.com/@teacherlistv",
    "zeneiasasmr": "https://www.youtube.com/@zeneiasasmr"
}

# --- Caching Logic ---
@st.cache_data(ttl=600)
def fetch_safe_videos(query="", sample_size=15): # Expanded sample size to showcase scrolling past 10
    videos = []
    selected_channels = random.sample(list(SAFE_CHANNELS.values()), min(len(SAFE_CHANNELS), sample_size))
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlistend': 5, 
        'no_warnings': True,
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for channel_url in selected_channels:
            try:
                info = ydl.extract_info(f"{channel_url}/videos", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'Safe Video')
                            v_id = entry.get('id')
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

# --- Math Question Generator Helper ---
def generate_math_question():
    operation = random.choice(["+", "-", "*", "/"])
    if operation == "+":
        num1, num2 = random.randint(5, 20), random.randint(5, 20)
        ans = num1 + num2
    elif operation == "-":
        num1 = random.randint(10, 30)
        num2 = random.randint(1, num1)
        ans = num1 - num2
    elif operation == "*":
        num1, num2 = random.randint(2, 9), random.randint(2, 9)
        ans = num1 * num2
    else:  # Division
        num2 = random.randint(2, 8)
        ans = random.randint(2, 10)
        num1 = num2 * ans
    return f"{num1} {operation} {num2}", ans

# Initialize Session States for Parental Controls
if "math_question" not in st.session_state:
    q_str, q_ans = generate_math_question()
    st.session_state.math_question = q_str
    st.session_state.math_answer = q_ans
    st.session_state.gate_passed = False

# --- UI Layout ---
st.title("🏠 Gleearn Kids")
st.write("A safe space for kids to explore educational and fun videos.")

# Sidebar Controls
with st.sidebar:
    st.header("Search & Settings")
    query = st.text_input("What do you want to watch?", placeholder="e.g. Science, Peppa...")
    
    # Theme Selection UI
    theme_choice = st.selectbox(
        "Choose Screen Mode:", 
        options=["Calm Mode (Green)", "Learning Mode (Blue)", "Neutral Mode (Teal)"],
        index=list(THEME_STYLES.keys()).index(st.session_state.app_theme)
    )
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
        
    if st.button("🔄 Refresh Feed"):
        # Reset math gate on manual clear
        q_str, q_ans = generate_math_question()
        st.session_state.math_question = q_str
        st.session_state.math_answer = q_ans
        st.session_state.gate_passed = False
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
    # Responsive Grid Display
    cols = st.columns(3)
    
    for index, video in enumerate(results):
        # Trigger Math Check Gate at every 10th milestone item (index 10, 20, etc.)
        if index > 0 and index % 10 == 0:
            if not st.session_state.gate_passed:
                st.markdown("---")
                st.subheader("🛑 Screen Time Break! Let's solve a puzzle to load more videos.")
                
                # Input container box
                with st.container(border=True):
                    st.write(f"What is: **{st.session_state.math_question}**?")
                    user_ans = st.number_input("Type your answer here:", value=None, step=1, key=f"gate_{index}")
                    
                    if user_ans is not None:
                        if user_ans == st.session_state.math_answer:
                            st.session_state.gate_passed = True
                            st.success("Great job! Loading more videos...")
                            st.rerun()
                        else:
                            st.error("Oops! Not quite right. Ask mom/dad for help! 💡")
                
                # Stop parsing the rest of the layout until condition is verified
                break

        # Render rows dynamically inside the standard grid columns 
        col_idx = index % 3
        with cols[col_idx]:
            st.video(f"https://www.youtube.com/watch?v={video['id']}")
            st.caption(f"**{video['title']}**")
            st.markdown(f"*Source: {video['channel']}*")
            st.write("")  # Margin spacing padding
