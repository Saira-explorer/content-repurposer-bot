import streamlit as st
import requests

# Hugging Face inference endpoint for Zephyr-7B model
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Store securely in Streamlit secrets

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Streamlit UI setup
st.set_page_config(page_title="Content Repurposer Bot", layout="centered")
st.title("🪄 Content Repurposer Bot (Hugging Face Edition)")
st.write("Paste a blog or LinkedIn post and get tweet threads, Instagram captions, email teasers, and more.")

# User input
post_input = st.text_area("✍️ Paste your long-form post here:", height=300)
tone = st.selectbox("🎙️ Choose tone:", ["Professional", "Witty", "Inspiring"])

# Define query function
def query_hf_model(prompt):
    response = requests.post(API_URL, headers=headers, json={
        "inputs": prompt,
        "parameters": {
            "temperature": 0.5,
            "max_new_tokens": 500,
            "return_full_text": False
        }
    })
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"⚠️ Error {response.status_code}: {response.text}"

# On button click
if st.button("🔁 Repurpose Content") and post_input:
    with st.spinner("Generating repurposed formats..."):

        prompt = f"""
You are a social media content repurposing expert.

Take the post below and generate:

---

🐦 TWEET THREAD (Numbered 1/ to 5/)

📸 INSTAGRAM CAPTION (Use emojis + 3 hashtags)

✉️ EMAIL TEASER (2 lines, catchy)

🎯 HOOK LINE (Short, bold, max 10 words)

---

Tone: {tone}

Post:
{post_input}
        """

        result = query_hf_model(prompt)

        # Display sections (splitting optional)
        st.markdown("### 🐦 Tweet Thread")
        st.code(result.split("📸")[0].strip())

        if "📸" in result:
            rest = result.split("📸")[1]
            insta, email, hook = rest.split("✉️")[0], rest.split("✉️")[1].split("🎯")[0], rest.split("🎯")[1]

            st.markdown("### 📸 Instagram Caption")
            st.code(insta.strip())

            st.markdown("### ✉️ Email Teaser")
            st.code(email.strip())

            st.markdown("### 🎯 Hook Line")
            st.code(hook.strip())

# Footer
st.markdown("---")
st.caption("Powered by Hugging Face • No OpenAI key needed 🚀")
