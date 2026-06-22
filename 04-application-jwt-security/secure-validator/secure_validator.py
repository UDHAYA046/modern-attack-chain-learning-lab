import jwt
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

KEY_DIR = BASE_DIR/"keys"
SAMPLE_DIR = BASE_DIR/"sample-data"

PUBLIC_KEY = (KEY_DIR/"public.pem").read_text()

 # load tokens
with open(SAMPLE_DIR/"sample_tokens.json") as f:
    tokens = json.load(f)

# validate
for name,token in tokens.items():

    try:

        decoded = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"]
        )

        print(name,"VALID")

    except Exception as e:

        print(name,"BLOCKED")
        print(e)


