import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import time
import requests
from io import BytesIO
from openai import OpenAI

# --- Setup & Helper Functions ---
st.set_page_config(page_title="GenAI Art Protection Simulator", layout="wide")

def apply_noise(img, intensity=15):
    """Simulates basic adversarial noise."""
    data = np.array(img, dtype=float)
    noise = np.random.normal(0, intensity, data.shape)
    noisy_data = np.clip(data + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_data)

def apply_ocr_poisoning(img):
    """Simulates Nightshade's conceptual poisoning."""
    poisoned_img = apply_noise(img, intensity=25)
    draw = ImageDraw.Draw(poisoned_img)
    draw.text((20, 20), "GALAXY DEEP SPACE STARS", fill=(150, 150, 150))
    return poisoned_img

@st.cache_data
def load_image_from_url(url):
    """Fetches an image from a URL and converts it for processing."""
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")

def generate_dynamic_image(prompt, api_key):
    """Calls the OpenAI DALL-E 3 API to generate an image."""
    try:
        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        return str(e)

api_key = st.secrets["OPENAI_API_KEY"]

# ==========================================
# STEP 0: Introduction
# ==========================================
st.title("🛡️ ArtShield: GenAI Protection Simulator")
st.markdown("""
**Welcome!** This simulation is designed for digital artists who want to protect their art from being scraped and reproduced by Generative AI models. 

*Note: True tools like Nightshade and Glaze require heavy GPU compute to calculate precise mathematical perturbations. This app is an educational simulation to demonstrate **how the AI sees and behaves** when encountering protected images.*
""")
st.divider()

# ==========================================
# STEP 1: Image Selection Gallery
# ==========================================
st.header("Step 1: Choose Your Canvas")
st.write("Select an image from the catalog below, or upload your own.")

# Catalog Data with specific hardcoded descriptions for Step 3
catalog_data = {
    "City": {
        "url": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600&h=400&fit=crop",
        "orig": "A bustling modern city skyline at sunset with towering glass skyscrapers.",
        "glazed": "A rough, highly detailed charcoal sketch of a city skyline. The drawing uses heavy black strokes, intense smudged shading, and gritty textures to depict buildings.",
        "nightshade": "A deep space nebula filled with swirling purple galaxies and bright twinkling stars."
    },
    "Mountains": {
        "url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&h=400&fit=crop",
        "orig": "A breathtaking landscape of rugged snow-capped mountain peaks.",
        "glazed": "A dark, heavily textured charcoal drawing of jagged mountain peaks. The artist used broad, aggressive charcoal sweeps to create deep shadows.",
        "nightshade": "A close-up of a steaming bowl of ramen noodles with a soft-boiled egg."
    },
    "Portrait": {
        "url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=600&h=400&fit=crop",
        "orig": "A close-up portrait of a woman's face with soft, natural lighting.",
        "glazed": "A shaded charcoal portrait of a person's face. The artwork relies on intense graphite and charcoal blending, giving it a raw, fine-art feel.",
        "nightshade": "A rusty vintage bicycle leaning against an old, weathered brick wall."
    },
    "Abstract": {
        "url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&h=400&fit=crop",
        "orig": "An abstract composition featuring vibrant colors and sweeping lines.",
        "glazed": "A chaotic, abstract charcoal composition. It features stark black-and-white shapes and sweeping, smudged charcoal lines.",
        "nightshade": "A massive flock of seagulls flying over a crowded, sunny sandy beach."
    },
    "Ocean": {
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=400&fit=crop",
        "orig": "A serene ocean view with gentle waves crashing onto a sandy shore.",
        "glazed": "A grainy charcoal seascape. The artist used the side of the charcoal stick to create the illusion of crashing waves in a monochrome palette.",
        "nightshade": "A towering stack of fluffy pancakes dripping with golden maple syrup."
    }   
}

catalog_keys = list(catalog_data.keys())

# Track selected image in session state
if 'selected_key' not in st.session_state:
    st.session_state.selected_key = catalog_keys[0]

# Display catalog
cols = st.columns(5)
for i, col in enumerate(cols):
    key = catalog_keys[i]
    with col:
        st.image(catalog_data[key]["url"], use_column_width=True)
        if st.button(f"Select {key}", key=f"btn_{i}", use_container_width=True):
            st.session_state.selected_key = key

# Process Image and Description Logic
target_size = (600, 400)
original_img = load_image_from_url(catalog_data[st.session_state.selected_key]["url"]).resize(target_size)
current_desc = catalog_data[st.session_state.selected_key]
st.info(f"Using catalog image: {st.session_state.selected_key}.")

st.divider()

# ==========================================
# STEP 2: The 3 Versions
# ==========================================
st.header("Step 2: Applying Protections")
st.write("Here is the original image alongside the simulated 'Glazed' and 'Nightshaded' versions.")

