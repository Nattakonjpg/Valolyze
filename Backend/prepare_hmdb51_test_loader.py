import torch
import torchvision
import torchvision.transforms as transforms
import transforms as T
from torch.utils.data import random_split, DataLoader
Bs_Test = 1


def prepare_hmdb51_test_loader(data_dir, split_dir, num_frames=24, clip_steps=12, batch_size=1):
    torch.manual_seed(97)
    transform_test_A5 = transforms.Compose([
        T.ToFloatTensorInZeroOne(),
        T.Resize((400, 400)),
        # T.Normalize(mean=[0.43216, 0.394666, 0.37645], std=[0.22803, 0.22145, 0.216989]),
        T.CenterCrop((320, 320))])  # Size for model

    hmdb51_test = torchvision.datasets.HMDB51(data_dir, split_dir,
                                              frames_per_clip=num_frames, frame_rate=24,
                                              step_between_clips=num_frames, fold=1,
                                              train=False, transform=transform_test_A5,
                                              num_workers=0)

    test_loader = DataLoader(hmdb51_test, batch_size=Bs_Test, shuffle=False)

    return test_loader
