# Swift QA Packets

Updated: 2026-07-03

Use one packet per returned Swift module before integration.

Ask the QA agent to review the complete returned files against this checklist:

- Compiles as SwiftUI source with the shared model stubs.
- No hidden dependencies, networking, auth, analytics, or StoreKit unless the packet explicitly allowed it.
- Includes previews or mock data.
- Preserves `confidence`, `confidence_note_*`, source URL, optional `place`, and EN/VI language behavior.
- Text wraps on iPhone SE width and does not rely on fixed-height body containers.
- Uses dark-first Anno palette and one accent color per screen.
- Does not premium-gate Today text or source transparency.

Return:

```json
{
  "module": "",
  "verdict": "pass|revise",
  "compile_risks": [],
  "integration_risks": [],
  "required_changes": [],
  "nice_to_have_changes": []
}
```
