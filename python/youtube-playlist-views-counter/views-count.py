'''
File name: program.py
Author: Ohidur Rahman Bappy
Author Website: https://ohidur.com
Author Email: ohidurbappy@gmail.com
Date created: 19/03/2020
Date last modified: 19/03/2020
Python Version: 3.8.1
'''

import traceback
import os
import datetime
# from urllib.parse import parse_qs, urlparse
import requests
import json

MAX_RESULTS_PER_PAGE = 50
YOTUBE_API_KEY = "YOUR_API_KEY_HERE"

API_ENDPOINT_GET_PLAYLIST_ITEMS = "https://www.googleapis.com/youtube/v3/playlistItems"
API_ENDPOINT_VIDEOS = "https://www.googleapis.com/youtube/v3/videos"

def get_video_ids_from_playlist(playlistId, video_Ids=None, nextPageToken=''):
    if video_Ids is not None:
        videoIds = video_Ids
    else:
        videoIds=[]
    payload = {
        'part': 'contentDetails',
        'maxResults': MAX_RESULTS_PER_PAGE,
        'playlistId': playlistId,
        'pageToken': nextPageToken,
        'key': YOTUBE_API_KEY,
    }

    response = requests.get(API_ENDPOINT_GET_PLAYLIST_ITEMS, params=payload)
    r = json.loads(response.content)

    items = r['items']
    # print(items)
    for item in items:
        contentDetails = item["contentDetails"]
        video_id = contentDetails['videoId']
        videoIds.append(video_id)

    if "nextPageToken" in r.keys():
       return get_video_ids_from_playlist(playlistId, videoIds, r["nextPageToken"])

    # print(videoIds)
    return videoIds



def main():
    playlists_ids=['PLTIh4N93lOTZivHW-hnlVtRuuYN1GeNGR']
    f = open("output.txt", "w")
    for playlist_id in playlists_ids:
        f.write(
            f"# Playlist URL: https://www.youtube.com/playlist?list={playlist_id}")
        f.write("\n\nOutput:\n")

        totalVideoCount = 0
        totalViewCount = 0

        print(".",end="")
        

        video_ids = get_video_ids_from_playlist(playlist_id)
        for video_id in video_ids:
            
            print(".",end="")
            totalVideoCount = totalVideoCount+1

            v_payload = {
                'part': 'statistics,snippet',
                'id': video_id,
                'key': YOTUBE_API_KEY
            }

            response = requests.get(API_ENDPOINT_VIDEOS, params=v_payload)

            print(".",end="")
            videoItem = json.loads(response.content)

            videoTitle = videoItem["items"][0]["snippet"]["title"]
            videoView = videoItem["items"][0]["statistics"]["viewCount"]

            f.write(
                f"Video{totalVideoCount} {videoTitle} - {videoView} views\n")

            totalViewCount = totalViewCount+int(videoView)


        print(f"Toatal Views: {totalViewCount}")

        f.write("\nSummary:\n")
        f.write(f"Total Video : {totalVideoCount}\n")
        f.write(f"Total Views : {totalViewCount}\n\n\n")


    today=(datetime.datetime.now()).strftime("%A , %d %B %Y")
    f.write(f"Date: {today}")
    f.close()

    print("\nDone")
    print("Output file saved as output.txt")


if __name__ == '__main__':
    print("Initializing")
    print("Progress:")
    try:
        main()
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT DETECTED. CLOSING MONITOR.")
    except Exception:
        traceback.print_exc()