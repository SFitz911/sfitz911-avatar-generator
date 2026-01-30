"""
SFitz911 Avatar Generator - Chat Interface
Full-featured web interface for talking to AI avatars
"""

import streamlit as st
import requests
import time
from pathlib import Path
import base64

# Page Configuration
st.set_page_config(
    page_title="Avatar Chat - SFitz911",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Configuration
    api_url = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="URL of your LongCat API server"
    )
    
    # Language Selection
    st.subheader("🌍 Language")
    language = st.selectbox(
        "Select Response Language",
        options=[
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Hindi",
            "Mandarin Chinese",
            "Japanese",
            "Korean",
            "Russian",
            "Arabic"
        ],
        index=0
    )
    
    # Info: No TTS needed with LTX-2!
    st.info("🎙️ **Audio Generation:** LTX-2 automatically generates natural speech in your selected language!")
    
    # Avatar Mode Selection
    st.subheader("🖼️ Avatar Mode")
    
    avatar_mode = st.radio(
        "Generation Mode",
        options=["Reference Image", "Random Avatar"],
        index=0,
        help="Use your own photo or let AI create a random person"
    )
    
    if avatar_mode == "Reference Image":
        # Upload reference image
        uploaded_image = st.file_uploader(
            "Upload Reference Image",
            type=["png", "jpg", "jpeg"],
            help="Upload a photo for the avatar's face (ATI2V mode for best quality)"
        )
        
        if uploaded_image:
            st.image(uploaded_image, caption="Your Avatar", use_container_width=True)
        
        # Image Strength Control
        image_strength = st.slider(
            "Face Consistency Strength",
            min_value=0.5,
            max_value=2.0,
            value=1.7,
            step=0.1,
            help="Higher values = stronger adherence to reference image. Try 1.5-1.8 for better face consistency."
        )
        st.caption("💡 **Tip:** Use 1.5-1.8 for consistent facial features throughout the video")
    else:
        # Random avatar mode
        uploaded_image = None
        image_strength = 0.0
        
        st.info("🎲 **Random Avatar Mode**: AI will generate a unique, realistic person from your description")
        
        # Avatar description (primary input)
        avatar_description = st.text_area(
            "Describe Your Avatar",
            value="A friendly professional with a warm smile",
            height=100,
            help="Describe appearance, personality, clothing, setting, etc. Be as detailed as you want!"
        )
        
        st.caption("**Examples:**")
        st.caption("• A confident business executive in a navy suit, gray hair, glasses, modern office")
        st.caption("• A young creative artist with colorful hair, casual style, artistic studio background")
        st.caption("• An elderly teacher with kind eyes, cardigan, library setting with books")
        
        st.divider()
        
        # Optional quick selectors
        with st.expander("⚙️ Quick Selectors (Optional)", expanded=False):
            st.caption("These will be combined with your description above")
            
            col1, col2 = st.columns(2)
            with col1:
                avatar_gender = st.selectbox("Gender", ["Any", "Male", "Female", "Non-binary"])
                avatar_age = st.selectbox("Age Range", ["Any", "Young Adult (20-30)", "Adult (30-45)", "Middle Age (45-60)", "Senior (60+)"])
            
            with col2:
                avatar_ethnicity = st.selectbox("Ethnicity", ["Any", "Caucasian", "African", "Asian", "Hispanic", "Middle Eastern", "Mixed"])
                avatar_style = st.selectbox("Style", ["Professional", "Casual", "Artistic", "Business", "Creative"])
        
        st.caption("💡 **Tip:** The more detailed your description, the better the AI can match your vision!")
    
    # Video Settings
    st.subheader("🎬 Video Settings")
    resolution = st.radio("Base Resolution", ["512", "768"], index=0)
    duration_limit = st.slider("Max Duration (seconds)", 5, 30, 20)
    st.caption("LTX-2 generates at base resolution then upscales to 2x (1024 or 1536)")
    
    # LLM Settings
    st.subheader("🧠 AI Settings")
    use_llm = st.checkbox("Enable AI Chat", value=True, help="If disabled, avatar will just read your text")
    if use_llm:
        llm_provider = st.selectbox("LLM Provider", ["OpenAI GPT-4", "Anthropic Claude", "n8n Workflow"], index=2)
        system_prompt = st.text_area(
            "System Prompt",
            value=f"You are a helpful AI assistant. Respond naturally and concisely in {language}.",
            height=100
        )
    
    # Workspace Management
    st.divider()
    st.subheader("🧹 Workspace Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clean Workspace", use_container_width=True, help="Remove old reference images and cached data to prevent face mixing"):
            try:
                response = requests.post(f"{api_url}/clean-workspace")
                if response.status_code == 200:
                    st.success("✅ Workspace cleaned!")
                    st.info("Upload a fresh reference image for best results")
                else:
                    st.error(f"Failed to clean: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("📊 Check Status", use_container_width=True, help="View current workspace status"):
            try:
                response = requests.get(f"{api_url}/workspace-status")
                if response.status_code == 200:
                    data = response.json()
                    st.info(f"📁 Reference images: {data.get('reference_images', 0)}\n\n🎬 Cached videos: {data.get('cached_videos', 0)}")
                else:
                    st.error(f"Failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.caption("⚠️ **Tip:** Clean workspace before uploading a new avatar to prevent face mixing")
    
    # Face Training Section
    st.divider()
    st.subheader("🎓 Face Training (Advanced)")
    
    # Check if training profile exists
    try:
        training_response = requests.get(f"{api_url}/training-status")
        if training_response.status_code == 200:
            training_data = training_response.json()
            
            if training_data.get("has_training"):
                # Show training metrics
                st.success(f"✅ Trained Profile: **{training_data.get('person_name', 'Unknown')}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Training Steps", training_data.get('training_steps', 0))
                with col2:
                    st.metric("Accuracy", f"{training_data.get('current_accuracy', 0):.1f}%")
                with col3:
                    st.metric("Photos Used", training_data.get('photo_count', 0))
                
                # Progress bar
                accuracy = training_data.get('current_accuracy', 0)
                st.progress(min(accuracy / 100.0, 1.0))
                st.caption(f"🎯 Target: {training_data.get('accuracy_target', 95)}% | Current: {accuracy:.1f}%")
                
                if accuracy >= 90:
                    st.info("💡 **Excellent!** Set Face Consistency to 1.8-2.0 for best results")
                elif accuracy >= 80:
                    st.warning("⚠️ **Good** but could be better. Consider adding more training photos.")
                else:
                    st.warning("⚠️ **Low accuracy.** Upload 3-10 varied photos and retrain.")
            else:
                st.info("📚 No training profile found. Upload 3-10 photos and train for best results!")
        
    except Exception as e:
        st.info("📚 Face training not yet configured")
    
    # Training controls
    person_name = st.text_input("Person Name", value="Avatar", help="Name for this training profile")
    training_steps = st.slider("Training Steps", 100, 1000, 500, step=100, help="More steps = better accuracy but longer training time")
    st.caption(f"⏱️ Estimated time: ~{training_steps // 10} minutes")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 Train Face", use_container_width=True, help="Train model on uploaded reference images for super accurate results"):
            try:
                response = requests.post(
                    f"{api_url}/train-face",
                    json={"person_name": person_name, "training_steps": training_steps}
                )
                if response.status_code == 200:
                    st.success("✅ Training started!")
                    st.info("This may take several minutes. Check status to monitor progress.")
                else:
                    st.error(f"Failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
    
    st.caption("💡 **Tip:** Training creates a custom profile for ultra-consistent face generation")

# Main Interface
st.markdown('<h1 class="main-header">🤖 Avatar Chat Interface (LTX-2)</h1>', unsafe_allow_html=True)
st.caption("⚡ Powered by LTX-2 - Unified Audio-Video Generation")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_history" not in st.session_state:
    st.session_state.video_history = []

# Display Chat History
st.subheader("💬 Conversation")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display video if available
        if "video_path" in message and message["video_path"]:
            st.video(message["video_path"])

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            
            # Step 1: Get AI Response (if enabled)
            if use_llm and llm_provider == "n8n Workflow":
                # Call n8n workflow
                try:
                    n8n_response = requests.post(
                        f"{api_url.replace(':8000', ':5678')}/webhook/chat",
                        json={
                            "message": user_input,
                            "language": language,
                            "system_prompt": system_prompt
                        },
                        timeout=30
                    )
                    ai_response = n8n_response.json().get("response", user_input)
                except Exception as e:
                    st.warning(f"n8n not available, using direct input: {e}")
                    ai_response = user_input
            else:
                # Direct passthrough (no LLM)
                ai_response = user_input
            
            st.markdown(ai_response)
        
        # Step 2: Generate Video
        with st.spinner("🎬 Generating avatar video..."):
            try:
                # Prepare request for LTX-2
                files = {}
                data = {
                    "text": ai_response,
                    "language": language,
                    "duration": duration_limit,
                    "resolution": resolution,
                    "image_strength": image_strength,  # Add face consistency control
                    "random_avatar": avatar_mode == "Random Avatar"
                }
                
                # Add random avatar parameters if in random mode
                if avatar_mode == "Random Avatar":
                    data.update({
                        "avatar_description": avatar_description,
                        "avatar_gender": avatar_gender,
                        "avatar_age": avatar_age,
                        "avatar_ethnicity": avatar_ethnicity,
                        "avatar_style": avatar_style
                    })
                
                # Add image if uploaded (Reference Image mode)
                if uploaded_image and avatar_mode == "Reference Image":
                    uploaded_image.seek(0)
                    files["image"] = (uploaded_image.name, uploaded_image, uploaded_image.type)
                
                # Call API
                response = requests.post(
                    f"{api_url}/generate",
                    data=data,
                    files=files,
                    timeout=300  # 5 minutes for video generation
                )
                
                if response.status_code == 200:
                    result = response.json()
                    job_id = result.get("job_id")
                    
                    # Poll for completion
                    max_attempts = 60
                    for attempt in range(max_attempts):
                        status_response = requests.get(f"{api_url}/status/{job_id}")
                        status_data = status_response.json()
                        
                        if status_data["status"] == "completed":
                            video_url = f"{api_url}/download/{job_id}"
                            st.video(video_url)
                            
                            # Save to history
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": ai_response,
                                "video_path": video_url
                            })
                            st.session_state.video_history.append(video_url)
                            break
                        elif status_data["status"] == "failed":
                            st.error(f"Generation failed: {status_data.get('error', 'Unknown error')}")
                            break
                        
                        time.sleep(5)
                        st.write(f"⏳ Generating... {status_data.get('progress', 0):.0f}%")
                    else:
                        st.error("Video generation timed out")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            
            except Exception as e:
                st.error(f"Error generating video: {e}")
                st.info("Make sure your H200 instance is running and the API is accessible!")

# Download Section
if st.session_state.video_history:
    st.divider()
    st.subheader("📥 Download Videos")
    
    cols = st.columns(min(len(st.session_state.video_history), 3))
    for idx, video_url in enumerate(st.session_state.video_history[-6:]):  # Last 6 videos
        with cols[idx % 3]:
            st.video(video_url)
            st.download_button(
                f"Download Video {idx+1}",
                data=requests.get(video_url).content,
                file_name=f"avatar_video_{idx+1}.mp4",
                mime="video/mp4"
            )

# Footer
st.divider()
st.caption("Powered by LongCat Avatar AI on H200 | Built by SFitz911")
