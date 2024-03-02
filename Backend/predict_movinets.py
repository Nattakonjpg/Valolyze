""" Install package Library """

import pandas as pd
import os
import subprocess
import numpy as np

!pip install av

pip install git+https://github.com/Atze00/MoViNet-pytorch.git

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

"""###Install ffmpeg

"""

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import clear_output
!sudo curl -L https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz -o /usr/local/bin/ffmpeg.tar.xz
clear_output()
# %cd /usr/local/bin/
clear_output()
!7z e /usr/local/bin/ffmpeg.tar.xz
clear_output()
!7z e /usr/local/bin/ffmpeg.tar
clear_output()
!sudo chmod a+rx /usr/local/bin/ffmpeg
clear_output()
# %cd /content/
!sudo curl -L https://mkvtoolnix.download/appimage/MKVToolNix_GUI-70.0.0-x86_64.AppImage -o /usr/local/bin/MKVToolNix_GUI-70.0.0-x86_64.AppImage
!sudo chmod u+rx /usr/local/bin/MKVToolNix_GUI-70.0.0-x86_64.AppImage
!sudo ln -s /usr/local/bin/MKVToolNix_GUI-70.0.0-x86_64.AppImage /usr/local/bin/mkvmerge
!sudo chmod a+rx /usr/local/bin/mkvmerge



"""#Load model ก่อน Session Function Predict"""

torch.manual_seed(97)
num_frames = 24 # 16
clip_steps = 12
Bs_Train = 1
Bs_Test = 1

transform_test_A5 = transforms.Compose([
                                 T.ToFloatTensorInZeroOne(),
                                 T.Resize((400, 400)),
                                 #T.Normalize(mean=[0.43216, 0.394666, 0.37645], std=[0.22803, 0.22145, 0.216989]),
                                 T.CenterCrop((320, 320))]) #Size for model

# Cuda , Gpu
loaded_model = MoViNet(_C.MODEL.MoViNetA5, causal=False, pretrained=True)
loaded_model.classifier[3] = torch.nn.Conv3d(2048, 8, (1, 1, 1))
# ระบุ path ของ checkpoint ที่คุณต้องการโหลด
best_checkpoint_path = '/content/drive/MyDrive/A5_yoru+habor_Checkpoint_epoch_round112.pth'
# Load checkpoint
best_checkpoint = torch.load(best_checkpoint_path)
# Load model state dictionary
loaded_model.load_state_dict(best_checkpoint['model_state_dict'])
# ทดสอบโมเดล
loaded_model.eval()

# Cpu
loaded_model = MoViNet(_C.MODEL.MoViNetA5, causal=False, pretrained=True)
loaded_model.classifier[3] = torch.nn.Conv3d(2048, 8, (1, 1, 1))

# Specify the path to the checkpoint file
best_checkpoint_path = '/content/drive/MyDrive/A5_yoru+habor_Checkpoint_epoch_round112.pth'

# Load the checkpoint, specifying map_location to CPU
best_checkpoint = torch.load(best_checkpoint_path, map_location=torch.device('cpu'))

# Load the model's state dictionary
loaded_model.load_state_dict(best_checkpoint['model_state_dict'])

# Set the model to evaluation mode
loaded_model.eval()

"""#Session Function Predict

##Function cut_video, create text
"""

