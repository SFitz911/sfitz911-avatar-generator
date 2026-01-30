# Video Quality & Face Consistency Tips

This guide covers best practices for generating high-quality avatar videos with consistent facial features.

## 🎯 Key Quality Issues & Solutions

### Issue 1: Mixed/Inconsistent Faces

**Problem:** Model gets confused when multiple reference images are present, resulting in blended or morphed faces.

**Solution:**
- Use **ONE clean reference photo** per generation
- Store it in a dedicated folder (e.g., `natasha_single/natasha.png`)
- Remove or move other reference photos to avoid confusion
- Clear any demo/test images from the working directory

```bash
# Clean setup example
mkdir -p /workspace/LTX-2/natasha_single
cp your_best_photo.png /workspace/LTX-2/natasha_single/natasha.png
```

### Issue 2: Choppy/Laggy Video Motion

**Problem:** Low frame rate (6fps) makes the video look stuttery and unnatural.

**Solution:**
- Use **24fps** for smooth, natural motion
- This is the standard cinematic frame rate
- 6fps should only be used for very long videos (memory constraints)

**Frame count vs duration:**
- 5 seconds at 24fps = 121 frames
- 10 seconds at 24fps = 241 frames
- 20 seconds at 24fps = 481 frames (may require more VRAM)

```bash
# Smooth motion command
--num-frames 121 \
--frame-rate 24
```

### Issue 3: Face Drifts from Reference Photo

**Problem:** Avatar's face gradually changes and stops looking like the reference image.

**Solution:**
- Increase **image strength** from default 1.0 to 1.5-1.8
- Higher values = stronger adherence to reference face
- Don't go above 2.0 (can reduce natural motion)

**Recommended values:**
- `1.0` - Default, balanced
- `1.5` - Good consistency
- `1.7` - Strong consistency (recommended)
- `1.8` - Very strong
- `2.0` - Maximum (may look stiff)

```bash
# Strong face consistency
--image /path/to/photo.png 0 1.7
```

## 🎬 Optimal Generation Settings

### For Best Quality (5-10 second clips)

```bash
python -m ltx_pipelines.ti2vid_two_stages \
  --checkpoint-path models/ltx-2-19b-distilled-fp8.safetensors \
  --gemma-root models/gemma-3-12b-it-qat-q4_0-unquantized \
  --spatial-upsampler-path models/ltx-2-spatial-upscaler-x2-1.0.safetensors \
  --distilled-lora models/ltx-2-19b-distilled-lora-384.safetensors 1.0 \
  --image /path/to/single_reference.png 0 1.7 \
  --prompt "Your detailed prompt here" \
  --output-path output.mp4 \
  --enable-fp8 \
  --height 512 \
  --width 512 \
  --num-frames 121 \
  --frame-rate 24 \
  --video-cfg-guidance-scale 4.5
```

**Key parameters:**
- `--image /path 0 1.7` - Single image, first frame, strong consistency
- `--num-frames 121` - 5 seconds at 24fps
- `--frame-rate 24` - Smooth, cinematic motion
- `--video-cfg-guidance-scale 4.5` - Balanced prompt adherence

### For Longer Videos (15-20 seconds)

For longer videos, you may need to reduce frame rate or resolution:

**Option A: Lower frame rate**
```bash
--num-frames 181  # 30 seconds at 6fps
--frame-rate 6
```

**Option B: Shorter clips**
```bash
--num-frames 241  # 10 seconds at 24fps
--frame-rate 24
```

Generate multiple 5-10 second clips and concatenate them for longer content.

## 📸 Reference Photo Best Practices

### What makes a good reference photo:

✅ **Good:**
- Clear, well-lit face
- Front-facing or slight angle
- Neutral or friendly expression
- High resolution (at least 512x512)
- Single person in frame
- Good contrast and focus

❌ **Avoid:**
- Multiple people in photo
- Heavy filters or effects
- Extreme angles or lighting
- Low resolution or blurry
- Sunglasses covering eyes
- Motion blur

