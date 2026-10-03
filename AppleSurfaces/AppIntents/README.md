# App Intents staging

This source is deliberately outside the active iPhone target while Mac access is limited.

It uses the current App Intents runtime model:
- background read-only intents where possible
- `supportedModes` instead of deprecated `openAppWhenRun`
- no fake foreground routing

Initial shortcut vocabulary:
- Today in Anno
- Today's Feast
- Pilgrimage Routes

Activation later:
1. include source in the app target
2. share the minimal fixture/glance models
3. validate shortcut discovery in Shortcuts/Siri
4. only then add foreground navigation intents for Today/Map
5. keep spoken responses short and useful
