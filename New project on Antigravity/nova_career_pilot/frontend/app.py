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

# Enhanced CSS for better contrast and Hackathon feel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    :root { --primary-orange: #FF9900; --nova-gradient: linear-gradient(135deg, #FF9900 0%, #E47911 100%); }
    .stApp { background: #0b0d11; color: #f8fafc; }
    .hero-container { padding: 2rem; background: rgba(255, 255, 255, 0.02); border-radius: 30px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 2rem; }
    h1 { font-family: 'Space Grotesk', sans-serif !important; background: var(--nova-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .input-card { background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 20px; }
    .metric-box { background: rgba(255, 255, 255, 0.03); padding: 1.2rem; border-radius: 15px; text-align: center; border-bottom: 3px solid var(--primary-orange); }
    .roadmap-step { position: relative; padding-left: 2rem; margin-bottom: 1rem; border-left: 2px dashed rgba(255, 153, 0, 0.3); }
    .roadmap-step::before { content: ''; position: absolute; left: -9px; top: 0; width: 16px; height: 16px; background: var(--primary-orange); border-radius: 50%; }
    .skill-pill { display: inline-block; padding: 5px 12px; border-radius: 8px; margin: 3px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.1); }
    .skill-match { background: rgba(34, 197, 94, 0.1); color: #4ade80; }
    .skill-miss { background: rgba(239, 68, 68, 0.1); color: #f87171; }
    .advice-box { background: rgba(255, 153, 0, 0.05); border: 1px solid rgba(255, 153, 0, 0.2); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; }
    .setup-warning { background: rgba(239, 68, 68, 0.1); border: 1px solid #f87171; padding: 1rem; border-radius: 10px; color: #f87171; text-align: center; margin-bottom: 2rem; }
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

st.markdown('<div class="hero-container"><h1>Nova Career-Pilot</h1><p style="color: #94a3b8;">Bridge the gap between your resume and your dream role.</p></div>', unsafe_allow_html=True)

with st.container():
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("📂 Resume (PDF)")
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.subheader("🎯 Job Description")
        job_description = st.text_area("Job Description", height=100, placeholder="Example: Senior Web Developer at Amazon...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

st.write("")
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
                    m1.markdown(f'<div class="metric-box"><div>Match Score</div><div style="font-size:2.5rem; font-weight:700; color:#FF9900">{result.get("match_score", 0)}%</div></div>', unsafe_allow_html=True)
                    m2.markdown(f'<div class="metric-box"><div>Skills Matched</div><div style="font-size:2.5rem; font-weight:700; color:#4ade80">{len(result.get("matching_skills", []))}</div></div>', unsafe_allow_html=True)
                    m3.markdown(f'<div class="metric-box"><div>Critical Gaps</div><div style="font-size:2.5rem; font-weight:700; color:#f87171">{len(result.get("missing_skills", []))}</div></div>', unsafe_allow_html=True)

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
                                    <strong style="color:#FF9900">Day {item.get('day', '??')} - {item.get('topic', 'Topic')}</strong><br/>
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
                            <div style="background:rgba(255,255,255,0.05); padding:1rem; border-radius:12px; border:1px solid rgba(255,255,255,0.1); margin-bottom:0.8rem;">
                                <h5 style="margin:0;">{res['title']}</h5>
                                <a href="{res['url']}" target="_blank" style="color:#3b82f6; text-decoration:none; font-size:0.9rem;">Start Learning →</a>
                            </div>
                            """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Unexpected Orbit Error: {e}")

# --- Footer ---
st.markdown("""
<div style="text-align:center; margin-top:5rem; padding:2rem; color:#475569; font-size:0.8rem;">
    Powered by Amazon Nova 2 & Streamlit | Built with 🧡 for the Nova Hackathon
</div>
""", unsafe_allow_html=True)