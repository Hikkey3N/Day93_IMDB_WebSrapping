import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250/', headers=headers)

if response.status_code == 200:
    print("Success!")
    # Do something with response.content
else:
    print(f"Failed to fetch the page: {response.status_code}")