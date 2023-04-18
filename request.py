import requests

def Media(link):
    url = "https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index"

    querystring = {"url":link}

    headers = {
        "X-RapidAPI-Key": "8ffab1e567msh9d3c11650e43ad1p122ee2jsn0db792092f5f",
        "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    response = response.json()
    return response

# print(media('https://www.instagram.com/p/CUwpJclNxS8/?utm_source=ig_web_copy_link'))
