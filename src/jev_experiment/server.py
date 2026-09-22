"""Local server for the red flag detector."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

from jev_experiment.detector import analyze

WEB_DIR = Path(__file__).resolve().parents[2] / "web"

app = FastAPI(title="Red Flag Detector")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=4000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze_text(body: AnalyzeRequest) -> dict:
    try:
        return analyze(body.text)
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail="Jev analysis failed") from error


app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the red flag detector")
    parser.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8765")))
    args = parser.parse_args()
    url = f"http://{args.host}:{args.port}/"
    print(f"🚩 Red flag detector: {url}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
