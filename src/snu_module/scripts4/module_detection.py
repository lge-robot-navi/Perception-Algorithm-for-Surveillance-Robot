"""
SNU Integrated Module v2.05
  - Detection (RefineDet)

"""
import os
import copy
import numpy as np
import scipy.misc
import torch
from detection_lib.backbone import RefineDetResNet34
from detection_lib.detector import RefineDet
from detection_lib.postproc import RefineDetPostProc
from detection_lib.framework import OneStageFramework
from detection_lib import util

thermal_camera_params = util.ThermalHeuristicCameraParams()

# import rescue.force_thermal_align_iitp_final_night as rgb_t_align


def load_model(opts, is_default_device=True):
    model_dir = opts.detector.model_dir
    if is_default_device is True:
        device = 0
    else:
        device = opts.detector.device

    backbone_path = os.path.join(model_dir, 'backbone.pth')
    detector_path = os.path.join(model_dir, 'detector.pth')

    backbone = RefineDetResNet34(opts.detector.detection_args, opts.detector.backbone_args)
    detector = RefineDet(opts.detector.detection_args, opts.detector.detector_args)
    backbone.build()
    detector.build()

    backbone.cuda(device)
    detector.cuda(device)
    backbone.load(backbone_path)
    detector.load(detector_path)

    postproc = RefineDetPostProc(opts.detector.detection_args, opts.detector.postproc_args, detector.anchors)
    framework = OneStageFramework(
        opts.detector.detection_args,
        network_dict={'backbone': backbone, 'detector': detector},
        postproc_dict={'detector': postproc})
    return framework


def detect(framework, imgStruct_dict, opts, is_default_device=True):
    if is_default_device is True:
        device = 0
    else:
        device = opts.detector.device

    # rgb.shape: (h, w, 3), rgb.range: [0, 255], img.type: np array
    # thermal.shape: (h, w), thermal.range: [0, 255], thermal.type: np array
    rgb = imgStruct_dict['rgb'].frame.raw
    thermal = imgStruct_dict['thermal'].frame.raw

    # rgb_size = rgb.shape[:2]
    rgb_size = (480, 640)
    input_size = (opts.detector.detection_args['input_h'], opts.detector.detection_args['input_w'])
    if opts.detector.thermal and (thermal is not None):
        img_size = thermal.shape[:2]
        img = torch.from_numpy(scipy.misc.imresize(thermal, size=input_size)).unsqueeze(dim=2)
        img = torch.cat([img, img, img], dim=2)
    else:
        img_size = rgb_size
        img = torch.from_numpy(scipy.misc.imresize(rgb, size=input_size))
    img = img.permute(2, 0, 1).unsqueeze(dim=0).float().cuda(device) / 255.0

    _, result_dict = framework.forward({'img': img}, train=False)
    boxes = result_dict['boxes_l'][0]
    confs = result_dict['confs_l'][0]
    labels = result_dict['labels_l'][0]

    boxes[:, [0, 2]] *= (float(img_size[1]) / float(input_size[1]))
    boxes[:, [1, 3]] *= (float(img_size[0]) / float(input_size[0]))
    # boxes= fbbox.zxs_to_bboxes(boxes, is_torch=True)

    # Copy before Conversion
    thermal_boxes = boxes.cpu().numpy()

    # if opts.detector.thermal and (thermal is not None):
    #     for i in range(len(boxes)):
    #         boxes[i, 0], boxes[i, 1] = util.thermal_coord_to_rgb_coord(
    #             thermal_camera_params, rgb_size, boxes[i, 0], boxes[i, 1])
    #         boxes[i, 2], boxes[i, 3] = util.thermal_coord_to_rgb_coord(
    #             thermal_camera_params, rgb_size, boxes[i, 2], boxes[i, 3])

    # if opts.detector.thermal and (thermal is not None):
    #     for i in range(len(boxes)):
    #         boxes[i, 0], boxes[i, 1] = rgb_t_align.thermal_to_rgb_coord(boxes[i, 0], boxes[i, 1])
    #         boxes[i, 2], boxes[i, 3] = rgb_t_align.thermal_to_rgb_coord(boxes[i, 2], boxes[i, 3])

    boxes = boxes.detach().cpu().numpy()
    confs = confs.detach().cpu().numpy()
    labels = labels.detach().cpu().numpy()
    # boxes.shape: (#boxes, 4), confs.shape: (#boxes, 1), labels.shape: (#boxes, 1)
    det_results = np.concatenate([boxes, confs, labels], axis=1)
    # det_results.shape: (#boxes, 6), [n, 0~3]: xywh, [n, 4]: confidence, [n, 5]: label

    if opts.detector.thermal and (thermal is not None):
        return det_results, thermal_boxes
    else:
        return det_results
