import requests

# Your game placeId
place_id = "85896571713843"

# (Optional) Your Discord webhook
webhook_url = "https://discord.com/api/webhooks/1411629941178765365/k0Tw3CWiuZ935oPnQ4GnofN3xcWAc7q3KWg41_SwqtkOlyNotA5nNXzPjf1XVg1zcu4h"

# Roblox servers API
url = f"https://games.roblox.com/v1/games/{place_id}/servers/Public?sortOrder=Asc&limit=100"

all_ids = []
cursor = None

while True:
    query_url = url if not cursor else url + f"&cursor={cursor}"
    response = requests.get(query_url)
    data = response.json()

    if "data" not in data or len(data["data"]) == 0:
        break

    for server in data["data"]:
        all_ids.append(server["id"])

    cursor = data.get("nextPageCursor")
    if not cursor:
        break

# ✅ Save only IDs into servers.lua (Lua table)
with open("servers.lua", "w") as f:
    f.write("return {\n")
    f.write(",\n".join([f'"{sid}"' for sid in all_ids]))
    f.write("\n}")

print(f"✅ Done! {len(all_ids)} servers saved to servers.lua")

# (Optional) Send Discord message
if webhook_url:
    message = {"content": f"✅ Updated servers.lua with {len(all_ids)} servers"}
    try:
        requests.post(webhook_url, json=message)
    except Exception as e:
        print("⚠️ Failed to send webhook:", e)

