import streamlit as st
from summarizer import summarize_text
from sentiment_filter import is_positive
from news_fetcher import fetch_news
from translator import translate_text
from tts_converter import text_to_speech
import uuid, os, re
from datetime import date


st.set_page_config(page_title="NewsBuddy - Smart Personalized News Delivery System", layout="wide", page_icon="📰")
API_KEY = "d8286c819d22413f950d35ad1dcc3923"

if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []

st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #2A2A72, #009FFD);
            color: white;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: rgba(255,255,255,0.15);
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .navbar h1 {
            color: #fff;
            margin: 0;
            font-size: 28px;
        }
        .nav-buttons {
            display: flex;
            gap: 15px;
        }
        .nav-buttons button {
            background: #fff;
            color: #2A2A72;
            font-weight: bold;
            border: none;
            padding: 6px 14px;
            border-radius: 8px;
            cursor: pointer;
        }
        .card {
            background: white;
            color: black;
            border-radius: 15px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        }
        .title {
            font-size: 28px;
            font-weight: bold;
            color: #2A2A72;
        }
        .desc {
            font-size: 22px;
            color: #333;
        }
        .btn-row {
            margin-top: 8px;
        }
        .btn {
            background: #009FFD;
            color: white;
            padding: 5px 10px;
            border-radius: 6px;
            text-decoration: none;
            margin-right: 10px;
            font-size: 13px;
        }
    </style>
""", unsafe_allow_html=True)


col1, col2 = st.columns([2,3])
with col1:
    st.markdown("<div class='navbar'><h1>📰 NewsBuddy</h1></div>", unsafe_allow_html=True)

section = st.radio("", ["Home", "Search", "Bookmarks", "Login"], horizontal=True)

with st.expander("⚙️ Filters"):
    cities = ["Nagpur", "Delhi", "Mumbai", "Pune", "Chennai", "Bangalore", "Hyderabad", "Kolkata"]
    countries = {
        "India": "in", "USA": "us", "UK": "gb", "Canada": "ca",
        "Australia": "au", "France": "fr", "Germany": "de",
        "Japan": "jp", "China": "cn"
    }
    languages = {
        "English": "en", "Hindi": "hi", "Marathi": "mr", "French": "fr",
        "Spanish": "es", "German": "de", "Chinese": "zh-cn",
        "Japanese": "ja", "Arabic": "ar", "Russian": "ru"
    }

    selected_city = st.selectbox("🏙️ City", cities)
    selected_country = st.selectbox("🌎 Country", list(countries.keys()))
    selected_language = st.selectbox("🌐 Language", list(languages.keys()))
    from_date = st.date_input("📅 From Date", value=date.today())
    to_date = st.date_input("📅 To Date", value=date.today())


def display_article(article, idx, query=None):
    title = article.get("title", "No Title")
    desc = article.get("description", "")
    img_url = article.get("urlToImage", "https://via.placeholder.com/300x180?text=News")
    url = article.get("url", "#")

    summary = summarize_text(desc) if desc else "No description available."

   
    if query:
        summary = re.sub(f"({query})", r"<mark>\1</mark>", summary, flags=re.IGNORECASE)

    
    if selected_language != "English":
        summary = translate_text(summary, languages[selected_language])

    st.markdown(f"""
    <div class="card">
        <img src="{img_url}" width="100%" style="border-radius:10px; margin-bottom:10px;">
        <div class="title">{title}</div>
        <p class="desc">{summary}</p>
        <div class="btn-row">
            <a class="btn" href="{url}" target="_blank">🔗 Read More</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1,1])
    with c1:
        if st.button(f"🔊 Listen {idx}", key=f"listen_{idx}"):
            filename = f"output_{uuid.uuid4().hex}.mp3"
            filepath = text_to_speech(summary, filename, lang_code=languages[selected_language])
            if filepath and os.path.exists(filepath):
                st.audio(filepath)
    with c2:
        if st.button(f"⭐ Save {idx}", key=f"save_{idx}"):
            st.session_state["bookmarks"].append({"title": title, "summary": summary, "url": url})
            st.success("✅ Saved to Bookmarks")


if section == "Home":
    st.subheader(f"🏠 News from {selected_city}, {selected_country}")

    categories = ["Business", "Technology", "Sports", "Entertainment", "Science", "Health", "Politics", "General"]
    tabs = st.tabs(categories)

    for idx, cat in enumerate(categories):
        with tabs[idx]:
            articles = fetch_news(API_KEY,
                                  category=cat.lower(),
                                  country=countries[selected_country],
                                  city=selected_city)
            if not articles:
                st.warning("⚠ No news found")
            for i, article in enumerate(articles[:5], 1):
                display_article(article, f"{cat}_{i}")


elif section == "Search":
    st.subheader("🔎 Search News")
    query = st.text_input("Enter keywords")
    sentiment_only = st.checkbox("Show only Positive News")
    if st.button("Search"):
        articles = fetch_news(API_KEY,
                              category="general",
                              country=countries[selected_country],
                              city=selected_city,
                              from_date=str(from_date),
                              to_date=str(to_date))
        for i, article in enumerate(articles[:8], 1):
            if sentiment_only and not is_positive(article.get("description", "")):
                continue
            display_article(article, f"search_{i}", query=query)


elif section == "Bookmarks":
    st.subheader("🔖 Saved Articles")
    if st.session_state["bookmarks"]:
        for i, b in enumerate(st.session_state["bookmarks"], 1):
            st.markdown(f"""
            <div class="card">
                <div class="title">{b['title']}</div>
                <p class="desc">{b['summary']}</p>
                <a class="btn" href="{b['url']}" target="_blank">🔗 Read More</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📌 No bookmarks yet.")


elif section == "Login":
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.success(f"✅ Logged in as {email}")
