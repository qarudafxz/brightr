#libraries for learning with deep lab v3
from tqdm import tqdm
import numpy as np
import utils
import os 
import random 
import argparse 

from torch.utils import data
import torch 
import torch.nn as nn
from utils.visualizer import Visualizer
from utils import ext_transforms as et

from models.deeplabv3 import DeepLabV3

def parser():
  parser = argparse.ArgumentParser(description='DeepLabV3')
  
  parser.add_argument('--batch_size', type=int, default=1, help='batch size')
  parser.add_argument('--epochs', type=int, default=100, help='number of epochs')
  
  parser.add_argument('--lr', type=float, default=0.0001, help='learning rate')
  
  parser.add_argument('--momentum', type=float, default=0.9, help='momentum')
 
  parser.add_argument('--weight_decay', type=float, default=0.0005, help='weight decay')
  
  parser.add_argument('--num_classes', type=int, default=21, help='number of classes')
  
  parser.add_argument('--backbone', type=str, default='resnet', help='backbone name (default: resnet)')
  
  parser.add_argument('--sync_bn', type=bool, default=None, help='whether to use sync bn (default: auto)')
  
  parser.add_argument('--freeze_bn', type=bool, default=False, help='whether to freeze bn parameters (default: False)')
  
  parser.add_argument('--cuda', type=bool, default=True, help='whether to use cuda if available')

  available_models = sorted(name for name in network.modeling.__dict__ if name.islower() and not name.startswith("__") and callable(network.modeling.__dict__[name]))
  
  parser.add_argument('--model', type=str, default='deeplabv3', help='model name (default: deeplabv3)')
  
  parser.add_argument('--aux_loss', type=bool, default=None, help='Auxilary loss')
  
  parser.add_argument('--visualize', type=bool, default=False, help='Visualize the training process')
  
  parser.add_argument('--save_cp', type=bool, default=False, help='Save checkpoint')
  
  parser.add_argument('--gpu_id', type=int, default=0, help='gpu id for evaluation')
  
  parser.add_argument('--checkname', type=str, default=None, help='set the checkpoint name')
  
  parser.add_argument('--eval_interval', type=int, default=1, help='evaluation interval (default: 1)')
  
  parser.add_argument('--dataset', type=str, default='pascal', choices=['pascal', 'coco', 'cityscapes'], help='dataset name (default: pascal)')
  
  parser.add_argument('--base_size', type=int, default=513, help='base image size')
  
def retrieve_dataset(args):
 if args.dataset == 'cityscapes':
   train_transform = et.ExtCompose([
      et.ExtResize(args.base_size),
      et.ExtRandomCrop(args.crop_size),
      et.ExtRandomHorizontalFlip(),
      et.ExtToTensor(),
      et.ExtNormalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
      ])
   val_transform = et.ExtCompose([
      et.ExtResize(args.base_size),
      et.ExtCenterCrop(args.crop_size),
      et.ExtToTensor(),
      et.ExtNormalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
      ])
   train_set = cityscapes.CityscapesSegmentation(args, split='train', transform=train_transform)
   val_set = cityscapes.CityscapesSegmentation(args, split='val', transform=val_transform)
   test_set = cityscapes.CityscapesSegmentation(args, split='test', transform=val_transform)
   
    
  