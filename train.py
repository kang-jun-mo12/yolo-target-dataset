"""Train using the dataset beside this script, regardless of working directory."""
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--model',default='yolo11n.pt')
    p.add_argument('--epochs',type=int,default=100)
    p.add_argument('--imgsz',type=int,default=1280)
    p.add_argument('--batch',type=int,default=8)
    p.add_argument('--device',default=None)
    a=p.parse_args()
    from ultralytics import YOLO
    kwargs=dict(data=str(Path(__file__).resolve().with_name('data.yaml')),epochs=a.epochs,imgsz=a.imgsz,batch=a.batch)
    if a.device is not None:kwargs['device']=a.device
    YOLO(a.model).train(**kwargs)

if __name__=='__main__':main()
