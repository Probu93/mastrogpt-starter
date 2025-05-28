import os, requests as req, base64
import vision2 as vision
from packages.vision.store.bucket import Bucket
import time

USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "Load Image",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def form(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")

    # Salva su S3
    img_bytes = base64.b64decode(img)
    bucket_args = {
      "S3_HOST": os.getenv("S3_HOST"),
      "S3_PORT": os.getenv("S3_PORT"),
      "S3_ACCESS_KEY": os.getenv("S3_ACCESS_KEY"),
      "S3_SECRET_KEY": os.getenv("S3_SECRET_KEY"),
      "S3_BUCKET_DATA": os.getenv("S3_BUCKET_DATA"),
      "S3_API_URL": os.getenv("S3_API_URL"),
    }
    bucket = Bucket(bucket_args)
    ts = time.strftime("%Y%m%d%H%M%S") + str(int(time.time()*1000) % 1000)
    key = f"uploads/{ts}.jpg"
    wr = bucket.write(key, img_bytes)

    if wr != "OK":
      out = f"Upload failed: {wr}"
      res['html'] = f'<img src="data:image/png;base64,{img}">'
    else:
      url = bucket.exturl(key, expiration=3600)
      res['html'] = f'<img src="{url}">'

      # Vision decode su base64 originale
      vis = vision.Vision(args)
      out = vis.decode(img)

  res['form'] = FORM
  res['output'] = out
  return res
