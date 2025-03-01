import asyncio
from shazamio import Shazam, Serialize
import yt_dlp
from bs4 import BeautifulSoup
from itertools import islice
from youtube_comment_downloader import *
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Expose only the desired function when imported as a module
__all__ = ["explain_the_joke"]

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

async def explain_the_joke(url):
    comments = await get_youtube_comments(url)
    video_info = await get_youtube_video(url)
    shazam_info = await shazam_song(video_info[0])
    info = format_info(comments, shazam_info, video_info)
    joke = interpret_data(info)
    cleanup(video_info[0])
    return joke

def interpret_data(info):
    system_prompt = (
'''
There is a channel on YouTube called Siivagunner. The premise of the channel is to upload video game music "rips". There are often called "High Quality Rips" as they are all in fact a bait and switch. Your job is to analyze the scraped data of one of these rips, 
(Youtube metadata, possible Shazam information, and a sample of the comment section) to identify the joke.
If there is a Shazam result, but the comments don't seem to align with the Shazam result, you are to ignore the Shazam result and focus on the comments, as Shazam was probably wrong.
You are to answer in-character as the channels mascot, the Joke Explainer 7000.
Ex. The Joke™: The melody of xxxx has been mashed up with xxxx!
Ex. The Joke™: The vocals of xxxx has been swapped with the vocals from the song xxxx!
Don't mention the comments or shazam, only explain the joke! Don't try to explain why it was made, or why its supposed to be funny.
If you are unable to indentify the joke, simply say "I don't know what the joke is, but I can tell you that this is a High Quality Rip!" and nothing else. Do not mention the channel name or the mascot name.
'''
)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": info,
            },
        ],
        model="gpt-4o",
    )
    response = chat_completion.choices[0].message.content
    return response

async def get_youtube_comments(video_url):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
    return comments

async def get_youtube_video(video_url):
    temp_dir = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(id)s.%(ext)s'),
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata'
            }
        ]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            filename = os.path.splitext(filename)[0] + ".mp3"
            title = info.get('fulltitle', None)
            return [filename, title]
    except Exception as e:
        print(f"Error getting video info: {e}")
        return {}

async def shazam_song(song_path):
    shazam = Shazam()
    result = await shazam.recognize(song_path)
    track = result.get("track")
    if track:
        print(f"Found song: {track.get('title')} - {track.get('subtitle')}")
        return f"{track.get('title')} - {track.get('subtitle')}"
    else:
        print("No match found.")
        return None

def format_info(comments, shazam_info, video_info):
    formatted = (
        "-=-=-=-=-=-=-=-=-\n"
        "Information about the High Quality Rip:\n"
        "-=-=-=-=-=-=-=-=-\n\n"
        "Video Info:\n"
        f"{video_info[1]}\n\n"
        "Shazam Info:\n"
        f"{shazam_info}\n\n"
        "Formatted Comments:\n"
    )
    for comment in islice(comments, 20):
        formatted += comment.get('text', '') + "\n"
    formatted += "\n-=-=-=-=-=-=-=-=-"
    return formatted

def cleanup(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print(f"The file {filename} does not exist.")
    except Exception as e:
        print(f"Error deleting file: {e}")


async def test():
    joke = await explain_the_joke('https://www.youtube.com/watch?v=lH93HsQCt9w')
    print(joke)
    
if __name__ == "__main__":
    asyncio.run(test())
