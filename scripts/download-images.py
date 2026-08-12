#!/usr/bin/env python3
"""Download images from the live Wix CDN into assets/images/."""

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

WIX = "https://static.wixstatic.com/media"

ASSETS = {
    "logo.jpeg": f"{WIX}/0eecb9_8c7b9ae27008430bbb9334fe3656b378~mv2.jpeg/v1/fill/w_294,h_160,al_c,q_80/0eecb9_8c7b9ae27008430bbb9334fe3656b378~mv2.jpeg",
    "headshot.jpg": f"{WIX}/0eecb9_0a7e4318ef74466097c77beb6fb5a015~mv2.jpg/v1/crop/x_0,y_19,w_1883,h_1883/fill/w_960,h_960,al_c,q_85/0eecb9_0a7e4318ef74466097c77beb6fb5a015~mv2.jpg",
    "icon-linkedin.png": f"{WIX}/6ea5b4a88f0b4f91945b40499aa0af00.png/v1/fill/w_48,h_48,al_c,q_85/6ea5b4a88f0b4f91945b40499aa0af00.png",
    "icon-instagram.png": f"{WIX}/01c3aff52f2a4dffa526d7a9843d46ea.png/v1/fill/w_48,h_48,al_c,q_85/01c3aff52f2a4dffa526d7a9843d46ea.png",
    "design/fidget-1.jpg": f"{WIX}/0eecb9_7ec40a8876854bb5a0d2b4497fef4932~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_7ec40a8876854bb5a0d2b4497fef4932~mv2.jpg",
    "design/fidget-2.jpg": f"{WIX}/0eecb9_dcf1400f334344e2830c9e7e5e0e6e6d~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_dcf1400f334344e2830c9e7e5e0e6e6d~mv2.jpg",
    "design/fidget-3.jpg": f"{WIX}/0eecb9_ab091dec5af1434a94b3f6db4b86bda8~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_ab091dec5af1434a94b3f6db4b86bda8~mv2.jpg",
    "design/fidget-4.jpg": f"{WIX}/0eecb9_e8fb32ea307d470fad782cc9ee5b8971~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_e8fb32ea307d470fad782cc9ee5b8971~mv2.jpg",
    "design/canary-1.jpg": f"{WIX}/0eecb9_3bb24ae2f0ef485887e876834687515e~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_3bb24ae2f0ef485887e876834687515e~mv2.jpg",
    "design/canary-2.jpg": f"{WIX}/0eecb9_5350b7de5fd9490a8c043c6dad4a9351~mv2.jpg/v1/fill/w_980,h_735,q_90/0eecb9_5350b7de5fd9490a8c043c6dad4a9351~mv2.jpg",
    "design/canary-3.gif": f"{WIX}/0eecb9_127cd14cf8f849248723a076032c855f~mv2.gif",
    "design/ghana-1.jpeg": f"{WIX}/0eecb9_e2ae1033bde74804be55f2c5053f18c6~mv2.jpeg/v1/fill/w_980,h_735,q_90/0eecb9_e2ae1033bde74804be55f2c5053f18c6~mv2.jpeg",
    "design/ghana-2.jpeg": f"{WIX}/0eecb9_560cfd21cd17431385f913139698a2df~mv2.jpeg/v1/fill/w_980,h_735,q_90/0eecb9_560cfd21cd17431385f913139698a2df~mv2.jpeg",
    "design/ghana-3.jpeg": f"{WIX}/0eecb9_0cd8d6cf25a84ab3b8fb133f324df75b~mv2.jpeg/v1/fill/w_980,h_735,q_90/0eecb9_0cd8d6cf25a84ab3b8fb133f324df75b~mv2.jpeg",
    "design/tide-1.jpeg": f"{WIX}/0eecb9_266f103c14f14f33805dcda3439b6fb8~mv2.jpeg/v1/fill/w_980,h_735,q_90/0eecb9_266f103c14f14f33805dcda3439b6fb8~mv2.jpeg",
    "design/tide-2.jpeg": f"{WIX}/0eecb9_24d570ada95b4d5e8f2def72b4be1142~mv2.jpeg/v1/fill/w_980,h_735,q_90/0eecb9_24d570ada95b4d5e8f2def72b4be1142~mv2.jpeg",
}

