import requests

url = "https://inamigosfoundation.org.in/"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("Status Code:", response.status_code)
print("Response Length:", len(response.text))

with open("debug.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Saved debug.html")