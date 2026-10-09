# YOLO26l OBB — 1920×1088 target detector

분홍색 `enemy`와 파란색 `ally` 타겟의 위치·크기·회전각을 예측하는 YOLO26l OBB 모델입니다. 라벨은 물체 전체와 나무 받침대를 포함합니다.

실제 촬영 이미지 1,856장과 증강 이미지 1,000장을 합쳐 학습했으며, 추론용 가중치는 **[best.pt](best.pt)**입니다. 기존 YOLO26m 일반 박스 모델과 별도로 제공합니다.

## 다운로드와 실행

가중치는 Git LFS로 관리합니다. 저장소 루트에서 아래 명령으로 이 모델만 내려받을 수 있습니다.

```sh
git lfs pull --include="models/yolo26l_obb_1920x1088/best.pt"
pip install ultralytics==8.4.165
```

```python
from ultralytics import YOLO

model = YOLO("models/yolo26l_obb_1920x1088/best.pt", task="obb")
results = model.predict("image.png", imgsz=1920, rect=True, conf=0.25, save=True)

# 원본 이미지 좌표계의 회전 박스: 중심 x, 중심 y, 폭, 높이, 회전각(rad)
print(results[0].obb.xywhr.cpu().numpy())
# 원본 이미지 좌표계의 네 꼭짓점: (물체 수, 4, 2)
print(results[0].obb.xyxyxyxy.cpu().numpy())
```

```sh
yolo obb predict model=models/yolo26l_obb_1920x1088/best.pt source=image.png imgsz=1920 rect=True conf=0.25 save=True
```

원본이 1920×1080인 단일 이미지의 최소 패딩 입력은 가로 1920×세로 1088입니다. `xywhr`의 폭·높이는 회전 박스의 두 변 길이이며, 화면의 수평·수직 방향 외접 박스 크기와는 다릅니다. GPU 추론에는 해당 환경에 맞는 CUDA 지원 PyTorch가 필요합니다.

## 학습 설정

| 항목 | 값 |
|---|---|
| 모델 | YOLO26l OBB, `yolo26l-obb.pt`에서 미세 조정 |
| 클래스 | `0: enemy`(분홍), `1: ally`(파랑) |
| Ultralytics / PyTorch | 8.4.165 / 2.11.0+cu128 |
| 학습 입력 | 가로 1920 × 세로 1088, `imgsz=1920`, `rect=True` |
| 원본 이미지 | 1920×1080, 원본 보존 |
| Batch / AMP / Seed | 1 / true / 42 |
| GPU | NVIDIA GeForce RTX 5070 Ti |
| 계획 / 실제 학습 | 최대 100 / 63 epochs |
| 조기 종료 | 30 epochs 동안 검증 성능 개선 없음 |
| 선택된 모델 | epoch 33의 `best.pt` |
| 학습 시간 | 로그 기준 5.057시간 |

학습 데이터는 총 2,856장으로, train 2,560장 / validation 296장입니다. 증강 이미지 1,000장은 모두 train에만 포함하고 validation은 실제 사진으로 구성했습니다. 학습 라벨에는 제외 요청된 신규 사진 9장이 들어 있지 않습니다.

이 모델이 사용한 OBB 학습 세트는 저장소 루트에 있는 기존 577장 일반 박스 데이터셋과 다릅니다. 이번 모델 폴더에는 가중치와 학습 기록만 포함하며, 전체 OBB 학습 이미지·라벨은 포함하지 않습니다. `train_config.yaml`은 기록용 설정이며 재학습에는 해당 OBB 데이터셋이 필요합니다.

## 검증 성능

모델 선택에 사용한 epoch 33의 `results.csv` 기록입니다.

| Validation 296장 / 587개 물체 | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|
| 전체 | 0.99978 | 1.00000 | 0.99500 | 0.96424 |

학습 종료 후 저장된 `best.pt`의 최종 재검증 로그는 반올림된 값으로 mAP50 0.995, mAP50–95 0.962를 기록했습니다. 기본 validation 로더의 입력은 가로 1952×세로 1120입니다.

이 수치는 같은 촬영 환경의 validation 결과이며 별도 독립 test 세트는 사용하지 않았습니다. mAP는 검출 성능 지표로, 박스 변 길이의 픽셀 오차를 직접 의미하지 않습니다.

![Training and validation curves](results.png)

## 파일

- `best.pt`: 검증 성능으로 선택한 추론용 가중치. 학습 종료 후 optimizer가 제거된 파일입니다.
- `best.pt.sha256`: 가중치 무결성 확인용 SHA-256.
- `model_info.json`: 클래스, 학습 설정, 데이터 수량, 검증 수치와 모델 해시.
- `train_config.yaml`: 사용한 주요 학습 설정.
- `results.csv`, `results.png`: 완료된 63 epochs의 학습·검증 기록.

가중치 SHA-256: `740bdb55a134f425bffc086fc446c9b6c59a98df97349767bd81aec59ffaf6a0`
