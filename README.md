# YOLO 타겟 학습 데이터셋

분홍색/파란색 타겟을 받침대까지 감싸는 바운딩 박스 데이터셋입니다. 2026-09-29 서버 라벨 버전 102를 기준으로 확정했습니다.

| 구분 | 이미지 | enemy (분홍색) | ally (파란색) |
|---|---:|---:|---:|
| 학습 | 409 | 409 | 407 |
| 검증 | 168 | 163 | 168 |
| 합계 | 577 | 572 | 575 |

- 클래스: `0 enemy`, `1 ally`. 총 박스 1,147개.
- 원본 1920×1080 PNG를 그대로 보존합니다. 이미지 용량은 약 1.40 GB이며 Git LFS로 관리합니다.
- 웹 편집기의 **사진 번호 42, 49**를 제외했습니다. 각각 원래 파일 인덱스 41, 48입니다. 파일명 앞 숫자는 기존 0부터 시작하는 인덱스이며 재번호를 매기지 않았습니다.
- 학습/검증 분할은 기존 촬영 그룹 기준을 유지합니다. 동일 PNG가 두 분할에 중복되지 않는 것을 검증했습니다.
- 같은 장소/타겟을 촬영했으므로 새 장소에 대한 성능은 별도 테스트 데이터로 평가하세요. 독립적인 테스트 세트는 포함하지 않습니다.
- 이 저장소는 확정 시점의 복사본입니다. 이후 웹 편집 사항이 자동으로 이 저장소에 반영되지는 않습니다.

## 내려받기

Git LFS를 설치한 환경에서 저장소를 `git clone`한 뒤 저장소 폴더에서 다음을 실행하세요.

```sh
git lfs install
git lfs pull
python validate_dataset.py
```

## 학습

Ultralytics를 설치한 Python 환경에서 실행합니다. `train.py`는 실행 위치와 무관하게 이 폴더의 절대 경로로 `data.yaml`을 전달합니다.

```sh
pip install ultralytics
python train.py --model yolo11n.pt --epochs 100 --imgsz 1280 --batch 8
```

학습 예시이며 모델 학습은 아직 수행하지 않았습니다. GPU 메모리에 맞춰 batch와 이미지 크기를 조절하세요.

## 파일 구성

- `images/train`, `images/val`: 원본 PNG.
- `labels/train`, `labels/val`: 대응하는 YOLO TXT. 각 줄은 `class_id center_x center_y width height`이며 좌표는 0~1로 정규화합니다.
- `data.yaml`, `classes.txt`: 학습 설정과 클래스 이름.
- `manifest.csv`: 웹 사진 번호, 기존 인덱스, 원본 상대 경로, 파일 대응, SHA-256, 서버 수정 버전.
- `annotations.json`: 최종 픽셀 좌표와 서버 저장 시각.
- `excluded.json`: 제외한 사진과 사유.
- `summary.json`, `validation.json`: 수량과 제작 시 검증 결과.

이미지의 라벨 대상은 두 색상 타겟입니다. 사람은 라벨 대상이 아닙니다. 타겟은 판·기둥·받침대를 포함하고, 가려진 경우 확인되는 부분을 감쌉니다.
