from bs4 import BeautifulSoup

# Read downloaded HTML
with open("debug.html", "r", encoding="utf-8") as f:
    html = f.read()

# Parse HTML
soup = BeautifulSoup(html, "html.parser")

# Remove unnecessary tags
for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

# Extract text
text = soup.get_text(separator="\n")

# Split into lines and remove whitespace
lines = [line.strip() for line in text.splitlines()]

# Remove empty lines
lines = [line for line in lines if line]

# Remove unwanted spam/content
spam_keywords = [
    "slot gacor",
    "slot gacor terbaik"
]

cleaned_lines = []

for line in lines:
    is_spam = False

    for keyword in spam_keywords:
        if keyword.lower() in line.lower():
            is_spam = True
            break

    if not is_spam:
        cleaned_lines.append(line)

# Remove duplicate consecutive lines
final_lines = []

for line in cleaned_lines:
    if not final_lines or final_lines[-1] != line:
        final_lines.append(line)

# Join everything
clean_text = "\n".join(final_lines)

# Save extracted text
with open("ngo_data.txt", "w", encoding="utf-8") as f:
    f.write(clean_text)

print("=" * 50)
print("Extraction Complete")
print("Characters extracted:", len(clean_text))
print("Lines extracted:", len(final_lines))
print("Saved to ngo_data.txt")
print("=" * 50)