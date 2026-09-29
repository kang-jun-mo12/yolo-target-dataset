# YOLO26m 1920 target detector

분홍색 `enemy`와 파란색 `ally` 타겟을 검출하도록 미세 조정한 Ultralytics YOLO26m 모델입니다.

## 파일

- `best.pt`: validation mAP50-95가 가장 높았던 epoch의 가중치
- `split_manifest.csv`: 각 이미지가 train, val, test 중 어디에 사용됐는지 기록
- `split_summary.json`: 분할별 이미지와 클래스 박스 수

가중치는 Git LFS로 관리합니다. 저장소를 받은 후 포인터 파일만 보이면 `git lfs pull`을 실행하세요.

## 학습 설정

| 항목 | 값 |
|---|---:|
| Base weights | `yolo26m.pt` |
| Ultralytics | 8.4.165 |
| PyTorch | 2.11.0+cu128 |
| Epochs | 100 |
| Input | 1920 |
| Batch | 1 |
| Rectangular batches | true |
| AMP | true |
| Optimizer | auto |
| Seed | 0 |
| GPU | NVIDIA GeForce RTX 5070 Ti 16 GB |

분할은 총 577장 중 train 519장, validation 29장, test 29장입니다. 각 촬영 묶음 안에서 연속된 구간을 validation과 test로 보관했습니다.

## 성능

`best.pt`는 epoch 76에서 validation mAP50-95 0.91057을 기록했습니다.

| Test 29장 | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| 전체 | 0.998 | 1.000 | 0.995 | 0.935 |
| enemy | 0.997 | 1.000 | 0.995 | 0.958 |
| ally | 0.998 | 1.000 | 0.995 | 0.912 |

테스트 세트에는 enemy 27개와 ally 29개가 있습니다. 테스트 이미지는 학습과 검증에서 제외했지만 동일한 촬영 환경에서 가져왔으므로, 새로운 장소와 카메라에 대한 성능은 별도로 평가해야 합니다.

## 사용

```python
from ultralytics import YOLO

model = YOLO("models/yolo26m_1920_90_5_5/best.pt")
results = model.predict("image.png", imgsz=1920, conf=0.25)
```

```sh
python prepare_split_90_5_5.py
yolo detect val model=models/yolo26m_1920_90_5_5/best.pt data=dataset_90_5_5/data.yaml split=test imgsz=1920 batch=1
```
