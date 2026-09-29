"""Create a reproducible 90/5/5 YOLO split without changing the source data."""

import csv
import json
import os
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEST = ROOT / "dataset_90_5_5"


def allocate(groups, total):
    """Apportion a target count by group size using largest remainders."""
    count = sum(map(len, groups.values()))
    quotas = {name: len(rows) * total / count for name, rows in groups.items()}
    allocated = {name: int(quota) for name, quota in quotas.items()}
    remaining = total - sum(allocated.values())
    order = sorted(groups, key=lambda name: (-(quotas[name] - allocated[name]), name))
    for name in order[:remaining]:
        allocated[name] += 1
    return allocated


def main():
    with (ROOT / "manifest.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 577
    groups = defaultdict(list)
    for row in rows:
        group = row["source"].split("/")[0] if "/" in row["source"] else "camera"
        groups[group].append(row)

    val_count = allocate(groups, 29)
    test_count = allocate(groups, 29)
    assignment = {}
    for group, items in groups.items():
        items.sort(key=lambda row: int(row["photo_number"]))
        n = len(items)
        val_start = n // 4 - val_count[group] // 2
        test_start = 3 * n // 4 - test_count[group] // 2
        val_indices = set(range(val_start, val_start + val_count[group]))
        test_indices = set(range(test_start, test_start + test_count[group]))
        assert not val_indices & test_indices
        for index, row in enumerate(items):
            split = "val" if index in val_indices else "test" if index in test_indices else "train"
            assignment[row["photo_number"]] = split

    assert not DEST.exists(), f"Output already exists: {DEST}"
    split_rows = []
    counts = Counter()
    boxes = Counter()
    for row in rows:
        split = assignment[row["photo_number"]]
        image = ROOT / row["image"]
        label = ROOT / row["label"]
        image_dest = DEST / "images" / split / image.name
        label_dest = DEST / "labels" / split / label.name
        image_dest.parent.mkdir(parents=True, exist_ok=True)
        label_dest.parent.mkdir(parents=True, exist_ok=True)
        os.link(image, image_dest)
        os.link(label, label_dest)
        split_rows.append({**row, "original_split": row["split"], "split": split,
                           "image": image_dest.relative_to(DEST).as_posix(),
                           "label": label_dest.relative_to(DEST).as_posix()})
        counts[split] += 1
        for line in label.read_text(encoding="utf-8").splitlines():
            boxes[(split, int(line.split()[0]))] += 1

    assert counts == {"train": 519, "val": 29, "test": 29}, counts
    assert all(boxes[(split, cls)] > 0 for split in counts for cls in (0, 1))
    (DEST / "data.yaml").write_text(
        f"path: {DEST.as_posix()}\ntrain: images/train\nval: images/val\ntest: images/test\n"
        "names:\n  0: enemy\n  1: ally\n", encoding="utf-8")
    with (DEST / "split_manifest.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=split_rows[0].keys())
        writer.writeheader()
        writer.writerows(split_rows)
    summary = {"images": dict(counts),
               "boxes": {split: {str(cls): boxes[(split, cls)] for cls in (0, 1)} for split in counts},
               "method": "contiguous held-out blocks within each capture group"}
    (DEST / "split_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