DRAWING_SPEC = [
    ("drawing-01.png", "0eecb9_2ac217134ed64532a75e65f1ceb667fc~mv2.png", "Illustration"),
    ("drawing-02.jpeg", "0eecb9_535eb600fc4a4177bf1212c3a18b340e~mv2.jpeg", "Portraits"),
    ("drawing-03.jpg", "0eecb9_bf59841acbaf4218871b97ba1cd173d2~mv2.jpg", "Sketching storyboards"),
    ("drawing-04.jpg", "0eecb9_09f3f50bbb6142f3ad365b87f387dd75~mv2.jpg", "Simple characters sitting"),
    ("drawing-05.jpeg", "0eecb9_3240f2818e394ff7b7caf53cd6e2f674~mv2.jpeg", "Cards"),
    ("drawing-06.jpg", "0eecb9_36eb7eedcec543baa02e0568af8b003e~mv2.jpg", "Roleplaying game group"),
    ("drawing-07.jpeg", "0eecb9_b412e9b0e42c4b0c8e986046522f81fa~mv2.jpeg", "Dancing man"),
    ("drawing-08.jpg", "0eecb9_5d55bc16652543ca99aa471922adc61d~mv2.jpg", "Man and cat"),
    ("drawing-09.jpg", "0eecb9_3973afdf680b4fb9b1fbd5eee863ae6b~mv2.jpg", "No space for yoga"),
    ("drawing-10.jpg", "0eecb9_73ef95a8466448cd9060c97a2a9d6782~mv2.jpg", "Presentation about AI"),
    ("drawing-11.jpg", "0eecb9_0fab2f61c5644dbb8419ec9b40f14830~mv2.jpg", "Sketch of hands"),
    ("drawing-12.jpg", "0eecb9_1be70b68f89e4cfdb2fc6333ee05eb9b~mv2.jpg", "Armoured character concept"),
    ("drawing-13.jpeg", "0eecb9_3ce1ae85f4ef4a33988293f3003637d9~mv2.jpeg", "Roleplay character drawing"),
    ("drawing-14.jpeg", "0eecb9_9f677081ad81418d863f070e47db29a3~mv2.jpeg", "Webcomic tribute"),
    ("drawing-15.jpg", "0eecb9_3330594cc8bb44fdbda4e8fe02c4e36f~mv2.jpg", "Life drawing of hawk"),
    ("drawing-16.jpg", "0eecb9_88bc3168c99b48d0a1a085dbb437f5c4~mv2.jpg", "Comic book cover"),
    ("drawing-17.jpg", "0eecb9_505bc9471d6c4832ab000769a469859a~mv2.jpg", "Dramatic roleplaying game moment"),
    ("drawing-18.jpeg", "0eecb9_473498437a024245a273497199fdc654~mv2.jpeg", "Three aunties"),
    ("drawing-19.jpg", "0eecb9_5302d1a2d5234b60a5e5dcfe95d618f2~mv2.jpg", "LRP portrait"),
    ("drawing-20.jpg", "0eecb9_ac78dae59c084f93a9e6dedfecc473e1~mv2.jpg", "LRP portrait"),
    ("drawing-21.jpg", "0eecb9_2be9c4d7f372468ba689f712cc996220~mv2.jpg", "Witchy character design"),
    ("drawing-22.jpg", "0eecb9_a4b50e5032b14a9bb203ecf2bea25b9e~mv2.jpg", "Medieval band"),
    ("drawing-23.jpg", "0eecb9_dc38b55a1ebf4e25bfd299cd36d35c78~mv2.jpg", "Podcast covers"),
    ("drawing-24.jpg", "0eecb9_076bcbeeca184f358c650d45c6cb0db9~mv2.jpg", "Portrait of Tim Minchin"),
    ("drawing-25.jpg", "0eecb9_992436bd99b14de88bb7c900d67f304c~mv2.jpg", "Watercolour sketch"),
]

for filename, media_id, _alt in DRAWING_SPEC:
    ext = media_id.split(".")[-1]
    ASSETS[f"drawing/{filename}"] = (
        f"{WIX}/{media_id}/v1/fill/w_1200,h_1200,q_90/{media_id}"
    )


def download(name: str, url: str) -> None:
    dest = IMG_DIR / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"skip {name}")
        return
    print(f"get  {name}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


if __name__ == "__main__":
    for name, url in ASSETS.items():
        try:
            download(name, url)
        except Exception as exc:
            print(f"FAIL {name}: {exc}")

    manifest = {
        "drawing": [
            {"file": f"assets/images/drawing/{f}", "alt": alt}
            for f, _id, alt in DRAWING_SPEC
        ]
    }
    (ROOT / "assets" / "drawing-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print("done")
