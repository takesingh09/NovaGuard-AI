import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import time
import base64
import sys
import os

# Path setup to ensure backend modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.pdf_parser import extract_text_from_pdf
    from backend.nova_manager import NovaManager
except ImportError:
    # Fallback only for internal preview environments
    def extract_text_from_pdf(file): return "Sample Resume Content"
    class NovaManager:
        def __init__(self): self.credentials_ok = True
        def analyze_career_gap(self, r, j): 
            return {
                "match_score": 75, "matching_skills": ["Python", "AWS"], "missing_skills": ["Nova API"],
                "roadmap": [{"day": "1-3", "topic": "Basics", "activity": "Study"}],
                "advice": "Keep going! You are doing great."
            }
        def fetch_learning_resources(self, s): return []

load_dotenv()

st.set_page_config(page_title="Nova Career-Pilot", page_icon="🚀", layout="wide")

# Enhanced UI styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    :root {
        --primary-orange: #FF9900;
        --nova-gradient: linear-gradient(135deg, #FF9900 0%, #FFB347 50%, #E47911 100%);
        --glass-bg: rgba(255, 255, 255, 0.06);
        --glass-border: rgba(255, 255, 255, 0.12);
        --surface: #10141c;
        --surface-soft: #151b24;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --accent-blue: #38bdf8;
    }
    .stApp {
        background: radial-gradient(circle at top right, rgba(255, 153, 0, 0.12), transparent 35%),
                    radial-gradient(circle at left, rgba(56, 189, 248, 0.08), transparent 40%),
                    #0b0f16;
        color: var(--text-main);
        font-family: 'Manrope', sans-serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    h1 {
        background: var(--nova-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-shell {
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
        border-radius: 28px;
        border: 1px solid var(--glass-border);
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.35);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    .hero-shell::after {
        content: "";
        position: absolute;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: rgba(56, 189, 248, 0.15);
        top: -70px;
        right: -60px;
        filter: blur(10px);
        animation: float 6s ease-in-out infinite;
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.12);
        color: var(--accent-blue);
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 1.05rem;
        margin-bottom: 1.6rem;
    }
    .hero-highlights {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .highlight-card {
        flex: 1 1 170px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1rem 1.2rem;
        animation: fadeInUp 0.9s ease-out;
    }
    .highlight-title {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }
    .highlight-value {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .input-card {
        background: var(--surface-soft);
        border: 1px solid var(--glass-border);
        padding: 1.7rem;
        border-radius: 20px;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.02);
        animation: fadeInUp 0.9s ease-out;
    }
    .section-title {
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .section-helper {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: var(--surface);
        padding: 1.4rem;
        border-radius: 18px;
        text-align: center;
        border: 1px solid var(--glass-border);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.3);
        animation: fadeInUp 0.9s ease-out;
    }
    .metric-label {
        color: var(--text-muted);
        margin-bottom: 0.4rem;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
    }
    .roadmap-step {
        position: relative;
        padding: 1rem 1.2rem 1rem 2.4rem;
        margin-bottom: 1rem;
        border-left: 2px dashed rgba(255, 153, 0, 0.4);
        background: rgba(255, 255, 255, 0.02);
        border-radius: 14px;
        animation: fadeInUp 0.8s ease-out;
    }
    .roadmap-step::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 1.2rem;
        width: 16px;
        height: 16px;
        background: var(--primary-orange);
        border-radius: 50%;
        box-shadow: 0 0 0 6px rgba(255, 153, 0, 0.1);
    }
    .skill-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        margin: 4px 6px 0 0;
        font-size: 0.8rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .skill-match { background: rgba(34, 197, 94, 0.12); color: #4ade80; }
    .skill-miss { background: rgba(239, 68, 68, 0.12); color: #f87171; }
    .advice-box {
        background: rgba(255, 153, 0, 0.08);
        border: 1px solid rgba(255, 153, 0, 0.2);
        padding: 1.5rem;
        border-radius: 18px;
        margin: 1.2rem 0 1.6rem;
        animation: fadeInUp 0.8s ease-out;
    }
    .setup-warning {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #f87171;
        padding: 1rem;
        border-radius: 12px;
        color: #f87171;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        background: var(--nova-gradient);
        color: #111827;
        font-weight: 700;
        border: none;
        border-radius: 999px;
        padding: 0.85rem 1.5rem;
        box-shadow: 0 10px 25px rgba(255, 153, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 35px rgba(255, 153, 0, 0.35);
    }
    .footer {
        text-align:center;
        margin-top:4rem;
        padding:2rem;
        color:#64748b;
        font-size:0.85rem;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(10px); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Check for AWS Credentials Readiness
nova = NovaManager()
if not nova.credentials_ok:
    st.markdown("""
    <div class="setup-warning">
        ⚠️ <b>AWS Setup Required:</b> Bedrock credentials not found. Please check your .env file or AWS CLI configuration to enable AI Analysis.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero-shell">
    <div class="hero-tag">🚀 Nova Career-Pilot</div>
    <h1>Design your next career move with confidence.</h1>
    <p class="hero-subtitle">Upload your resume, map it against a dream role, and receive a tailored growth roadmap powered by Nova intelligence.</p>
    <div class="hero-highlights">
        <div class="highlight-card">
            <div class="highlight-title">Insight Engine</div>
            <div class="highlight-value">Skill gap analysis</div>
        </div>
        <div class="highlight-card">
            <div class="highlight-title">Personalized</div>
            <div class="highlight-value">15-day action plan</div>
        </div>
        <div class="highlight-card">
            <div class="highlight-title">Curated</div>
            <div class="highlight-value">Learning resources</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📂 Resume (PDF)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-helper">Drop in your latest resume to begin the analysis.</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Job Description</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-helper">Paste a target role description to benchmark your fit.</div>', unsafe_allow_html=True)
        job_description = st.text_area("Job Description", height=120, placeholder="Example: Senior Web Developer at Amazon...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
if st.button("✨ Analyze Career Path", width="stretch"):
    if not uploaded_file or not job_description:
        st.warning("Please provide both Resume and Job Description! 😊")
    elif not nova.credentials_ok:
        st.error("Cannot proceed without AWS Credentials. Check your setup and retry.")
    else:
        with st.status("🚀 Nova is scanning the horizon...", expanded=True) as status:
            resume_text = extract_text_from_pdf(uploaded_file)
            try:
                result = nova.analyze_career_gap(resume_text, job_description)
                
                if "error" in result:
                    status.update(label="Setup Issue Found", state="error", expanded=True)
                    st.error(f"Nova Error: {result['error']}")
                else:
                    status.update(label="Analysis Ready!", state="complete", expanded=False)

                    # 💡 Mentorship Suggestion Box
                    st.markdown(f"""
                    <div class="advice-box">
                        <h4 style="margin:0; color:#FF9900;">💡 Mentorship Insight</h4>
                        <p style="margin:10px 0 0 0; font-style:italic;">"{result.get('advice', 'Keep pushing your boundaries!')}"</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.markdown(
                        f'<div class="metric-box"><div class="metric-label">Match Score</div>'
                        f'<div class="metric-value" style="color:#FFB347">{result.get("match_score", 0)}%</div></div>',
                        unsafe_allow_html=True
                    )
                    m2.markdown(
                        f'<div class="metric-box"><div class="metric-label">Skills Matched</div>'
                        f'<div class="metric-value" style="color:#4ade80">{len(result.get("matching_skills", []))}</div></div>',
                        unsafe_allow_html=True
                    )
                    m3.markdown(
                        f'<div class="metric-box"><div class="metric-label">Critical Gaps</div>'
                        f'<div class="metric-value" style="color:#f87171">{len(result.get("missing_skills", []))}</div></div>',
                        unsafe_allow_html=True
                    )

                    st.write("")
                    t1, t2, t3 = st.tabs(["📊 Skill Map", "📅 15-Day Roadmap", "📚 Learning Resources"])

                    with t1:
                        col_a, col_b = st.columns([1, 1])
                        with col_a:
                            st.write("✅ **Your Strengths**")
                            for s in result.get("matching_skills", []):
                                st.markdown(f'<span class="skill-pill skill-match">{s}</span>', unsafe_allow_html=True)
                        with col_b:
                            st.write("⚠️ **Gap Analysis**")
                            for s in result.get("missing_skills", []):
                                st.markdown(f'<span class="skill-pill skill-miss">{s}</span>', unsafe_allow_html=True)

                    with t2:
                        roadmap = result.get("roadmap", [])
                        if roadmap:
                            for item in roadmap:
                                st.markdown(f"""
                                <div class="roadmap-step">
                                    <strong style="color:#FFB347">Day {item.get('day', '??')} · {item.get('topic', 'Topic')}</strong><br/>
                                    <span style="color:#cbd5e1; font-size:0.95rem;">{item.get('activity', '')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("AI couldn't generate a roadmap for this specific JD. Try pasting more details.")

                    with t3:
                        st.write("#### AI-Curated Learning Path")
                        resources = nova.fetch_learning_resources(result.get("missing_skills", []))
                        for res in resources:
                            st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.05); padding:1rem; border-radius:14px; border:1px solid rgba(255,255,255,0.1); margin-bottom:0.8rem;">
                                <h5 style="margin:0;">{res['title']}</h5>
                                <a href="{res['url']}" target="_blank" style="color:#3b82f6; text-decoration:none; font-size:0.9rem;">Start Learning →</a>
                            </div>
                            """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Unexpected Orbit Error: {e}")

# --- Footer ---
st.markdown("""
<div class="footer">
    Powered by Amazon Nova 2 & Streamlit | Built with 🧡 for the Nova Hackathon
</div>
""", unsafe_allow_html=True)
