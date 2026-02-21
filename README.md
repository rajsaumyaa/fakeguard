# 🔍 FakeGuard — AI-Powered Fake News Detector

A sleek, dark-themed web app that analyzes news articles and headlines for credibility using AI. Built with **Streamlit** and powered by **Groq's free API** (LLaMA 3.3 70B).

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Free%20API-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- **Verdict** — Classifies news as `REAL`, `FAKE`, or `UNCERTAIN` with a confidence score
- **Red Flags** — Detects sensationalist language, unverifiable claims, emotional manipulation
- **Credibility Signals** — Highlights positive indicators like named sources and verifiable facts
- **Detailed Analysis** — Multi-paragraph AI reasoning behind the verdict
- **Source Suggestions** — Recommends trusted sources to verify the claim
- **Sleek Dark UI** — Custom-styled with Syne + IBM Plex Mono fonts and color-coded verdict cards

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or 3.12
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/rajsaumyaa/fakeguard.git
cd fakeguard
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv1
venv1\Scripts\activate        # Windows
source venv1/bin/activate     # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set your Groq API key permanently (run once):**
```powershell
# Windows PowerShell
[System.Environment]::SetEnvironmentVariable("GROQ_API_KEY", "gsk_your-key-here", "User")
```
```bash
# Mac/Linux
echo 'export GROQ_API_KEY="gsk_your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**5. Run the app:**
```bash
streamlit run fake_news_detector.py
```

The app will open automatically at `http://localhost:8501`

---

## 🖥️ Usage

1. Paste any news article, headline, or claim into the text box
2. Click **Analyze Now**
3. Get an instant AI-powered credibility verdict with detailed reasoning

---

## 📁 Project Structure

```
fakeguard/
├── fake_news_detector.py   # Main Streamlit app
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Groq](https://groq.com) | Free AI API (LLaMA 3.3 70B) |
| Python 3.11+ | Backend language |

---

## 📦 Dependencies

```
streamlit>=1.35.0
groq>=0.9.0
```

---

## ⚡ Daily Run Commands

Every time you want to run the app:
```bash
cd "C:\Users\hp\OneDrive\Attachments\Desktop\fakeguard"
venv1\Scripts\activate
streamlit run fake_news_detector.py
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> **Disclaimer:** FakeGuard is an AI-assisted tool and should not be used as the sole source of truth. Always verify information with trusted primary sources.
