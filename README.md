# BSC-Pro Gateway EG122SN Restart Button

HACS-Integration für BSC-Pro EG122SN Gateway. Button führt Login → JWT → Restart aus.

## Installation
1. Via HACS: Integrations → Suche "BSC-Pro"
2. Konfiguriere IP + Login-Hash
3. Button zu Dashboard hinzufügen

## Konfiguration
- **IP-Adresse**: `10.0.0.2`
- **Login-Hash**: `6691F8B...` (64 Zeichen Hex)

## API-Flow
1. `POST /rest/authentication/login` → JWT Token
2. `POST /rest/system/restart` mit `X-Auth-Token`

## Donate
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/networkcoder)
