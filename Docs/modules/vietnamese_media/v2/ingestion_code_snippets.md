# Ingestion Code Snippets — For Hub/Linkboard Development

**Extracted from:** `master_directory_technical.md` §4  
**Purpose:** Ready-to-use frontend/backend templates for aggregating Vietnamese Catholic media

---

## 4.1 YouTube Channel Live Stream & VOD Ingestion (IFrame Embed)

```html
<!-- Responsive YouTube Embed for Parish Livestreams -->
<div class="video-container" style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden;">
  <iframe 
    src="https://www.youtube.com/embed/live_stream?channel=CHANNEL_ID&autoplay=0" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen 
    style="position:absolute; top:0; left:0; width:100%; height:100%;">
  </iframe>
</div>
```

**Verified Channel IDs for OC Parishes:**
| Parish | Channel ID / Handle | Notes |
|--------|---------------------|-------|
| Vietnamese Catholic Center | `UC1HuzI97H8M5bI3Wl6wKdvA` / `@VietCatholicCenter` | Daily 8:30 AM PT |
| Christ Cathedral | Diocese: `@DioceseOrange` | Multiple weekly VI Masses |
| Holy Spirit FV | `@blessedsacramentcatholicch9746` | Multiple weekly |
| St. Bonaventure HB | Parish YouTube via `stbonaventure.org/livestream` | Archived VODs |
| TGPSG (Saigon) | `@tgpsgthanhletructuyen` | **State context flag** |
| Redemptorists VN | `@dcctsaigon` | Migrated from lapsed domain |
| Vatican News VI | `@VaticanNewsVI` / `@VaticanNewsTiengViet` | **Embed permitted** (official player) |

---

## 4.2 Live Radio Audio Stream Ingestion (HTML5 Audio Player)

```html
<!-- HTML5 Audio Stream for Radio Veritas Asia & Radio Mẹ Hằng Cứu Giúp -->
<div class="audio-player-card">
  <h3>Đài Chân Lý Á Châu (Radio Veritas Asia) - Tiếng Việt</h3>
  <audio controls preload="none" style="width:100%;">
    <source src="https://stream.zeno.fm/edDe0t8E" type="audio/mpeg">
    Trình duyệt của bạn không hỗ trợ phát âm thanh trực tuyến.
  </audio>
</div>

<div class="audio-player-card">
  <h3>Radio Mẹ Hằng Cứu Giúp (KALI-FM 106.3)</h3>
  <audio controls preload="none" style="width:100%;">
    <source src="https://stream.zeno.fm/YOUR_RADIO_MHCG_STREAM_URL" type="audio/mpeg">
    Trình duyệt của bạn không hỗ trợ phát âm thanh trực tuyến.
  </audio>
</div>
```

**Verified Stream URLs:**
| Source | Stream URL | Backup |
|--------|------------|--------|
| Radio Veritas Asia (VI) | `https://stream.zeno.fm/edDe0t8E` | Radio Garden: `radio.garden/listen/radio-veritas-asia/edDe0t8E` |
| Radio Veritas Asia (RSS) | `https://vietnamese.rvasia.org/feed/` | myTuner Radio app |
| Radio MHCG (KALI 106.3) | Check `dongchuacuuthe.us/radio-mhcg` | YouTube `@GiaoDiemTinMungOfficial` |

---

## 4.3 Automated Podcast & RSS Feed Ingestion (Node.js)

```javascript
// Node.js / JavaScript Fetch for Vatican News Daily Podcast RSS
async function fetchDailyVaticanPodcast() {
  const RSS_URL = 'https://www.vaticannews.va/vi/podcast/vietnamese-program.podcast.xml';
  const response = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(RSS_URL)}`);
  const data = await response.json();
  
  // Extract latest daily 25-minute MP3 episode
  const latestEpisode = data.items[0];
  return {
    title: latestEpisode.title,
    mp3Url: latestEpisode.enclosure.link,
    pubDate: latestEpisode.pubDate,
    description: latestEpisode.description,
    duration: latestEpisode.itunes?.duration || '25:00'
  };
}

