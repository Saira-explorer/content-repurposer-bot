import streamlit as st
from openai import OpenAI

# Set your OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app setup
st.set_page_config(page_title="Content Repurposer Bot", layout="centered")
st.title("🪄 Content Repurposer Bot")
st.write("Paste a blog or LinkedIn post, and get it repurposed for Twitter, Instagram, and more!")

# User input
post_input = st.text_area("✍️ Paste your blog or LinkedIn post here:", height=300)
tone = st.selectbox("🎙️ Choose the tone you want:", ["Professional", "Witty", "Inspiring"])

# When user clicks the button
if st.button("🔁 Repurpose Content") and post_input:
    with st.spinner("Generating repurposed content..."):

        # Prompt template
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

        try:
            # OpenAI call using new SDK
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800
            )

            output = response.choices[0].message.content
            st.success("✅ Your repurposed content is ready!")
            st.text_area("📄 Output", output, height=400)
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Footer
st.markdown("---")
st.markdown("Built by a solo founder exploring AI entrepreneurship 🚀")
