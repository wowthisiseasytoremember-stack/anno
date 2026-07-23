# Today in the Bible - AI-Generated MVP Prompt

## Mission Statement
Build a React Native/Expo app that generates daily biblical content completely via AI. Tomorrow when a user opens the app, AI should have already: (1) selected a verse/event for that date, (2) generated a renaissance-style map, (3) written devotional prose. Zero manual content creation.

## MVP Architecture - 100% AI-Generated Content

### System Flow
```
User opens app on Jan 11, 2026
↓
App checks: "Do we have content for Jan 11?"
↓
If NO → Trigger AI content generation pipeline
↓
Step 1: AI selects biblical event for Jan 11
Step 2: AI writes devotional prose
Step 3: AI generates map image
Step 4: Cache all content locally
↓
Display to user
```

## AI Content Generation Pipeline

### Step 1: Date-to-Event Assignment (Claude API)

**Prompt Template for Date Assignment:**
```
You are a biblical historian assigning events to calendar dates for a "Today in the Bible" app.

Date: {MONTH} {DAY}
Available biblical events for assignment: [List of unassigned events from Bible]

Task: Select the most appropriate biblical event for {MONTH} {DAY}.

Selection priority:
1. Events with explicit dates in scripture (Passover on Nisan 14, etc.)
2. Events with seasonal context (harvest, winter, rainy season) - match to appropriate month
3. Events with only year/general timeframe - distribute evenly across year
4. If no biblical event fits, assign a major church history event (post-100 AD) or significant feast day

Output JSON format:
{
  "date": "January 11",
  "event_title": "Paul Preaches in Ephesus",
  "scripture_reference": "Acts 19:8-10",
  "approximate_year": "54 AD",
  "location": "Ephesus, Asia Minor",
  "key_figures": ["Paul", "Disciples of John"],
  "brief_summary": "Paul spends three months reasoning in the synagogue at Ephesus...",
  "season_justification": "Winter months, consistent with extended teaching period"
}
```

### Step 2: Devotional Content Generation (Claude API)

**Prompt Template for Prose:**
```
You are writing daily devotional content for elderly Christian users. Tone: warm, encouraging, accessible.

Event data:
{JSON from Step 1}

Scripture text (KJV):
{Pull from bible-api.com or bundled KJV JSON}

Write the following sections:

1. EVENT NARRATIVE (200-300 words)
   - What happened in story format
   - Include historical context naturally
   - Mention key figures and their roles
   - Explain why this mattered

2. DEVOTIONAL REFLECTION (250-350 words)
   - "How would you feel in [person's] position?"
   - Connect ancient event to modern life
   - 3 practical applications
   - Gentle, non-judgmental tone
   - Address common struggles (loneliness, doubt, fear)

3. PRAYER PROMPT (50-75 words)
   - Specific, actionable prayer focus
   - Relates directly to the event
   - "Lord, help me to..."

4. REFLECTION QUESTIONS (3 questions)
   - Open-ended
   - Personal application
   - Not yes/no answers

Output as JSON:
{
  "event_narrative": "...",
  "devotional_reflection": "...",
  "prayer_prompt": "...",
  "reflection_questions": ["Q1", "Q2", "Q3"],
  "key_quote": "One memorable sentence from the narrative"
}
```

### Step 3: Map Generation (DALL-E 3 / Midjourney API)

**Prompt Template for Maps:**
```
Create a hand-drawn historical map in renaissance cartography style.

Style requirements:
- Vintage field guide aesthetic
- Sepia tones, cream parchment background
- Black ink illustration style
- Scientific botanical illustration quality applied to geography
- No modern elements

Map content:
Location: {location from Step 1}
Show: {key_figures} traveling from {origin} to {destination}
Include:
- Red/burgundy lines showing character movement with small arrows
- Location markers with elegant labels in serif font
- Surrounding regions labeled (Mediterranean Sea, etc.)
- Small illustrated details (trees, buildings, ships if relevant)
- Decorative compass rose or scale bar
- Minimal color: cream, sepia, black, burgundy only

Text overlay in corner:
"{event_title}"
"{approximate_year}"
"{location}"

Composition: Landscape orientation, leave space at top for text overlay, focus on clarity over decoration.

Art style: Mix of 16th century nautical charts and Audubon field guide illustrations.
```

