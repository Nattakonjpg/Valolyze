import pandas as pd
import os
import subprocess
import numpy as np
import av
import time
import torchvision
import torch.nn.functional as F
import torchvision.transforms as transforms
import torch.optim as optim
from torch.utils.data import random_split, DataLoader
import torch
import transforms as T
from movinets import MoViNet
from movinets.config import _C

from flask import Flask, request

# Import function from function file
from cut_video import cut_video
from create_test_split import create_test_split
from prepare_hmdb51_test_loader import prepare_hmdb51_test_loader
from evaluate_model import evaluate_model
from combine_and_transform_csv import combine_and_transform_csv

app = Flask(__name__)

torch.manual_seed(97)
num_frames = 24  # 16
clip_steps = 12
Bs_Test = 1

def load_model(selected_model_path):
    # โค้ดโหลดโมเดลของคุณ
    loaded_model = MoViNet(_C.MODEL.MoViNetA5, causal=False, pretrained=True)
    loaded_model.classifier[3] = torch.nn.Conv3d(2048, 8, (1, 1, 1))
    best_checkpoint_path = selected_model_path  # กำหนด path ของโมเดลตามที่ผู้ใช้เลือก
    best_checkpoint = torch.load(best_checkpoint_path, map_location=torch.device('cpu'))
    loaded_model.load_state_dict(best_checkpoint['model_state_dict'])
    loaded_model.eval()
    return loaded_model

@app.route('/load-model', methods=['POST'])
def load_selected_model():
    selected_model_path = request.json['selectedModelPath']
    try:
        loaded_model = load_model(selected_model_path)
        return 'Model loaded successfully!', 200
    except Exception as e:
        return f'Failed to load model. Error: {str(e)}', 500

if __name__ == '__main__':
    # ระบุ path ของวิดีโอที่ต้องการตัด
    inputVideo = r"/home/nattakonpu/codes/Valolyze/Backend/video_data/test_videofull/agent/round/รอบ 1.avi"
    # ระบุ path ที่ต้องการบันทึกไฟล์ผลลัพธ์
    outputFolderVideo = r"/home/nattakonpu/codes/Valolyze/Backend/video_data/test_cutvideo/agent/round/test/"
    # ระบุความยาวของคลิปวิดีโอที่ต้องการตัด (วินาที)
    clipDuration = 2
    # ระบุ path ที่ต้องการบันทึกไฟล์ CSV
    output_csv = r"/home/nattakonpu/codes/Valolyze/Backend/Output/Time/agent/round1.csv"

    cut_video(inputVideo, outputFolderVideo, clipDuration, output_csv)
    df = pd.read_csv(output_csv)
    print(df.tail())

    # เรียกใช้งาน function
    # outputFolderVideo = มาจาก video ตัดซอย 2 วิแล้วใช้ folder เดียวกัน
    output_file_text = r"/home/nattakonpu/codes/Valolyze/Backend/test_train_splits/agent/round/test_test_split1.txt"

    create_test_split(outputFolderVideo, output_file_text)

    data_dir = r"/home/nattakonpu/codes/Valolyze/Backend/video_data/test_cutvideo/agent/round/"
    split_dir = r"/home/nattakonpu/codes/Valolyze/Backend/test_train_splits/agent/round/"
    test_loader_A5 = prepare_hmdb51_test_loader(data_dir, split_dir)
    print(test_loader_A5.dataset)

    # ระบุเส้นทางที่จะบันทึกผลลัพธ์
    output_path = r"/home/nattakonpu/codes/Valolyze/Backend/Output/Predict/agent/Round1.csv"
    # เรียกใช้ฟังก์ชัน
    evaluate_model(loaded_model, test_loader_A5, output_path)

    path1 = output_path
    path2 = output_csv
    path3 = r"/home/nattakonpu/codes/Valolyze/Backend/Output/Final/FinalPredict+time_Round_1.csv"
    combine_and_transform_csv(path1, path2, path3)
