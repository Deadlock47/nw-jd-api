from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["https://save-ur-jav.vercel.app/","https://*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def __getJsonResult(data: dict[str]):
        result = {"id": data["dvd_id"]}
        result["title"] = data["title_en"]
        result["title_ja"] = data["title_ja"]
        result[
            "page"
        ] = f"https://r18.dev/videos/vod/movies/detail/-/id={data['content_id']}/"
        result["poster"] = data.get("jacket_full_url", None)
        result["preview"] = data.get("sample_url", None)

        ## result.details
        result["details"] = {
            "director": None,
            "release_date": None,
            "runtime": None,
            "studio": None,
        }
        result["details"]["director"] = (
            data["directors"][0]["name_romaji"] if data["directors"] else None
        )
        result["details"]["release_date"] = data.get("release_date", None)
        result["details"]["runtime"] = data.get("runtime_mins", None)
        result["details"]["studio"] = data.get("maker_name_en", None)

        result["actress"] = [
            {
                "name": a["name_romaji"],
                "image": "https://pics.dmm.co.jp/mono/actjpgs/" + a["image_url"]
                
            }
            for a in data["actresses"]
        ]

        result["screenshots"] = [ss["image_full"] for ss in data["gallery"]]
        result["tags"] = [c["name_en"] for c in data["categories"]]
        return result

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/r18/{code}")
async def get_code_data(code):
    url = f"https://r18.dev/videos/vod/movies/detail/-/combined={code}/json"
    data = requests.get(url)
    # print(data)
    
    if data.ok:
        return __getJsonResult(data.json())
    else :
        return {"status" : "failed"}