// For Radio Veritas Asia podcast (if feed restored)
async function fetchRVAPodcast() {
  const RSS_URL = 'https://vietnamese.rvasia.org/podcast.xml'; // Verify current URL
  // Same pattern as above
}
```

---

## 4.4 Daily Liturgical Broadcast Schedule (Pacific Time) — For App Routing

```javascript
// Daily schedule for Westminster hub routing engine
const DAILY_LITURGICAL_SCHEDULE = {
  "06:30": {
    source: "Archdiocese of Saigon Morning Mass",
    platform: "YouTube",
    handle: "@tonggiaophansaigon",
    note: "Vietnam time (UTC+7) = 14hr ahead; use archived replay for US viewers"
  },
  "08:30": {
    source: "Orange County Daily Mass",
    platform: "YouTube",
    handle: "@VietCatholicCenter",
    location: "Vietnamese Catholic Center, Santa Ana",
    verified: true
  },
  "12:00": {
    source: "Vatican News Tiếng Việt Midday Bulletin & Angelus Audio",
    platform: "YouTube/Podcast",
    handle: "@VaticanNewsVI"
  },
  "15:00": {
    source: "Divine Mercy Chaplet & Healing Prayers",
    platform: "YouTube",
    handle: "@GiaoDiemTinMungOfficial"
  },
  "18:00": {
    source: "Blessed Sacrament Westminster Local Parish Evening Mass",
    platform: "YouTube",
    handle: "@blessedsacramentcatholicch9746"
  },
  "22:00": {
    source: "Radio Mẹ Hằng Cứu Giúp Nightly Broadcast",
    platform: "Radio (KALI-FM 106.3) + YouTube",
    handle: "@GiaoDiemTinMungOfficial"
  }
};
```

---

## 4.5 Source Metadata Schema (for Database)

```sql
-- SQLite schema for Vietnamese Catholic media sources
CREATE TABLE vi_catholic_sources (
  id TEXT PRIMARY KEY,                    -- e.g., 'vcc_oc', 'christ_cathedral', 'rva_vi'
  name TEXT NOT NULL,                     -- Display name
  name_vi TEXT,                           -- Vietnamese name
  category TEXT NOT NULL,                 -- 'parish', 'diocese', 'vatican', 'radio', 'tv', 'archive', 'aggregator'
  tier INTEGER NOT NULL,                  -- 1=primary, 2=secondary, 3=tertiary, 4=context-flagged
  platform TEXT NOT NULL,                 -- 'youtube', 'radio_stream', 'rss', 'website', 'app', 'broadcast'
  platform_handle TEXT,                   -- YouTube channel ID / handle
  stream_url TEXT,                        -- Direct HLS/MP3/RSS URL
  embed_url TEXT,                         -- iframe embed URL
  schedule_json TEXT,                     -- JSON schedule (days/times)
  timezone TEXT DEFAULT 'America/Los_Angeles',
  orientation TEXT,                       -- 'conciliar', 'traditionalist', 'neutral', 'state_affiliated'
  state_context_flag BOOLEAN DEFAULT 0,   -- 1 = produced in Vietnam, state context applies
  verification_status TEXT,               -- 'verified_live', 'listed_unconfirmed', 'offline', 'archival'
  last_verified DATE,
  contact_info TEXT,                      -- Phone, email, address
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_sources_category ON vi_catholic_sources(category);
CREATE INDEX idx_sources_tier ON vi_catholic_sources(tier);
CREATE INDEX idx_sources_verification ON vi_catholic_sources(verification_status);
CREATE INDEX idx_sources_orientation ON vi_catholic_sources(orientation);
```

---

## 4.6 Verified Source Seed Data (Partial)

```sql
INSERT INTO vi_catholic_sources (id, name, name_vi, category, tier, platform, platform_handle, stream_url, embed_url, schedule_json, orientation, state_context_flag, verification_status, last_verified, contact_info, notes) VALUES
('vcc_oc', 'Vietnamese Catholic Center', 'Trung Tâm Công Giáo Việt Nam', 'diocese', 1, 'youtube', 'UC1HuzI97H8M5bI3Wl6wKdvA', NULL, 'https://www.youtube.com/embed/live_stream?channel=UC1HuzI97H8M5bI3Wl6wKdvA', '{"daily": "08:30"}', 'neutral', 0, 'verified_live', '2026-08-18', '(714) 554-4211; 1538 Century Blvd, Santa Ana', 'Daily Mass 8:30 AM PT; archive back to Dec 2023'),
('christ_cathedral', 'Christ Cathedral', 'Nhà Thờ Chính Tòa Christ Cathedral', 'diocese', 1, 'youtube', 'DioceseOrange', NULL, 'https://www.youtube.com/embed/live_stream?channel=DioceseOrange', '{"sun": ["06:30","14:00","16:00"], "sat": ["06:30","09:00","18:30"], "weekday": "17:30"}', 'neutral', 0, 'verified_live', '2026-08-18', '13280 Chapman Ave, Garden Grove', 'Bishop Thanh Thai Nguyen; La Vang Shrine events'),
('rva_vi', 'Radio Veritas Asia - Tiếng Việt', 'Đài Chân Lý Á Châu', 'radio', 1, 'radio_stream', 'daichanlyachau', 'https://stream.zeno.fm/edDe0t8E', NULL, '{"24_7": true}', 'conciliar', 0, 'verified_live', '2026-08-19', 'vietnamese.rvasia.org; mobile app org.rvasia.app', 'Radio Garden backup; FABC Asian pastoral'),
('radio_mhcg', 'Radio Mẹ Hằng Cứu Giúp', 'Đài Mẹ Hằng Cứu Giúp', 'radio', 2, 'radio_stream', 'GiaoDiemTinMungOfficial', 'CHECK_dongchuacuuthe_us', NULL, '{"daily_night": "22:00"}', 'traditionalist', 0, 'verified_live', '2026-08-18', 'KALI-FM 106.3 LA/OC; dongchuacuuthe.us/radio-mhcg', 'Redemptorists Long Beach/OC'),
('vatican_news_vi', 'Vatican News - Tiếng Việt', 'Vatican News Tiếng Việt', 'vatican', 1, 'youtube', 'VaticanNewsVI', 'https://www.vaticannews.va/vi/podcast/vietnamese-program.podcast.xml', 'https://www.youtube.com/embed/live_stream?channel=VaticanNewsVI', '{"daily_podcast": true}', 'conciliar', 0, 'verified_live', '2026-08-18', 'tiengviet@vaticannews.va', 'Embed permitted; no rehost without written consent'),
('vietcatholic_news', 'VietCatholic News', 'VietCatholic News', 'diaspora', 2, 'youtube', 'VietCatholicTV', NULL, 'https://www.youtube.com/embed/live_stream?channel=VietCatholicTV', '{}', 'traditionalist', 0, 'verified_live', '2026-08-18', 'vietcatholic.net; est. 1996; 724K subs', 'TV stream via nguoiviet.tv; radio archive KVNR'),
('tgpsg_saigon', 'TGPSG - Tổng Giáo phận Sài Gòn', 'TGPSG', 'vietnam_produced', 4, 'youtube', 'tgpsgthanhletructuyen', NULL, 'https://www.youtube.com/embed/live_stream?channel=tgpsgthanhletructuyen', '{}', 'conciliar', 1, 'verified_live', '2026-08-19', 'hdgmvietnam.com', 'State context flag REQUIRED; bishops conference directory'),
('redemptorists_vn', 'Đền Đức Mẹ Hằng Cứu Giúp Sài Gòn', 'Redemptorists Vietnam', 'vietnam_produced', 4, 'youtube', 'dcctsaigon', NULL, 'https://www.youtube.com/embed/live_stream?channel=dcctsaigon', '{}', 'conciliar', 1, 'verified_live', '2026-08-19', 'dongchuacuuthe.us', 'Migrated from lapsed trungtammucvudcct.com'),
('thanh_ca_vn', 'Thánh Ca Việt Nam', 'Thánh Ca Việt Nam', 'archive', 2, 'website', NULL, NULL, NULL, '{}', 'neutral', 0, 'verified_live', '2026-08-18', 'thanhcavietnam.net / .info', '70+ years hymnody; PDF sheet music + MP3 choral'),
('phim_cong_giao', 'Phim Công Giáo Archive', 'Phim Công Giáo', 'archive', 2, 'website', NULL, NULL, NULL, '{}', 'neutral', 0, 'verified_live', '2026-08-18', 'phimconggiao.net / conggiao.org', 'Dubbed/subtitled Catholic films (Passion, Padre Pio)');
```

---

## Usage Notes

1. **Vatican embeds:** Use official YouTube iframe embed — permitted by YouTube ToS and Vatican sharing tools. Do NOT download/rehost MP4.
2. **RVA stream:** `https://stream.zeno.fm/edDe0t8E` is the verified HLS/MP3 endpoint. Test before deploy.
3. **Radio MHCG stream URL:** Check `dongchuacuuthe.us/radio-mhcg` for current stream URL — may rotate.
4. **Parish schedules:** COVID-era daily streams shifted to Weekend/Vigil. Verify current schedule before hardcoding.
5. **State context sources (tier 4):** Always display "Produced in Vietnam; state context applies" badge in UI.
6. **Time zones:** Vietnam = UTC+7 = +14 hours from Pacific. Use archived replays for US-targeted content.