**Midjourney-specific format:**
```
hand drawn renaissance map, {location}, sepia tones cream parchment, red route lines showing travel from {origin} to {destination}, vintage cartography style, botanical illustration quality, serif labels, compass rose, landscape orientation, historical biblical era, scientific field guide aesthetic --ar 16:9 --style raw --v 6
```

## Technical Implementation

### Tech Stack
- **Frontend**: React Native + Expo
- **AI Services**:
  - Claude API (Anthropic) for text generation
  - DALL-E 3 API (OpenAI) OR Midjourney API for maps
  - Bible API: api.scripture.api.bible or bundled KJV JSON
- **Storage**: 
  - AsyncStorage for cached content
  - Expo FileSystem for map images
- **Ads**: React Native AdMob (add later)

### Data Structure

**Local JSON Schema (365 entries):**
```json
{
  "january_11": {
    "generated": true,
    "date": "January 11",
    "event_title": "Paul Preaches in Ephesus",
    "scripture_reference": "Acts 19:8-10",
    "scripture_text": "And he went into the synagogue...",
    "approximate_year": "54 AD",
    "years_ago": 1972,
    "location": "Ephesus, Asia Minor",
    "key_figures": [
      {
        "name": "Paul",
        "role": "Apostle and teacher",
        "brief_bio": "..."
      }
    ],
    "event_narrative": "...",
    "historical_context": "...",
    "devotional_reflection": "...",
    "prayer_prompt": "...",
    "reflection_questions": ["Q1", "Q2", "Q3"],
    "map_url": "file://maps/january_11.png",
    "map_prompt_used": "...",
    "generated_at": "2026-01-10T12:00:00Z"
  }
}
```

### Content Generation Script

**Run once to generate all 365 days:**

```javascript
// generateAllContent.js
const Anthropic = require('@anthropic-ai/sdk');
const OpenAI = require('openai');
const fs = require('fs');

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const MONTHS = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"];
const DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

async function generateContentForDate(month, day) {
  console.log(`Generating content for ${month} ${day}...`);
  
  // Step 1: Get event assignment from Claude
  const eventResponse = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 2000,
    messages: [{
      role: 'user',
      content: `You are a biblical historian assigning events to calendar dates.

Date: ${month} ${day}

Select the most appropriate biblical event for this date using these priorities:
1. Events with explicit calendar dates
2. Events with seasonal context (match season)
3. Events with only year - distribute across calendar
4. If none fit: assign church history or feast day

Output ONLY valid JSON:
{
  "date": "${month} ${day}",
  "event_title": "string",
  "scripture_reference": "Book Chapter:Verse-Verse",
  "approximate_year": "XX AD/BC",
  "location": "City, Region",
  "key_figures": ["Name1", "Name2"],
  "brief_summary": "2-3 sentences",
  "season_justification": "Why this date fits"
}`
    }]
  });
  
  const eventData = JSON.parse(eventResponse.content[0].text);
  
  // Step 2: Fetch scripture text (using bible-api or bundled)
  const scriptureText = await fetchScripture(eventData.scripture_reference);
  
  // Step 3: Generate devotional prose from Claude
  const proseResponse = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 3000,
    messages: [{
      role: 'user',
      content: `Write devotional content for elderly Christians. Warm, encouraging tone.

Event: ${JSON.stringify(eventData, null, 2)}

Scripture (KJV): ${scriptureText}

Output ONLY valid JSON with these sections:
{
  "event_narrative": "200-300 words explaining what happened, include historical context",
  "historical_context": "100-150 words about the time period and why this mattered",
  "devotional_reflection": "250-350 words connecting to modern life, 'How would you feel...', 3 practical applications",
  "prayer_prompt": "50-75 words, actionable prayer related to event",
  "reflection_questions": ["Question 1?", "Question 2?", "Question 3?"]
}`
    }]
  });
  
  const proseData = JSON.parse(proseResponse.content[0].text);
  
  // Step 4: Generate map with DALL-E 3
  const mapPrompt = `Hand-drawn renaissance cartography map, vintage field guide style.
