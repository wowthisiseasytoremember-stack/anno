# Artwork Clearance Packets

Updated: 2026-07-03

Create one packet per candidate from `data/assets/artwork_clearance_queue_2026-07-03_2026-07-16.json`.

For each candidate, return:

```json
{
  "entry_id": "",
  "artwork_title": "",
  "recommended_ship_decision": "cleared_for_bundle|candidate_pending_clearance|placeholder_only|replace",
  "rights_evidence": {
    "object_url": "",
    "image_url": "",
    "rights_url": "",
    "rights_statement": "",
    "commercial_app_use": "allowed|unclear|not_allowed",
    "app_store_screenshot_use": "allowed|unclear|not_allowed",
    "attribution": ""
  },
  "replacement_candidate": null,
  "notes": []
}
```

Rules: modern or unclear images default to `placeholder_only`; museum candidates require explicit rights evidence; public-domain candidates still need source, image URL, and attribution.
