import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")  # Replace with your key or use Streamlit Secrets

st.set_page_config(page_title="Content Repurposer", layout="centered")

st.title("🪄 Content Repurposer Bot")
st.write("Turn a blog or LinkedIn post into social media gold 🧵📩📸")

# Input area
post_input = st.text_area("Paste your blog or LinkedIn post:", height=300)
tone = st.selectbox("Choose a tone:", ["Professional", "Witty", "Inspiring"])

if st.button("Repurpose Content") and post_input:
    with st.spinner("🧠 Thinking..."):

        prompt = f"""
You are a social media content strategist.

Take the following post and rewrite it into 4 formats:
1. A tweet thread (max 5 tweets)
2. An Instagram caption with emojis and hashtags
3. A short email teaser for a newsletter
4. A bold hook line to grab attention

Tone: {tone}
Post:
{post_input}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )

            output = response['choices'][0]['message']['content']
            st.success("Here’s your repurposed content 👇")
            st.text_area("Repurposed Outputs", output, height=400)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("---")
st.markdown("Made with ❤️ by a solo founder exploring AI")