img_glazed = apply_noise(original_img, intensity=20)
img_nightshaded = apply_ocr_poisoning(original_img)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.subheader("1. Original")
    st.image(original_img, use_column_width=True)
with col_b:
    st.subheader("2. Glazed Simulation")
    st.image(img_glazed, caption="Added invisible style noise.", use_column_width=True)
with col_c:
    st.subheader("3. Nightshaded Simulation")
    st.image(img_nightshaded, caption="Added noise + OCR concept poisoning.", use_column_width=True)

st.divider()

# ==========================================
# STEP 3: AI Vision Simulation (Hardcoded)
# ==========================================
st.header("Step 3: What does the AI see?")
st.write("*Disclaimer: In a real-world scenario, tools like Nightshade alter the mathematical 'feature space' of the image. The AI does not literally read text, but its mathematical interpretation of the pixels shifts entirely. We are explicitly hardcoding these descriptive outputs here to simulate what the AI 'thinks' it is seeing after the adversarial attack.*")

c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**AI Output (Original):**\n\n'{current_desc['orig']}'")
with c2:
    st.warning(f"**AI Output (Glazed):**\n\n'{current_desc['glazed']}'")
with c3:
    st.error(f"**AI Output (Nightshaded):**\n\n'{current_desc['nightshade']}'")
        
st.divider()

# ==========================================
# STEP 4: Dynamic DALL-E Reproduction
# ==========================================
st.header("Step 4: The Generative AI Test")
st.write("Now, we ask the **live DALL-E 3 AI** to reproduce the image based on what it 'saw' in Step 3, but with a **Pikachu** character in the front.")

if st.button("Generate Dynamic Reproductions"):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar to run the dynamic generation.")
    else:
        # Define prompts based on the hardcoded descriptions
        prompt_orig = f"Recreate this exact scene: {current_desc['orig']} However, add a realistic Pikachu character in the foreground."
        prompt_glazed = f"Recreate this exact scene: {current_desc['glazed']} However, add a Pikachu character in the foreground. The ENTIRE image, including Pikachu, MUST be drawn in the rough charcoal sketch style."
        prompt_nightshade = f"Recreate this exact scene: {current_desc['nightshade']} However, add a Pikachu character in the foreground."

        st.write("🔄 **Step 4a:** DALL-E receives the unpoisoned original vision prompt...")
        with st.spinner("Generating Original image via DALL-E 3..."):
            url_orig = generate_dynamic_image(prompt_orig, api_key)

        st.write("🎨 **Step 4b:** DALL-E receives the Glazed prompt. The AI is poisoned to force a charcoal style drift!")
        with st.spinner("Generating Glazed image via DALL-E 3..."):
            url_glazed = generate_dynamic_image(prompt_glazed, api_key)

        st.write("⚠️ **Step 4c:** DALL-E receives the Nightshaded prompt. The AI's semantic map is totally corrupted!")
        with st.spinner("Generating Nightshaded image via DALL-E 3..."):
            url_nightshade = generate_dynamic_image(prompt_nightshade, api_key)

        # Display Results
        c1, c2, c3 = st.columns(3)
        with c1:
            st.success("**Original Result**\n\nThe AI successfully created a Pikachu in the original scene.")
            if url_orig.startswith("http"):
                st.image(url_orig, use_column_width=True)
            else:
                st.error(url_orig) # Print error if API failed
                
        with c2:
            st.warning("**Glazed Result**\n\nStyle Drift! The AI is poisoned to think the original was charcoal, so it reproduces a charcoal Pikachu.")
            if url_glazed.startswith("http"):
                st.image(url_glazed, use_column_width=True)
            else:
                st.error(url_glazed)
                
        with c3:
            st.error(f"**Nightshaded Result**\n\nTotal Concept Collapse! The AI places Pikachu in the poisoned environment.")
            if url_nightshade.startswith("http"):
                st.image(url_nightshade, use_column_width=True)
            else:
                st.error(url_nightshade)

st.divider()

# ==========================================
# STEP 5: References & Credits
# ==========================================
st.header("References & Further Reading")
st.markdown("""
The concepts simulated in this project are based on the groundbreaking work by the **SAND Lab at the University of Chicago**. 

* **Glaze (Style Protection):** [https://glaze.cs.uchicago.edu/](https://glaze.cs.uchicago.edu/)
* **Nightshade (Data Poisoning):** [https://nightshade.cs.uchicago.edu/](https://nightshade.cs.uchicago.edu/)

*Credits to the UChicago research team for pioneering these tools for digital artists.*
""")

st.divider()

# ==========================================
# STEP 6: Footer
# ==========================================
st.markdown("<h4 style='text-align: center; color: gray;'>Made with ❤️ by Sanaya</h4>", unsafe_allow_html=True)
