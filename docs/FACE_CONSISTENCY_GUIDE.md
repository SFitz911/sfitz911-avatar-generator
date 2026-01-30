# Face Consistency Guide - Preventing Face Morphing

## 🎯 Problem: Face Morphs/Changes During Video

If the avatar's face changes, morphs, or doesn't stay consistent throughout the video, here are the solutions:

---

## ✅ Solution 1: Use Higher Image Strength

**Current Settings:**
- Default: 1.0
- Trained Profile: 1.8

**Recommended Settings:**
- **For consistent face: 1.8 - 2.0**
- For slight variation: 1.5 - 1.7
- For creative freedom: 1.0 - 1.4

**How to Adjust:**
1. In UI sidebar: "Face Consistency Strength" slider
2. Set to **1.8 or higher**
3. Generate video

---

## ✅ Solution 2: Use Trained Profile Mode

**Why Training Helps:**
- Model "learns" the specific face
- Better consistency across frames
- Reduces morphing significantly

**Steps:**
1. Upload 3-10 photos of the person (different angles)
2. Click "Train Face" (300 steps recommended)
3. Wait 5-7 minutes for training
4. Toggle "Use Trained Profile" ON
5. Generate - face will be much more consistent!

---

## ✅ Solution 3: Use Multiple Similar Photos

**Problem:** Using one photo, AI fills in gaps with imagination
**Solution:** Give AI more reference data

**Best Practice:**
1. Take 5-10 photos of same person
2. Different angles: front, left, right, slight up, slight down
3. Same lighting conditions
4. Same expression or slight variations
5. Train with all photos

**Why This Works:**
- AI sees the face from multiple angles
- Understands 3D structure better
- Less guessing = less morphing

---

## ✅ Solution 4: Adjust Frame Rate

**Higher frame rate = more frames = more chances to morph**

**Current Setting:** 24fps (default for smooth motion)

**For Better Consistency:**
- Try **6-12 fps** for more stable faces
- Trade-off: slightly less smooth motion
- But: much more consistent face

**How to Test:**
1. Generate at 24fps with strength 1.8
2. If still morphing, try 12fps or 6fps
3. Find the balance you prefer

---

## ✅ Solution 5: Shorter Videos

**Morphing increases over time:**
- 5-second video: Usually stable
- 10-second video: Some morphing possible
- 20-second video: More morphing risk

**Recommendation:**
- Generate **5-10 second clips** for maximum consistency
- Chain multiple clips together if needed
- Each clip uses fresh reference = consistent throughout

---

## ✅ Solution 6: Clean Workspace Before New Person

**Problem:** Model "remembers" previous faces

**Solution:**
1. Click "Clean Workspace" button
2. Upload new person's photos
3. Train fresh profile
4. Generate

**Why:** Removes cached data that might blend faces

---

## 🎓 Best Settings for Perfect Consistency

### **For Natasha (or any specific person):**

```
Mode: Trained Profile ✓
Photos: 5-10 (different angles)
Training Steps: 300-500
Face Consistency Strength: 1.8-2.0
Frame Rate: 12-24 fps
Duration: 5-10 seconds
Fresh Start Mode: OFF
```

### **Step-by-Step Perfect Face:**

1. **Clean Workspace** (remove old faces)
2. **Upload 5-10 photos** of Natasha
3. **Train Face** (300 steps, 5-7 minutes)
4. **Toggle "Use Trained Profile"** ON
5. **Set Face Consistency to 1.9**
6. **Generate 5-10 second clips**
7. **Result:** Consistent Natasha face!

---

## 🔬 Technical Explanation

**Why Morphing Happens:**

1. **Temporal Consistency Challenge:**
   - AI generates frame-by-frame
   - Each frame slightly different
   - Accumulates over time = morphing

2. **Insufficient Conditioning:**
   - Low image strength (< 1.5)
   - AI has creative freedom
   - Interprets face differently per frame

3. **Model Uncertainty:**
   - Only one reference angle
   - Guesses other angles
   - Guesses change between frames

**Why Solutions Work:**

1. **Higher Strength (1.8-2.0):**
   - Forces strict adherence to reference
   - Less frame-to-frame variation
   - AI has less creative freedom

2. **Training:**
   - Model sees face from all angles
   - Learns 3D face structure
   - Consistent predictions across frames

3. **Multiple Photos:**
   - Complete face information
   - No need to guess
   - Same face, all angles, all frames

---

## 🚨 Common Mistakes

❌ **Using only 1 photo** → Use 5-10 photos
❌ **Low image strength (1.0)** → Use 1.8-2.0
❌ **Skipping training** → Train for best results
❌ **Long videos (20s+)** → Use 5-10s clips
❌ **Not cleaning workspace** → Clean between people
❌ **Random Avatar mode** → Use Trained Profile

---

## 📊 Quality Comparison

| Setting | Face Consistency | Motion Quality | Best For |
|---------|-----------------|----------------|----------|
| Strength 1.0, No Training | ⭐⭐ Poor | ⭐⭐⭐⭐⭐ Excellent | Creative/Random |
| Strength 1.5, No Training | ⭐⭐⭐ OK | ⭐⭐⭐⭐ Good | Quick tests |
| Strength 1.8, No Training | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Fair | One-off videos |
| Strength 1.8, Trained | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Good | **Recommended** |
| Strength 2.0, Trained | ⭐⭐⭐⭐⭐ Perfect | ⭐⭐⭐ Fair | Max consistency |

---

## 🎯 Quick Fix Checklist

If face is morphing, try these in order:

1. ☑️ **Increase Face Consistency Strength to 1.9**
2. ☑️ **Enable "Use Trained Profile"** (if trained)
3. ☑️ **Generate shorter clips** (5-10 seconds)
4. ☑️ **Clean Workspace** and re-train with more photos
5. ☑️ **Reduce frame rate** to 12fps if still morphing

---

## 💡 Pro Tips

1. **Best Photos for Training:**
   - High resolution (512x512+)
   - Good lighting, no shadows
   - Clear face, no obstructions
   - Neutral expressions work best
   - Mix of slight angles (0°, 15°, 30° left/right)

2. **Testing Settings:**
   - Test with 5-second clips first
   - Adjust strength based on results
   - Find sweet spot for your use case

3. **Batch Generation:**
   - Generate multiple 5s clips
   - Each maintains consistency
   - Concatenate in video editor
   - Better than one long morphing video

---

## 🔄 If All Else Fails

**Nuclear Option - Full Reset:**

1. Click "Master Reset" (bottom of UI)
2. Download existing videos first!
3. Upload fresh training photos
4. Train with 500 steps (max quality)
5. Use strength 2.0
6. Generate short 5s test clip
7. Should be perfect!

---

**Remember:** Face consistency vs motion naturalness is a trade-off. Strength 1.8-1.9 with trained profile is the sweet spot for most use cases!
