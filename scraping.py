import os
import googleapiclient.discovery
import pandas as pd

# Set API key
API_KEY = "SECRET"
VIDEO_ID = "Aja2KfuoqGA"  # Jake Paul vs. Mike Tyson FIGHT HIGHLIGHTS 🥊 | ESPN Ringside

# Setup YouTube API
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_comments(video_id, max_comments=50000):
    comments = []
    next_page_token = None
    
    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "text": comment["textOriginal"],
                "likes": comment["likeCount"],
                "replies": item["snippet"]["totalReplyCount"],
                "timestamp": comment["publishedAt"]
            })
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        
    return comments

# get comments
data = get_comments(VIDEO_ID)

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("dataset_scraping.csv", index=False)
print("Scraping selesai! Data tersimpan dalam dataset_scraping.csv")
