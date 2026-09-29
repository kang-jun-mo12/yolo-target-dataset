"""Check all downloaded PNG hashes, exclusions, split membership and YOLO labels."""
import csv
import hashlib
import json
from pathlib import Path

def main():
    root=Path(__file__).resolve().parent
    with (root/'manifest.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    annotations={r['photo_number']:r for r in json.loads((root/'annotations.json').read_text(encoding='utf-8'))}
    assert len(rows)==577 and len(annotations)==577
    assert not {42,49}&{int(r['photo_number']) for r in rows}
    assert {p.relative_to(root).as_posix() for p in (root/'images').rglob('*.png')}=={r['image'] for r in rows}
    assert {p.relative_to(root).as_posix() for p in (root/'labels').rglob('*.txt')}=={r['label'] for r in rows}
    seen={};boxes=0
    for row in rows:
        image=root/row['image'];label=root/row['label'];payload=image.read_bytes()
        assert payload[:8]==b'\x89PNG\r\n\x1a\n',f'Not a PNG; run git lfs pull: {image}'
        digest=hashlib.sha256(payload).hexdigest();assert digest==row['image_sha256'],image
        assert digest not in seen or seen[digest]==row['split'],'Cross-split duplicate'
        seen[digest]=row['split']
        lines=label.read_text(encoding='utf-8').splitlines()
        expected=annotations[int(row['photo_number'])]['boxes']
        assert len(lines)==int(row['objects'])==len(expected)
        for line,b in zip(lines,expected):
            parts=line.split();assert len(parts)==5
            cls=int(parts[0]);cx,cy,w,h=map(float,parts[1:])
            assert cls in (0,1) and 0<w<=1 and 0<h<=1
            assert cx-w/2>=-1e-7 and cx+w/2<=1+1e-7 and cy-h/2>=-1e-7 and cy+h/2<=1+1e-7
            x,y,x2,y2=b['box'];coords=((x+x2)/3840,(y+y2)/2160,(x2-x)/1920,(y2-y)/1080)
            assert cls==b['cls'] and all(abs(a-c)<1e-7 for a,c in zip((cx,cy,w,h),coords))
            boxes+=1
    assert boxes==1147
    print(f'PASS: {len(rows)} images, {boxes} boxes; excluded photos 42 and 49 absent.')

if __name__=='__main__':main()