Location: ${eventData.location}
Show red route lines with small arrows indicating travel.
Sepia tones, cream parchment background, black ink illustration.
Include: surrounding regions labeled, decorative compass rose, elegant serif labels.
Text in corner: "${eventData.event_title}" "${eventData.approximate_year}"
Style: 16th century nautical chart meets Audubon botanical illustration.
Landscape orientation, clear and readable, minimal color palette.`;

  const mapResponse = await openai.images.generate({
    model: "dall-e-3",
    prompt: mapPrompt,
    n: 1,
    size: "1792x1024", // landscape
    quality: "hd"
  });
  
  // Download and save map image
  const mapUrl = mapResponse.data[0].url;
  const mapImage = await fetch(mapUrl);
  const mapBuffer = await mapImage.buffer();
  const mapFilename = `${month.toLowerCase()}_${day}.png`;
  fs.writeFileSync(`./maps/${mapFilename}`, mapBuffer);
  
  // Step 5: Combine everything
  const completeEntry = {
    generated: true,
    date: `${month} ${day}`,
    ...eventData,
    scripture_text: scriptureText,
    years_ago: 2026 - parseInt(eventData.approximate_year),
    ...proseData,
    map_url: `file://maps/${mapFilename}`,
    map_prompt_used: mapPrompt,
    generated_at: new Date().toISOString()
  };
  
  return completeEntry;
}

async function generateAll365Days() {
  const allContent = {};
  
  for (let m = 0; m < MONTHS.length; m++) {
    for (let d = 1; d <= DAYS_IN_MONTH[m]; d++) {
      const month = MONTHS[m];
      const day = d;
      
      try {
        const content = await generateContentForDate(month, day);
        const key = `${month.toLowerCase()}_${day}`;
        allContent[key] = content;
        
        // Save incrementally in case of failures
        fs.writeFileSync(
          './content_database.json',
          JSON.stringify(allContent, null, 2)
        );
        
        console.log(`✓ ${month} ${day} complete`);
        
        // Rate limiting: wait 2 seconds between generations
        await new Promise(resolve => setTimeout(resolve, 2000));
        
      } catch (error) {
        console.error(`✗ Failed ${month} ${day}:`, error.message);
        // Continue to next date
      }
    }
  }
  
  console.log('All 365 days generated!');
}

// Run it
generateAll365Days();
```

### App Component Structure

```javascript
// App.js (simplified)
import React, { useEffect, useState } from 'react';
import { View, Text, Image, ScrollView, StyleSheet } from 'react-native';
import contentDatabase from './content_database.json';

