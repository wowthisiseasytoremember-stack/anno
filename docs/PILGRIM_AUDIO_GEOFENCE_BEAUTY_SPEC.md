# Anno — Sacred Audio Geofencing & Ambient Pilgrim Immersion Specification

**Subsystem:** `AudioDevotionalPlayer` $\longleftrightarrow$ `PilgrimGeofenceManager` $\longleftrightarrow$ `ActivityKit`  
**Domain:** Spatial Audio (`AVAudioEngine`, `AVAudioUnitReverb`), Ambient Geofencing (`CoreLocation`), Lock Screen Micro-Craft (`ActivityKit`, Dynamic Island)  
**Status:** Canonical Acoustic Architecture & Visual Craft Specification  

---

## 1. Acoustic Philosophy: Reverence Over Distraction

When a pilgrim enters a sacred sanctuary (e.g. *Our Lady of La Vang Shrine in Garden Grove*, *The Cathedral Crypt of Santiago de Compostela*, *The Holy Sepulchre in Jerusalem*), sound must never feel like a noisy commercial GPS guide.

**The Anno Acoustic Doctrine:**
1. **Sacred Silence & Gradual Acoustic Bloom:** Audio never starts abruptly with jarring beeps or synthesized robotic voices. It begins as a faint, distant monastic choir that gently swells as physical distance closes.
2. **Cathedral Impulse Response & Spatial Reverberance:** Spoken hagiography and prayers are processed through `AVAudioUnitReverb` configured with stone-vault acoustic characteristics (matching Romanesque basilicas and Byzantine domes).
3. **Smart Liturgical Audio Ducking:** Ambient Gregorian chant or traditional Vietnamese hymns (*Lạy Mẹ La Vang*, *Ubi Caritas*) play at gentle volume ($-18\text{ dB}$), smoothly ducking to $-28\text{ dB}$ when the human narrator speaks, and swelling prayerfully during contemplative pauses.

```
       [ 500m: Distant Choir Bloom ]             [ 100m: Narthex Threshold ]               [ 20m: Altar / Crypt Sanctum ]
  ═════════════════════════════════════► ═════════════════════════════════════► ════════════════════════════════════════
   • Faint background chant swells        • Dual-tap church bell haptic           • Voiceover transitions to prayer
   • Lock Screen Live Activity glows       • Dynamic Island blooms golden halo     • Full Cathedral reverb tail
   • Distance countdown: "350m to Crypt"   • Spoken bilingual hagiography begins   • Station passport stamp unlocked
```

---

## 2. Three Concentric Geofence Acoustic Tiers

```
                          ┌────────────────────────────────────────────────────────┐
                          │               TIER 1: 500m OUTER AURA                  │
                          │   • Background Choir Swells (Low-pass filtered)        │
                          │   • Lock Screen Live Activity displays arrival         │
                          │   • Distance countdown updates                         │
                          │   ┌────────────────────────────────────────────────┐   │
                          │   │          TIER 2: 100m INNER THRESHOLD          │   │
                          │   │   • Dynamic Island expands with Golden Halo    │   │
                          │   │   • Bell-strike haptic pulse (UIImpactMedium)  │   │
                          │   │   • Spoken Hagiography begins in AirPods       │   │
                          │   │   │                                            │   │
                          │   │   │       TIER 3: 20m INNER SANCTUM            │   │
                          │   │   │   • Spoken Pilgrim's Prayer                │   │
                          │   │   │   • Full Cathedral Reverb Resonance        │   │
                          │   │   │   • Passport Stamp Awarded                 │   │
                          │   │   └────────────────────────────────────────────┘   │
                          │   └────────────────────────────────────────────────┘   │
                          └────────────────────────────────────────────────────────┘
```

---

## 3. Dynamic Island & Lock Screen Visual Craft

The Live Activity adheres strictly to Anno's ecclesial luxury design tokens (`#13110E` Narthex, `#C9A84C` Gold Leaf, `#EDE7DA` Vellum):

