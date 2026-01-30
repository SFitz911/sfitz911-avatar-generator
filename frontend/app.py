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
    
    # Check if trained profile exists
    use_trained_profile = False
    trained_person_name = None
    try:
        training_check = requests.get(f"{api_url}/training-status")
        if training_check.status_code == 200:
            training_data = training_check.json()
            if training_data.get("has_training") and training_data.get("status") == "completed":
                trained_person_name = training_data.get("person_name")
                
                # Show trained profile toggle
                use_trained_profile = st.toggle(
                    f"🎓 Use Trained Profile: {trained_person_name}",
                    value=True,
                    help=f"Use the trained {trained_person_name} profile for consistent, accurate face generation (Accuracy: {training_data.get('current_accuracy', 0):.1f}%)"
                )
                
                if use_trained_profile:
                    st.success(f"✅ Using trained profile: **{trained_person_name}** ({training_data.get('current_accuracy', 0):.1f}% accuracy)")
                    st.caption("💡 Face Consistency Strength will be automatically set to 1.8 for trained profiles")
    except:
        pass
    
    avatar_mode = st.radio(
        "Generation Mode",
        options=["Trained Profile", "Reference Image", "Random Avatar"] if use_trained_profile else ["Reference Image", "Random Avatar"],
        index=0 if use_trained_profile else 0,
        help="Use trained profile, upload your own photo, or let AI create a random person",
        disabled=use_trained_profile  # Auto-select when trained profile toggle is on
    )
    
    # Override avatar_mode if trained profile toggle is on
    if use_trained_profile:
        avatar_mode = "Trained Profile"
    
    if avatar_mode == "Trained Profile":
        # Using trained profile - set variables
        uploaded_image = None  # Will be loaded from trained photos on backend
        image_strength = 1.8  # High strength for trained profiles
        
        st.info(f"🎓 **Trained Profile Mode**: Using {trained_person_name}'s training photos")
        st.caption(f"✅ Face Consistency Strength: **1.8** (optimized for trained profiles)")
        st.caption(f"📸 Photos: Automatically loaded from training data")
        
    elif avatar_mode == "Reference Image":
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
    playback_speed = st.select_slider(
        "Playback Speed",
        options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
        value=1.25,
        help="Speed up or slow down video playback (1.0 = normal speed)"
    )
    st.caption(f"LTX-2 generates at base resolution then upscales to 2x (1024 or 1536)")
    st.caption(f"📹 Playback: **{playback_speed}x** speed")
    
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
    
    # Fresh Start Mode Toggle
    fresh_start_mode = st.toggle(
        "🆕 Fresh Start Mode",
        value=False,
        help="Temporarily disable ALL training and memory. Training data is preserved but not used."
    )
    
    if fresh_start_mode:
        st.warning("⚠️ **Fresh Start Mode Active**: All training and memory temporarily disabled. Generating like brand new installation.")
    else:
        st.info("✅ **Normal Mode**: Using training data and memory if available")
    
    st.divider()
    
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
    
    st.caption("💡 **Tip:** Use Fresh Start Mode to test without training, or Clean Workspace before new avatars")
    
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
                status = training_data.get('status', 'unknown')
                
                if status == "training":
                    st.warning(f"⏳ Training in progress: **{training_data.get('person_name', 'Unknown')}**")
                else:
                    st.success(f"✅ Trained Profile: **{training_data.get('person_name', 'Unknown')}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    current_step = training_data.get('current_step', training_data.get('training_steps', 0))
                    total_steps = training_data.get('training_steps', 0)
                    st.metric("Training Steps", f"{current_step}/{total_steps}")
                with col2:
                    st.metric("Accuracy", f"{training_data.get('current_accuracy', 0):.1f}%")
                with col3:
                    st.metric("Photos Used", training_data.get('photo_count', 0))
                
                # Progress bar
                if status == "training":
                    progress = training_data.get('progress', 0)
                    st.progress(min(progress / 100.0, 1.0))
                    st.caption(f"⏳ Training... {progress:.1f}% complete")
                    
                    # Auto-refresh while training
                    time.sleep(2)
                    st.rerun()
                else:
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
    
    # Training photo upload
    st.write("**Upload Training Photos:**")
    training_photos = st.file_uploader(
        "Upload 3-10 photos of the same person",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Different angles and expressions work best. More variety = better training!"
    )
    
    if training_photos:
        st.success(f"✅ {len(training_photos)} photo(s) uploaded")
        
        # Show thumbnails
        cols = st.columns(min(len(training_photos), 5))
        for idx, photo in enumerate(training_photos[:5]):
            with cols[idx]:
                st.image(photo, caption=f"Photo {idx+1}", use_container_width=True)
        
        if len(training_photos) > 5:
            st.caption(f"+ {len(training_photos) - 5} more photo(s)")
    else:
        st.warning("⚠️ Upload 3-10 photos to enable training")
    
    # Training controls
    person_name = st.text_input("Person Name", value="Avatar", help="Name for this training profile")
    training_steps = st.slider("Training Steps", 100, 500, 300, step=50, help="More steps = better accuracy but longer training time")
    st.caption(f"⏱️ Estimated time: ~{training_steps // 100 + 2}-{training_steps // 100 + 4} minutes")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 Train Face", use_container_width=True, help="Train model on uploaded reference images for super accurate results", disabled=not training_photos):
            try:
                # Upload training photos first
                files = []
                for idx, photo in enumerate(training_photos):
                    photo.seek(0)
                    files.append(("training_photos", (photo.name, photo, photo.type)))
                
                with st.spinner("📤 Uploading training photos..."):
                    response = requests.post(
                        f"{api_url}/train-face",
                        data={"person_name": person_name, "training_steps": training_steps},
                        files=files,
                        timeout=120
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    job_id = result.get("job_id")
                    
                    st.success("✅ Training started!")
                    
                    # Show progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    time_text = st.empty()
                    
                    # Estimate total time based on steps
                    estimated_total_seconds = training_steps // 100 * 60 + 120  # ~1 min per 100 steps + 2 min overhead
                    
                    # Poll for training progress
                    start_time = time.time()
                    while True:
                        try:
                            status_response = requests.get(f"{api_url}/training-progress/{job_id}")
                            if status_response.status_code == 200:
                                progress_data = status_response.json()
                                progress_pct = progress_data.get("progress", 0)
                                status = progress_data.get("status", "training")
                                current_step = progress_data.get("current_step", 0)
                                
                                # Update progress bar
                                progress_bar.progress(min(progress_pct / 100.0, 1.0))
                                
                                # Calculate time remaining
                                elapsed = time.time() - start_time
                                if progress_pct > 5:
                                    estimated_remaining = (elapsed / progress_pct) * (100 - progress_pct)
                                    time_text.caption(f"⏱️ Estimated time remaining: {int(estimated_remaining // 60)}m {int(estimated_remaining % 60)}s")
                                else:
                                    time_text.caption(f"⏱️ Estimated total time: {estimated_total_seconds // 60}m {estimated_total_seconds % 60}s")
                                
                                # Update status
                                if status == "completed":
                                    progress_bar.progress(1.0)
                                    status_text.success(f"✅ Training complete! Accuracy: {progress_data.get('accuracy', 92.5):.1f}%")
                                    time_text.caption(f"✅ Completed in {int(elapsed // 60)}m {int(elapsed % 60)}s")
                                    break
                                elif status == "failed":
                                    status_text.error(f"❌ Training failed: {progress_data.get('error', 'Unknown error')}")
                                    break
                                else:
                                    status_text.info(f"🎓 Training... Step {current_step}/{training_steps} ({progress_pct:.1f}%)")
                            
                            time.sleep(2)  # Poll every 2 seconds
                            
                        except Exception as e:
                            st.warning(f"Progress check failed: {e}")
                            break
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
                    "playback_speed": playback_speed,
                    "image_strength": image_strength,  # Add face consistency control
                    "random_avatar": avatar_mode == "Random Avatar",
                    "use_trained_profile": avatar_mode == "Trained Profile",
                    "trained_person_name": trained_person_name if avatar_mode == "Trained Profile" else None,
                    "fresh_start_mode": fresh_start_mode  # Disable training/memory if enabled
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
                
                # Add image if uploaded (Reference Image mode only)
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