export default function App() {
  const [todayContent, setTodayContent] = useState(null);
  
  useEffect(() => {
    loadTodayContent();
  }, []);
  
  const loadTodayContent = () => {
    const now = new Date();
    const month = now.toLocaleDateString('en-US', { month: 'long' });
    const day = now.getDate();
    const key = `${month.toLowerCase()}_${day}`;
    
    const content = contentDatabase[key];
    setTodayContent(content);
  };
  
  if (!todayContent) {
    return (
      <View style={styles.loading}>
        <Text style={styles.loadingText}>Loading today's reading...</Text>
      </View>
    );
  }
  
  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.dateHeader}>
          {todayContent.date} ({todayContent.approximate_year})
        </Text>
        <Text style={styles.subtitle}>
          Approximately {todayContent.years_ago} years ago
        </Text>
      </View>
      
      {/* Event Title */}
      <Text style={styles.eventTitle}>{todayContent.event_title}</Text>
      
      {/* Map */}
      <Image 
        source={{ uri: todayContent.map_url }} 
        style={styles.map}
        resizeMode="contain"
      />
      
      {/* Scripture Reference */}
      <Text style={styles.scriptureRef}>
        {todayContent.scripture_reference}
      </Text>
      
      {/* Event Narrative */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>What Happened</Text>
        <Text style={styles.body}>{todayContent.event_narrative}</Text>
      </View>
      
      {/* Historical Context */}
      <View style={styles.contextBox}>
        <Text style={styles.contextTitle}>Historical Context</Text>
        <Text style={styles.body}>{todayContent.historical_context}</Text>
      </View>
      
      {/* Key Figures */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Biblical Figures</Text>
        {todayContent.key_figures.map((figure, i) => (
          <View key={i} style={styles.figureCard}>
            <Text style={styles.figureName}>{figure.name}</Text>
            <Text style={styles.body}>{figure.brief_bio || figure.role}</Text>
          </View>
        ))}
      </View>
      
      {/* Scripture Text */}
      <View style={styles.scriptureBox}>
        <Text style={styles.sectionTitle}>Scripture</Text>
        <Text style={styles.scriptureText}>{todayContent.scripture_text}</Text>
      </View>
      
      {/* Devotional */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Reflection</Text>
        <Text style={styles.body}>{todayContent.devotional_reflection}</Text>
      </View>
      
      {/* Prayer Prompt */}
      <View style={styles.prayerBox}>
        <Text style={styles.sectionTitle}>Prayer</Text>
        <Text style={styles.body}>{todayContent.prayer_prompt}</Text>
      </View>
      
      {/* Reflection Questions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Reflect</Text>
        {todayContent.reflection_questions.map((q, i) => (
          <Text key={i} style={styles.question}>• {q}</Text>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F1E8', // cream
    padding: 20,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5F1E8',
  },
  loadingText: {
    fontSize: 20,
    fontFamily: 'Georgia',
    color: '#3E3731',
  },
  header: {
    marginTop: 40,
    marginBottom: 20,
  },
  dateHeader: {
    fontSize: 32,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    color: '#3E3731',
  },
  subtitle: {
    fontSize: 16,
    fontFamily: 'Georgia',
    color: '#6B635A',
    marginTop: 5,
  },
  eventTitle: {
    fontSize: 28,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    color: '#8B4513', // saddle brown
    marginVertical: 15,
  },
  map: {
    width: '100%',
    height: 250,
    marginVertical: 20,
    borderRadius: 8,
  },
  scriptureRef: {
    fontSize: 18,
    fontFamily: 'Georgia',
    fontStyle: 'italic',
    color: '#8B4513',
    marginBottom: 20,
  },
  section: {
    marginVertical: 15,
  },
  sectionTitle: {
    fontSize: 22,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    color: '#3E3731',
    marginBottom: 10,
  },
  body: {
    fontSize: 18,
    fontFamily: 'Georgia',
    color: '#3E3731',
    lineHeight: 28,
  },
  contextBox: {
    backgroundColor: '#EDE7D9',
    padding: 15,
    borderRadius: 8,
    marginVertical: 15,
  },
  contextTitle: {
    fontSize: 20,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    color: '#8B4513',
    marginBottom: 10,
  },
  figureCard: {
    backgroundColor: '#FFFFFF',
    padding: 12,
    borderRadius: 6,
    marginBottom: 10,
    borderLeftWidth: 3,
    borderLeftColor: '#8B4513',
  },
  figureName: {
    fontSize: 20,
    fontFamily: 'Georgia',
    fontWeight: 'bold',
    color: '#3E3731',
    marginBottom: 5,
  },
  scriptureBox: {
    backgroundColor: '#FAF8F3',
    padding: 15,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#D4C5A9',
    marginVertical: 15,
  },
  scriptureText: {
    fontSize: 18,
    fontFamily: 'Georgia',
    fontStyle: 'italic',
    color: '#3E3731',
    lineHeight: 28,
  },
  prayerBox: {
    backgroundColor: '#E8DCC8',
    padding: 15,
    borderRadius: 8,
    marginVertical: 15,
  },
  question: {
    fontSize: 18,
    fontFamily: 'Georgia',
    color: '#3E3731',
    lineHeight: 26,
    marginBottom: 8,
  },
});
```

## MVP Scope - What You Get Day 1

### Immediate Functionality
✓ Open app → see today's biblical event
✓ AI-selected event appropriate for the date
✓ AI-generated devotional prose (narrative, reflection, prayer, questions)
✓ AI-generated renaissance-style map
✓ Full KJV scripture text
✓ Historical context
✓ Key figures with bios
✓ Clean, readable layout for elderly users
✓ Works offline (all content bundled)

### What's NOT in MVP
✗ Date picker (premium feature later)
✗ Timeline view (premium feature later)
✗ Audio narration
✗ Share functionality
✗ User accounts
✗ Bookmarks
✗ Search
✗ Multiple translations
✗ Ads (validate first, monetize later)

## Cost Estimates for 365-Day Generation

### AI API Costs (One-Time Generation)
**Claude API**: 365 days × 2 calls/day
- Date assignment: 365 × ~500 tokens input + ~1000 tokens output = ~$0.015/call
- Prose generation: 365 × ~800 tokens input + ~2500 tokens output = ~$0.025/call
- **Total Claude**: 365 × $0.04 = **~$15**

**DALL-E 3**: 365 maps
- HD quality 1792×1024: $0.08/image
- **Total DALL-E**: 365 × $0.08 = **~$30**

**Total one-time content generation**: **~$45**

### Ongoing Costs
$0 per user (content pre-generated and bundled in app)

## Implementation Timeline

### Week 1: Setup & Single Day Test
- Set up React Native/Expo project
- Install Claude + OpenAI SDKs
- Create generation script for ONE day
- Test full pipeline: date selection → prose → map → app display
- Verify output quality

### Week 2: Scale to 365 Days
- Run generation script for all 365 days
- Handle failures/retries
- Manual QC on ~50 random days
- Bundle content + maps into app

### Week 3: App Polish
- Implement full UI from wireframe
- Test on actual iPhone with large font settings
- Ensure offline functionality
- Test on grandma (literal usability test)

### Week 4: Deploy
- TestFlight beta for iOS
- Google Play internal testing for Android
- Fix critical bugs
- Public launch

**Total MVP timeline: 4 weeks**

## Validation Metrics (Before Adding Ads/Premium)

Track for first 1000 users:
- Daily Active Users (DAU) / Monthly Active Users (MAU)
- Average session length (target: 2-4 minutes)
- Day 7 retention (target: >40%)
- Day 30 retention (target: >20%)
- Organic shares (does anyone screenshot and share?)

If metrics hit targets → add ads + premium features
If metrics miss targets → iterate on content quality/UX

## Next Steps After MVP

1. **Content iteration**: Review user feedback, regenerate low-quality days
2. **Monetization**: Add AdMob banner ads (non-intrusive)
3. **Premium v1**: Date picker + timeline view ($2.99/month or $19.99/year)
4. **Audio narration**: Text-to-speech or recorded readings
5. **Share feature**: Generate shareable image cards
6. **Translations**: Vietnamese and Korean localization

## Critical Success Factors

**Content quality over quantity**: 365 mediocre AI-generated pages is worse than 30 excellent handcrafted ones. After MVP generation:
- Manually review at least 50 random days
- Regenerate any that feel generic or off-tone
- Keep AI prompts but add human QC layer

**Simplicity over features**: Elderly users want:
- Big text
- No confusing navigation
- Predictable behavior (opens to today, every time)
- No surprises

**Biblical accuracy matters**: Even with AI generation:
- Cross-check date assignments against biblical scholarship
- Don't fabricate events that contradict scripture
- Stay theologically conservative to avoid controversy

---

## Ralph's Action Items

1. **Set up project**:
   ```bash
   npx create-expo-app today-in-bible
   cd today-in-bible
   npm install @anthropic-ai/sdk openai
   ```

2. **Get API keys**:
   - Anthropic: https://console.anthropic.com/
   - OpenAI: https://platform.openai.com/

3. **Create generation script** (copy code from above)

4. **Generate content for one day** (January 11) and verify:
   - Event makes sense for winter
   - Prose is encouraging, not preachy
   - Map looks vintage/hand-drawn
   - Everything displays correctly in app

5. **If Day 1 works → scale to 365**

6. **Budget ~$45 for full generation + ~$50 for testflight/play store**

Total to working MVP: **~$100 + 4 weeks**
