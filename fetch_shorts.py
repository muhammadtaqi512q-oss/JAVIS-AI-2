import json
import subprocess

CATEGORIES = ["boys", "girls", "mountain"]
MAX_RESULTS_PER_CAT = 30

def fetch_shorts_with_ytdlp(category, count=30):
    # Search query
    search_query = f"ytsearch{count * 2}:{category} shorts"
    
    cmd = [
        "yt-dlp",
        search_query,
        "--dump-json",
        "--flat-playlist",
        "--ignore-errors",
        "--no-warnings",
        "--extractor-args", "youtube:player_client=android,web", # Anti-bot bypass
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    results = []
    
    for line in process.stdout:
        try:
            video_data = json.loads(line.strip())
            video_id = video_data.get("id")
            title = video_data.get("title", "No Title")
            
            if video_id:
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com/shorts/{video_id}"
                })
                
                # Desired count complete hone par stop karein
                if len(results) >= count:
                    break
        except json.JSONDecodeError:
            continue
            
    return results

def main():
    data = {"categories": {}}
    
    for category in CATEGORIES:
        print(f"Fetching 30 shorts for category: '{category}'...")
        shorts = fetch_shorts_with_ytdlp(category, MAX_RESULTS_PER_CAT)
        data["categories"][category] = shorts
        print(f"-> Successfully fetched {len(shorts)} shorts for '{category}'")

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n[SUCCESS] data.json generated!")

if __name__ == "__main__":
    main()