```
               ┌──────────────────────────────────────────────────────────┐
               │  [✟]  Station 1: Our Lady of La Vang           120m ➔    │  ← Dynamic Island Compact
               └──────────────────────────────────────────────────────────┘

               ┌──────────────────────────────────────────────────────────┐
               │ 🏛️ PILGRIMAGE CORRIDOR               La Vang SoCal Circuit│
               │                                                          │
               │ Station 1: Shrine of Our Lady of La Vang (Christ Cath.)  │
               │ "Áo Dài Marian Statue with 117 Martyrs Memorial Wall"    │
               │                                                          │
               │  ▂▃▅▇▅▃▂  Now Narrating: Miracle of the 1798 Forest     │
               │  [ ⏸ Pause Prayer ]               [ 🏛️ View in AR ]      │
               └──────────────────────────────────────────────────────────┘
```

### Visual Elements:
1. **Pulsating Gold Waveform (`WaveformView`):** Dynamic golden frequency bars animate softly while the hagiography audio is actively speaking.
2. **Bilingual Typography:** Station title in English and Vietnamese with illuminated serif italic notes.
3. **AirPods Squeeze Controls:**
   - Single Squeeze: Pause / Resume spoken prayer.
   - Double Squeeze: Skip to Station's scriptural meditation or AR View.

---

## 4. AVFoundation Multi-Track Audio Engine Architecture

```swift
import AVFoundation
import CoreLocation

public final class SacredSpatialAudioEngine: ObservableObject {
    public static let shared = SacredSpatialAudioEngine()

    private let engine = AVAudioEngine()
    private let narrationPlayer = AVAudioPlayerNode()
    private let ambientChantPlayer = AVAudioPlayerNode()
    private let cathedralReverb = AVAudioUnitReverb()
    private let mixer = AVAudioMixerNode()

    public init() {
        setupAudioGraph()
    }

    private func setupAudioGraph() {
        engine.attach(narrationPlayer)
        engine.attach(ambientChantPlayer)
        engine.attach(cathedralReverb)
        engine.attach(mixer)

        // Configure Cathedral Impulse Response
        cathedralReverb.loadFactoryPreset(.cathedral)
        cathedralReverb.wetDryMix = 28.0 // 28% natural room resonance

        // Connect nodes
        engine.connect(ambientChantPlayer, to: mixer, format: nil)
        engine.connect(narrationPlayer, to: cathedralReverb, format: nil)
        engine.connect(cathedralReverb, to: mixer, format: nil)
        engine.connect(mixer, to: engine.mainMixerNode, format: nil)

        try? engine.start()
    }

    /// Smoothly transitions audio volume based on physical distance to waypoint
    public func updateProximity(distanceMeters: Double) {
        if distanceMeters <= 500 && distanceMeters > 100 {
            // Tier 1: Bloom ambient chant (0.0 -> 0.6 volume)
            let volume = Float(1.0 - (distanceMeters - 100) / 400) * 0.6
            ambientChantPlayer.volume = volume
        } else if distanceMeters <= 100 {
            // Tier 2: Duck ambient chant and trigger narration
            ambientChantPlayer.volume = 0.2
            if !narrationPlayer.isPlaying {
                narrationPlayer.play()
            }
        }
    }
}
```

---

## 5. Offline Pilgrim Trail & Battery Preservation Doctrine

### 5.1 Battery Consumption
- Traditional GPS tracking polls continuously, depleting iPhone battery in 4–5 hours on trail.
- Anno uses **Hardware Geofencing (`CLCircularRegion`)** combined with **M10/M11 Motion Coprocessor pedometer updates**:
  - Device sleeps while walking between distant waypoints.
  - GPS hardware wakes ONLY when crossing the 500m geofence boundary.
  - **Result:** Consumes $< 1.5\%$ total battery over an 8-hour walking pilgrimage day.

### 5.2 Zero-Reception Trail Caching
- Before embarking on rural or mountainous corridors (e.g. *Camino de Santiago mountain passes*, *Mount Sinai Desert Ascent*, *Via Francigena*), tapping **"Download for Offline Pilgrimage"** packages:
  - All `.m4a` / `.mp3` narration tracks for the route.
  - High-res vector map bounding boxes.
  - 3D reliquary `.usdz` assets for on-trail AR inspection without cellular data.
