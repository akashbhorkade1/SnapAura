import streamlit as st
import requests
import time

# 🔐 Replicate API setup
REPLICATE_API_TOKEN = "r8_VkpuI6caYPYR8RCkMAwCFoAZBO4VCkB3lHTWe"
GFPGAN_VERSION = "297a243ce8643961d52f745f9b6c8c1bd96850a51c92be5f43628a0d3e08321a"

# 🖼️ Page config
st.set_page_config(page_title="SnapAura – AI Photo Enhancer", layout="centered")

# 🎨 Branding
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://i.ibb.co/6WZyZpY/snapaura-logo.png' width='120'>
        <h1 style='color: #6C63FF;'>SnapAura</h1>
        <p style='font-size: 18px;'>AI-powered photo restoration in seconds</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 🎨 Grey background + animation
st.markdown(
    """
    <style>
    body {
        background-color: #e0e0e0;
    }
    .stSpinner > div {
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 📤 Input options
st.markdown("### 📤 Choose your input method")
uploaded_file = st.file_uploader("Upload a JPG or PNG", type=["jpg", "jpeg", "png"])
image_url = st.text_input("Or paste a public image URL")

# 🖼️ Preview uploaded file
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.warning("Enhancement only works with public URLs. Upload your image to imgbb.com or postimages.org to get a link.")

# 🧠 Use public URL for enhancement
if image_url and image_url.startswith("http"):
    with st.spinner("🔄 Enhancing your photo... Please wait"):
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {REPLICATE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "version": GFPGAN_VERSION,
                "input": {"img": image_url}
            }
        )

        if response.status_code == 201:
            prediction = response.json()
            status_url = prediction["urls"]["get"]

            while True:
                result = requests.get(status_url, headers={"Authorization": f"Token {REPLICATE_API_TOKEN}"}).json()
                if result["status"] == "succeeded":
                    raw_output = result.get("output", None)

                    # ✅ Handle both list and string formats
                    if isinstance(raw_output, list) and raw_output and isinstance(raw_output[0], str) and raw_output[0].startswith("http"):
                        output_url = raw_output[0]
                    elif isinstance(raw_output, str) and raw_output.startswith("http"):
                        output_url = raw_output
                    else:
                        output_url = None

                    if output_url:
                        st.success("✅ Enhancement complete!")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 🖼️ Original")
                            st.image(image_url, use_column_width=True)
                        with col2:
                            st.markdown("### ✨ Enhanced")
                            st.image(output_url, use_column_width=True)

                        st.markdown(
                            f"<a href='{output_url}' download style='font-size:18px;'>📥 Download Enhanced Photo</a>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.error("Invalid enhanced image URL. Please try a different image.")
                    break

                elif result["status"] == "failed":
                    st.error("Enhancement failed. Try another image.")
                    break

                time.sleep(1)
        else:
            st.error("Something went wrong. Check your API key or image format.")
            st.text(f"Status code: {response.status_code}")
            st.text(f"Response: {response.text}")

# 🪪 Footer
st.markdown(
    """
    <hr>
    <p style='text-align: center; font-size: 14px;'>
        Built with ❤️ by Akash | Powered by Replicate & Streamlit
    </p>
    """,
    unsafe_allow_html=True
)