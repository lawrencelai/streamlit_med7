import json
import re

import spacy
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TextRequest(BaseModel):
    type: str | None = None
    text: str


@app.post("/analyse")
async def analyse(request: TextRequest):
    print(request.type)
    print(request.text)
    if request.type == "random":
        return {"message": "Not support yet"}
    med7 = spacy.load("en_core_med7_lg")

    doc = med7(request.text)

    med7_annotation = []

    for ent in doc.ents:
        if ent.label_ == "DRUG":
            if {"text": ent.text, "label_": ent.label_} not in med7_annotation:
                med7_annotation.append({"text": ent.text, "label_": ent.label_})

    med7_result = []

    anno_map = med7_annotation
    print(anno_map)
    for i in anno_map:
        for match in re.finditer(i['text'], request.text):
            med7_result.append({"start": match.start(), "end": match.end(), "label": [i['label_']]})
    print(json.dumps(med7_result))
    return json.dumps(med7_result)
