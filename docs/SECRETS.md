# Anno — Secrets Mapping

Exact mapping: code/CI placeholder → GitHub Secret name → source. Set every GitHub Secret under
Repository Settings → Secrets and variables → Actions before running `ios-release.yml`.

| Placeholder used in code/CI | GitHub Secret name | Source / where to get it |
|---|---|---|
| `MATCH_GIT_URL` | `MATCH_GIT_URL` | Private git repo URL holding match certificates/profiles |
| `MATCH_PASSWORD` | `MATCH_PASSWORD` | match repo encryption password (store in Doppler `ichabod`/`prd`) |
| `APP_STORE_CONNECT_API_KEY_KEY_ID` | `APP_STORE_CONNECT_API_KEY_KEY_ID` | ASC API key `.p8` key ID (App Store Connect → Keys) |
| `APP_STORE_CONNECT_API_KEY_ISSUER_ID` | `APP_STORE_CONNECT_API_KEY_ISSUER_ID` | ASC API key issuer ID |
| `APP_STORE_CONNECT_API_KEY_CONTENT` | `APP_STORE_CONNECT_API_KEY_CONTENT` | **raw `.p8` file contents (NOT base64)** |
| `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` | `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD` | appleid.apple.com → App-Specific Passwords |
| `REVENUECAT_API_KEY` | `REVENUECAT_API_KEY` | RevenueCat dashboard (only if server-side webhooks used; the SDK **public** key goes in the app bundle) |

> GitHub auto-masks secrets in Actions logs. Never `echo $SECRET`, print secrets, or commit them to the repo.
> Use Doppler (`ichabod`/`prd`) as the source of truth; export into GitHub Secrets — do not hand-type.

## How secrets flow
- `Matchfile` reads `MATCH_GIT_URL` from env.
- `Fastfile`/ASC API uses the three `APP_STORE_CONNECT_API_KEY_*` values.
- `pilot` upload uses `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD`.
- `MATCH_PASSWORD` decrypts the match repo locally during `match`.
