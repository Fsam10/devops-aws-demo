import requests
import json

with open("assets_seed.json", "r", encoding="utf-8") as f:
    assets = json.load(f)

for asset in assets:
    resp = requests.post("http://a96d66ca67c2e434d87b23f90277c46d-1143781009.us-east-1.elb.amazonaws.com/assets", json=asset)
    print(f"Ajout: {asset['name']} -> {resp.status_code}")
