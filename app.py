import streamlit as st
import time

# --- CONFIG & STYLING ---
st.set_page_config(
    page_title="Election Assistant",
    page_icon="🗳️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Civic Educational Theme
st.markdown("""
    <style>
    /* Adapts to user's browser Dark/Light Mode automatically */
    .main-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #0d6efd, #0dcaf0);
        color: white;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .timeline-card {
        background-color: rgba(13, 110, 253, 0.08); /* Semi-transparent blue */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0d6efd;
        margin-bottom: 20px;
    }
    .step-number {
        background: #0d6efd;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

import requests

# --- HELPER FUNCTIONS ---
@st.cache_data(ttl=600) # Cache for 10 mins
def fetch_india_election_news():
    api_key = "91e973e1024e424696e9daf84359a8f2"
    url = f"https://newsapi.org/v2/everything?q=India+Election&apiKey={api_key}&pageSize=5&sortBy=publishedAt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('articles', [])
        return []
    except:
        return []

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1907/1907579.png", width=100) # Open source icon
    st.title("🗳️ Civic Guide")
    st.markdown("Your interactive guide to understanding democracy.")
    
    page = st.radio("Choose a Module:", [
        "🗺️ Election Journey", 
        "📚 Process & Rules", 
        "✅ Voter Eligibility Checker"
    ])
    
    st.markdown("---")
    
    # LIVE NEWS TIMELINE IN SIDEBAR
    st.subheader("📰 Live India Election News")
    news_articles = fetch_india_election_news()
    
    if news_articles:
        for article in news_articles:
            # Clean up date
            date_str = article.get('publishedAt', '')[:10]
            st.markdown(f"""
            <div style="font-size: 0.85rem; margin-bottom: 15px; border-left: 2px solid #0d6efd; padding-left: 10px;">
                <strong style="color: #0d6efd;">{date_str}</strong><br>
                <a href="{article.get('url')}" target="_blank" style="text-decoration: none; color: inherit;">
                    {article.get('title')}
                </a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Unable to fetch live news at the moment.")
        
    st.markdown("---")
    st.info("💡 **Did you know?**\nIndia has the largest democratic election in the world!")

# --- HEADER ---
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'>Democracy Assistant</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Empowering voters through interactive education.</p>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE LOGIC ---

if page == "🗺️ Election Journey":
    st.header("Interactive Election Timeline")
    st.write("Drag the slider to explore the different phases of an election.")
    
    phases = [
        "1. Announcement", 
        "2. Voter Registration", 
        "3. Nominations", 
        "4. Campaigning", 
        "5. Polling Day", 
        "6. Counting & Results"
    ]
    
    selected_phase = st.select_slider("Select Phase:", options=phases)
    
    st.markdown("---")
    
    if selected_phase == phases[0]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">1</span> Election Announcement</h3>
            <p>The Election Commission (EC) officially announces the election dates. This triggers the <strong>Model Code of Conduct</strong>.</p>
            <ul>
                <li>Dates for voting and counting are finalized.</li>
                <li>Government cannot announce new schemes.</li>
                <li>Ensures a level playing field for all parties.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_phase == phases[1]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">2</span> Voter Registration</h3>
            <p>Citizens ensure their names are on the electoral rolls. Without this, you cannot vote!</p>
            <ul>
                <li>New voters (turning 18) fill out Form 6.</li>
                <li>Voter ID cards (EPIC) are issued.</li>
                <li>Rolls are verified and finalized by Booth Level Officers.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_phase == phases[2]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">3</span> Candidate Nominations</h3>
            <p>Political parties and independent candidates officially enter the race.</p>
            <ul>
                <li>Candidates file affidavits declaring assets and criminal records.</li>
                <li>The EC scrutinizes the papers to ensure validity.</li>
                <li>Candidates can withdraw before a final deadline.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_phase == phases[3]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">4</span> Campaigning</h3>
            <p>The most visible part of the election! Candidates reach out to voters to explain their manifestos.</p>
            <ul>
                <li>Public rallies, door-to-door visits, and digital ads.</li>
                <li>Must strictly follow EC spending limits and rules.</li>
                <li>Campaigning stops 48 hours before voting day (Silence Period).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_phase == phases[4]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">5</span> Polling Day</h3>
            <p>The day voters exercise their democratic right.</p>
            <ul>
                <li>Voters verify identity at the polling booth.</li>
                <li>Votes are cast secretly using Electronic Voting Machines (EVMs).</li>
                <li>Security forces ensure peaceful voting.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_phase == phases[5]:
        st.markdown("""
        <div class="timeline-card">
            <h3><span class="step-number">6</span> Counting & Results</h3>
            <p>The EVMs are unsealed and votes are counted under heavy security.</p>
            <ul>
                <li>Results are announced constituency by constituency.</li>
                <li>The party (or coalition) with the majority forms the government.</li>
                <li>Democracy in action!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

elif page == "📚 Process & Rules":
    st.header("Understand the Rules")
    st.write("Click on the topics below to learn about key election concepts.")
    
    with st.expander("What is the Model Code of Conduct (MCC)?"):
        st.write("""
        The MCC is a set of guidelines issued by the Election Commission to regulate political parties and candidates prior to elections. 
        - **Why?** To ensure free and fair elections.
        - **Rule 1:** No party can use religious places for campaign platforms.
        - **Rule 2:** The ruling party cannot use government transport or machinery for campaigning.
        """)
        
    with st.expander("How do Electronic Voting Machines (EVMs) work?"):
        st.write("""
        EVMs are standalone machines used to cast votes securely.
        - They are **not** connected to the internet, making them safe from remote hacking.
        - A voter presses the blue button next to the candidate's symbol.
        - A slip is generated by the VVPAT (Voter Verifiable Paper Audit Trail) for 7 seconds so the voter can verify their choice.
        """)
        
    with st.expander("What is NOTA?"):
        st.write("""
        **None Of The Above (NOTA)** is an option on the EVM.
        If a voter feels none of the candidates in their constituency are worthy, they can press NOTA. While NOTA doesn't change the election outcome (even if it gets the most votes, the runner-up wins), it registers a strong protest vote.
        """)

elif page == "✅ Voter Eligibility Checker":
    st.header("Are you ready to vote?")
    st.write("Take this quick interactive test to see if you are eligible to participate in the upcoming elections.")
    
    with st.container():
        age = st.number_input("What is your age?", min_value=0, max_value=120, value=17)
        citizen = st.radio("Are you a citizen of the country?", ["Yes", "No"])
        registered = st.radio("Is your name on the electoral roll (voter list)?", ["Yes", "No", "I don't know"])
        
        if st.button("Check Eligibility"):
            with st.spinner("Analyzing criteria..."):
                time.sleep(1) # Fake processing time for interactive feel
                
                if age >= 18 and citizen == "Yes" and registered == "Yes":
                    st.success("🎉 **Congratulations!** You are fully eligible and ready to vote. Keep your Voter ID handy on polling day!")
                    # Custom CSS animation for a voting hand instead of balloons
                    st.markdown("""
                        <style>
                        @keyframes vote-animation {
                            0% { transform: translateY(50px) scale(0.8); opacity: 0; }
                            50% { transform: translateY(-10px) scale(1.1); opacity: 1; }
                            100% { transform: translateY(0) scale(1); opacity: 1; }
                        }
                        .voting-hand-container {
                            display: flex;
                            justify-content: center;
                            margin: 20px 0;
                            animation: vote-animation 1s ease-out forwards;
                        }
                        .voting-hand {
                            font-size: 80px;
                            filter: drop-shadow(0 10px 10px rgba(0,0,0,0.2));
                        }
                        </style>
                        <div class="voting-hand-container">
                            <div class="voting-hand">🗳️✋</div>
                        </div>
                    """, unsafe_allow_html=True)
                elif age < 18:
                    st.error(f"⏳ **Not quite yet.** You need to be at least 18 years old to vote. You have {18 - age} year(s) to go!")
                elif citizen == "No":
                    st.error("🚫 **Ineligible.** Only citizens of the country are permitted to vote in national/state elections.")
                elif registered == "No" or registered == "I don't know":
                    st.warning("⚠️ **Action Required!** Even if you are 18 and a citizen, you cannot vote unless your name is on the electoral roll. Please visit the Election Commission website to register via Form 6.")
                else:
                    st.info("Please fill out the form accurately.")

# Footer
st.markdown("<br><hr><p style='text-align:center; color:#888; font-size:0.8rem;'>Built for Civic Education | Lightweight Interactive App (< 10MB)</p>", unsafe_allow_html=True)