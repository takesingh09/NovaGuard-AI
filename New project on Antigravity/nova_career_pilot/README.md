# 🚀 Nova Career-Pilot

An AI-powered career mentorship platform designed for B.Tech CSE students. Use the power of **Amazon Nova 2 Lite** and **Nova Act** to bridge your skill gap and land your dream job.

## 🌟 Key Features
- **Smart Gap Analysis**: Analyzes your Resume vs Job Description to find missing skills.
- **15-Day Learning Roadmap**: Auto-generated personalized study plan.
- **AI-Curated Resources**: Fetches top documentation and video tutorials.
- **Visual Analytics**: Radar charts and match scores for instant insights.
- **Dark Mode UI**: Professional Amazon-themed interface with glassmorphism.

## 🔧 Tech Stack
- **Frontend**: Streamlit, Plotly (Glassmorphism UI)
- **AI Core**: AWS Bedrock (Amazon Nova 2 Lite)
- **Agents**: Simulated Nova Act behavior (Python/Boto3)
- **PDF Processing**: PyPDF2
- **Language**: Python 3.9+

## ⚙️ Setup Instructions

1.  **Clone this repository**
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    - Rename `.env.example` to `.env`
    - Add your AWS Credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
    - Ensure your AWS region is enabled for Bedrock and Nova models (default: `us-east-1`).
4.  **Run the Application**:
    ```bash
    streamlit run frontend/app.py
    ```

## 📂 Project Structure
```
nova_career_pilot/
├── frontend/
│   └── app.py              # Main Application Entry Point
├── backend/
│   └── nova_manager.py     # Bedrock Interaction Layer
├── utils/
│   └── pdf_parser.py       # PDF Text Extraction
├── requirements.txt        # Dependencies
├── .env.example            # Environment Config
└── assets/                 # Static files
```