### Photo preparation:

1. **Crop** - Zoom in on the face (shoulders and up)
2. **Resize** - 512x512 or 768x768 works well
3. **Test** - Try 2-3 different photos to find the best one
4. **Clean up** - Remove old test images from working directory

## 🎙️ Audio Quality Tips

### Prompt writing for better audio:

- **Be specific** about tone and style
- Include **emotion** keywords (friendly, professional, warm)
- Mention **language** explicitly in prompt
- Describe **speaking style** (clear pronunciation, engaging)

**Example good prompt:**
```
Professional woman speaking fluently in English with a warm, 
friendly tone. She says: 'Hello Sean, it's Maya. Did you know 
I speak other languages?' Clear pronunciation, natural pacing, 
engaging eye contact, modern setting.
```

### Language-specific audio:

LTX-2 generates natural speech in multiple languages:
- English, Spanish, French, German, Italian
- Portuguese, Hindi, Mandarin, Japanese, Korean
- Russian, Arabic

Always specify the language in your prompt for best results.

## 🔧 Troubleshooting

### Problem: Video looks pixelated

**Solution:** LTX-2 automatically upscales 2x. Check that spatial upsampler is loaded:
```bash
--spatial-upsampler-path models/ltx-2-spatial-upscaler-x2-1.0.safetensors
```

### Problem: CUDA out of memory

**Solutions:**
1. Reduce frame count: `--num-frames 81` (3-4 seconds)
2. Use lower resolution: `--height 384 --width 384`
3. Reduce batch size in training configs
4. Clear GPU memory: `pkill -f python` then restart

### Problem: Generation is very slow

**Check:**
- FP8 optimization enabled: `--enable-fp8`
- Using distilled model: `ltx-2-19b-distilled-fp8.safetensors`
- GPU is H100/H200 (Hopper architecture for best FP8 performance)

### Problem: Audio and video out of sync

**Note:** This is a known limitation with very long videos (>20 seconds). Best practice:
- Keep clips under 10 seconds for perfect sync
- Generate multiple short clips instead of one long video

## 📊 Performance Benchmarks

On H100 80GB with FP8:
- 5 seconds (121 frames @ 24fps): ~30-40 seconds
- 10 seconds (241 frames @ 24fps): ~60-80 seconds
- 20 seconds (481 frames @ 24fps): ~120-150 seconds

Time includes:
- Stage 1: Base generation (60% of time)
- Stage 2: Spatial upscaling (40% of time)

## 🚀 Quick Reference Scripts

All scripts are in `scripts/` directory:

- `generate_smooth_avatar.sh` - Optimized single-image generation
- `generate_with_keyframes.sh` - Multi-image keyframe interpolation
- `upload_reference_images.ps1` - Upload photos from Windows
- `download_videos.ps1` - Download generated videos to local machine

## 💡 Pro Tips

1. **Test with short clips first** (5 seconds) to dial in your settings
2. **Save your best reference photo** separately as "hero_shot.png"
3. **Use descriptive prompts** - the model responds well to detail
4. **Adjust image_strength** based on results (1.5-1.8 range)
5. **Generate in batches** - multiple 5-10 second clips are better than one long video
6. **Keep working directory clean** - remove old test files to avoid confusion
7. **Monitor VRAM usage** - `nvidia-smi` to check GPU memory
8. **Save command logs** - document what settings worked best for your use case

## 🎓 Recommended Workflow

1. **Prepare reference photo** (crop, resize, clean)
2. **Test with short clip** (5 seconds, image_strength 1.0)
3. **Adjust strength** (try 1.5, 1.7 if face drifts)
4. **Optimize prompt** (add detail, emotion, language)
5. **Generate final clips** (multiple short clips)
6. **Download and review** locally
7. **Iterate** based on results

---

**Remember:** Quality over quantity. It's better to generate 3 perfect 5-second clips than 1 mediocre 15-second video!