def cut_video(input_file, output_folder, clip_duration, output_csv):
    # Get video duration
    command = ['ffmpeg', '-i', input_file, '-f', 'null', '-']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode('utf-8')

    # Check if output contains duration information
    if 'Duration: ' not in output:
        print("Error: Failed to get video duration.")
        return

    duration_index = output.find('Duration: ') + len('Duration: ')
    duration = output[duration_index:duration_index+11]
    duration = duration.split(':')
    duration = int(duration[0])*3600 + int(duration[1])*60 + int(duration[2].split('.')[0])

    # Calculate number of clips
    num_clips = duration // clip_duration

    # Create output folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    # Create DataFrame to store clip start times
    clip_start_times = []

    # Cut each clip
    for i in range(num_clips):
        start_time = i * clip_duration
        end_time = start_time + clip_duration

        # Generate command line for FFMPEG
        command_line = ['-hide_banner', '-i', input_file, '-map', '0', '-c', 'copy', '-ss',
                        "{:02d}:{:02d}:{:02d}".format(start_time // 3600, (start_time // 60) % 60, start_time % 60),
                        '-to',
                        "{:02d}:{:02d}:{:02d}".format(end_time // 3600, (end_time // 60) % 60, end_time % 60)]

        # Set output file path
        output_file = os.path.join(output_folder, f"video_test_{i+1}.avi")
        command_line += [output_file]

        # Run FFMPEG to cut the video
        subprocess.run(['ffmpeg'] + command_line)

        # Store clip start time
        clip_start_times.append("{:02d}:{:02d}:{:02d}".format(start_time // 3600, (start_time // 60) % 60, start_time % 60))

    # Create DataFrame with clip start times
    df = pd.DataFrame({'clip_start_times': clip_start_times})
    # Save DataFrame to a CSV file
    df.to_csv(output_csv, index=False)

def create_test_split(input_path, output_file_path):
    with open(output_file_path, "w") as f:
        for i, filename in enumerate(os.listdir(input_path), start=1):
            if filename.endswith(".avi"):
                new_filename = f"video_test_{i}.avi 2\n"
                f.write(new_filename)

"""##Predict Function"""

torch.manual_seed(97)
num_frames = 24 # 16
clip_steps = 12
Bs_Test = 1

def prepare_hmdb51_test_loader(data_dir, split_dir, num_frames=24, clip_steps=12, batch_size=1):
    torch.manual_seed(97)
    transform_test_A5 = transforms.Compose([
                                 T.ToFloatTensorInZeroOne(),
                                 T.Resize((400, 400)),
                                 #T.Normalize(mean=[0.43216, 0.394666, 0.37645], std=[0.22803, 0.22145, 0.216989]),
                                 T.CenterCrop((320, 320))]) #Size for model

    hmdb51_test = torchvision.datasets.HMDB51(data_dir, split_dir,
                                              frames_per_clip=num_frames, frame_rate=24,
                                              step_between_clips=num_frames, fold=1,
                                              train=False, transform=transform_test_A5,
                                              num_workers=2)

    test_loader = DataLoader(hmdb51_test, batch_size=Bs_Test, shuffle=False)

    return test_loader

def evaluate_model(loaded_model, test_loader, output_path):
    device = next(loaded_model.parameters()).device
    true_labels, predicted_labels = [], []
    with torch.no_grad():
        for data, _, target in test_loader_A5:
            # Move data and target to the same device as the model
            data, target = data.to(device), target.to(device)

            output = F.log_softmax(loaded_model(data), dim=1)
            _, predicted = torch.max(output, dim=1)

            true_labels.extend(target.cpu().numpy())
            predicted_labels.extend(predicted.cpu().numpy())

    # Create DataFrame from true_labels and predicted_labels
    df_output = pd.DataFrame({'true_label': true_labels, 'predicted_label': predicted_labels})

    # Save DataFrame as a CSV file
    df_output.to_csv(output_path, index=False)

"""##Predict_Final + csv"""

def combine_and_transform_csv(df1_path, df2_path, output_path):
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)

    df_combined = pd.concat([df1, df2], axis=1)
    df_combined = df_combined.reindex(df2.index)
    df_combined.drop(columns=['true_label'], inplace=True)
    df_combined.index += 1

    def get_class_names():
        # สร้างรายชื่อคลาสตามลำดับที่คุณต้องการ
        return ["Buy_Aciton", "Class 0 Aciton", "Dead_Aciton", "Defuse Aciton", "Orb Aciton", "Plant Aciton", "Shoot_Aciton", "Skill_Aciton"]

    # ใช้ฟังก์ชันเพื่อรับชื่อคลาส
    class_names = get_class_names()

    # Assuming 'predicted_label' is the name of the column containing predicted labels
    # Assuming 'class_names' is a list containing the class names
    class_names_dict = {i: class_name for i, class_name in enumerate(class_names)}

    # Add a new column 'predicted_class_names' to df_combined
    df_combined['predicted_class_names'] = df_combined['predicted_label'].map(class_names_dict)

    # เรียกใช้ชื่อคลาสตามตำแหน่งที่ทำนายได้
    for label in df_combined['predicted_label']:
        print(class_names[label])
    df_combined = df_combined.reindex(columns=['clip_start_times', 'predicted_label', 'predicted_class_names'])

    # พิมพ์ DataFrame ที่เกิดขึ้น
    df_combined

    df_combined.to_csv(output_path, index=False)

"""#Use function Here"""

# ระบุ path ของวิดีโอที่ต้องการตัด
inputVideo = "/content/drive/MyDrive/video_data/video แบ่งรอบไม่ตัด/video_data/test_video_fullvideo/Yoru/Pro_Player/DevineFPS_Yoru/รอบ 14.avi"
# ระบุ path ที่ต้องการบันทึกไฟล์ผลลัพธ์
outputFolderVideo = "/content/drive/MyDrive/video_data/video แบ่งรอบไม่ตัด/video_data/test_video_cutvideo/Pro_Player/DevineFPS_Yoru/รอบ 14/test"
# ระบุความยาวของคลิปวิดีโอที่ต้องการตัด (วินาที)
clipDuration = 2
# ระบุ path ที่ต้องการบันทึกไฟล์ CSV
output_csv = "/content/drive/MyDrive/Csv file/time/DevineFPS_Yoru/Round14.csv"

# เรียกใช้ฟังก์ชันเพื่อตัดวิดีโอ
cut_video(inputVideo, outputFolderVideo, clipDuration, output_csv)
df = pd.read_csv(output_csv)
len(df)

# เรียกใช้งาน function
#outputFolderVideo = มาจาก video ตัดซอย 2 วิแล้วใช้ folder เดียวกัน
output_file_text = "/content/drive/MyDrive/test_train_splits/DevineFPS_Yoru/รอบ 14/test_test_split1.txt"

create_test_split(outputFolderVideo, output_file_text)

data_dir =  "/content/drive/MyDrive/video_data/video แบ่งรอบไม่ตัด/video_data/test_video_cutvideo/Pro_Player/DevineFPS_Yoru/รอบ 14/"
split_dir =   "/content/drive/MyDrive/test_train_splits/DevineFPS_Yoru/รอบ 14/"
test_loader_A5 = prepare_hmdb51_test_loader(data_dir, split_dir)
print(test_loader_A5.dataset)

# ระบุเส้นทางที่จะบันทึกผลลัพธ์
output_path = "/content/drive/MyDrive/Csv file/Predict/DevineFPS_Yoru/Round14.csv"
# เรียกใช้ฟังก์ชัน
evaluate_model(loaded_model, test_loader_A5, output_path)

path1 = "/content/drive/MyDrive/Csv file/Predict/DevineFPS_Yoru/Round14.csv"
path2 = "/content/drive/MyDrive/Csv file/time/DevineFPS_Yoru/Round14.csv"
path3 = "/content/drive/MyDrive/Csv file/File.csv for Yoru_video_round/Pro_player/DevineFPS_Yoru/Predict+time_Round_14.csv"
combine_and_transform_csv(path1, path2, path3)

