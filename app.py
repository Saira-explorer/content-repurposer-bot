import streamlit as st
import requests

# Hugging Face model endpoint (use Mistral for quality + speed)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Store in Streamlit Secrets (for free use)

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.set_page_config(page_title="Content Repurposer Bot", layout="centered")
st.title("🪄 Content Repurposer Bot (Free Hugging Face Version)")
st.write("Turn a blog or LinkedIn post into tweets, captions, emails, and hooks!")

post_input = st.text_area("✍️ Paste your blog or LinkedIn post:", height=300)
tone = st.selectbox("🎙️ Choose the tone:", ["Professional", "Witty", "Inspiring"])

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"⚠️ Error {response.status_code}: {response.text}"

if st.button("🔁 Repurpose Content") and post_input:
    with st.spinner("Generating using free model..."):

        prompt = f"""
You are a social media content strategist.

Take the following long-form post and rewrite it into 4 formats:
1. A tweet thread (max 5 tweets)
2. An Instagram caption with emojis and hashtags
3. A short email teaser for a newsletter
4. A bold hook line to grab attention

Tone: {tone}
Post:
{post_input}
        """

        output = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 400, "temperature": 0.7}
        })

        st.success("✅ Repurposed content is ready!")
        st.text_area("📄 Output", output, height=400)

st.markdown("---")
st.markdown("Built using free Hugging Face models — no OpenAI key needed 🚀
