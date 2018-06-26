# OTX Pulse explort

Small script that exports IOCs from your AlienVault OTX subscription to csv and stdout.

Edit the api_key in the script with the api key from your OTX account (https://otx.alienvault.com/api) before running.

## Dependencies
Unidecode is the only non-standard dependency at this time:

```pip install unidecode```

## Usage

### Linux:
`python otx_feed.py [output.csv]`

### Windows:
```C:\Python27\python.exe .\otx_feed.py [output.csv]```

