import json
import subprocess

CATEGORIES = ["boys", "girls", "mountain"]
MAX_RESULTS_PER_CAT = 30

def fetch_shorts_with_ytdlp(category, count=30):
    # Search query specifically looking for shorts
    search_query = f"ytsearch{count}:{category} shorts"
    
    # Run yt-dlp command to extract json info without downloading video
    cmd = [
        "yt-dlp",
        search_query,
        "--dump-json",
        "--flat-playlist",
        "--ignore-errors",
        "--no-warnings"
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    results = []
    
    for line in process.stdout:
        try:
            video_data = json.loads(line)
            video_id = video_data.get("id")
            title = video_data.get("title", "No Title")
            
            if video_id:
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com/shorts/{video_id}"
                })
        except json.JSONDecodeError:
            continue
            
    return results

def main():
    data = {"categories": {}}
    
    for category in CATEGORIES:
        print(f"Fetching 30 shorts for category: '{category}' without API key...")
        shorts = fetch_shorts_with_ytdlp(category, MAX_RESULTS_PER_CAT)
        data["categories"][category] = shorts
        print(f"Fetched {len(shorts)} shorts for '{category}'")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n[SUCCESS] data.json updated successfully!")

if __name__ == "__main__":
    main()
