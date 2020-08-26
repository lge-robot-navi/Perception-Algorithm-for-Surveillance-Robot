"""
SNU Integrated Module v5.0
    - Configuration File for Outdoor Surveillance Robots


"""
# Import Module
import os

# Import Config Module
from yacs.config import CfgNode as CN

# Get NN Model Base Path
model_base_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "models"
)

# Config Class Initialization
__C = CN(new_allowed=False)

# Data Environment
# (for [static/dynamic] robots, it is literal)
# (for ROS Bag Files, describe the bag file's image sequence environment)
__C.env = CN(new_allowed=True)
__C.env.type = "NULL"
__C.env.name = "NULL"

# Screen Compensate Flag
__C.screen_compensate = True

# ROS Odometry Message
__C.odometry_rostopic_name = "/robot_odom"

# --------------------- #
# ROS Publisher Options #
# --------------------- #
__C.publisher = CN(new_allowed=False)
__C.publisher.tracks = "/osr/tracks"

# ------------------ #
# ROS Sensor Options #
# ------------------ #

# ROS Sensor Option Initialization
__C.sensors = CN(new_allowed=False)

# ROS Sensors Initialization
__C.sensors.color = CN(new_allowed=True)
__C.sensors.color.is_valid = True
__C.sensors.color.encoding = "8UC3"
__C.sensors.color.rostopic_name = "/osr/image_color"
__C.sensors.color.camerainfo_rostopic_name = "/osr/image_color_camerainfo"


__C.sensors.disparity = CN(new_allowed=True)
__C.sensors.disparity.is_valid = True
__C.sensors.disparity.encoding = "16UC1"
__C.sensors.disparity.rostopic_name = "/osr/image_aligned_depth"
__C.sensors.disparity.camerainfo_rostopic_name = "/osr/image_depth_camerainfo"

__C.sensors.disparity.clip = CN(new_allowed=False)
__C.sensors.disparity.clip.value = -1
__C.sensors.disparity.clip.min_distance = 1000
__C.sensors.disparity.clip.max_distance = 15000


__C.sensors.thermal = CN(new_allowed=True)
__C.sensors.thermal.is_valid = True
__C.sensors.thermal.encoding = "16UC1"
__C.sensors.thermal.rostopic_name = "/osr/image_thermal"
__C.sensors.thermal.camerainfo_rostopic_name = "NULL"


__C.sensors.infrared = CN(new_allowed=True)
__C.sensors.infrared.is_valid = True
__C.sensors.infrared.encoding = "8UC1"
__C.sensors.infrared.rostopic_name = "/osr/image_ir"


__C.sensors.nightvision = CN(new_allowed=True)
__C.sensors.nightvision.is_valid = True
__C.sensors.nightvision.encoding = "8UC3"
__C.sensors.nightvision.rostopic_name = "/osr/image_nv1"
__C.sensors.nightvision.camerainfo_rostopic_name = "NULL"


__C.sensors.lidar = CN(new_allowed=True)
__C.sensors.lidar.is_valid = True
__C.sensors.lidar.encoding = "NULL"
__C.sensors.lidar.rostopic_name = "/osr/lidar_pointcloud"
__C.sensors.lidar.camerainfo_rostopic_name = "NULL"

# ---------------- #
# Detector Options #
# ---------------- #
# TODO: Add options/parameters that can be easily modified while impacting the overall performance
__C.detector = CN(new_allowed=True)
__C.detector.name = "YOLOv4"#"RefineDet"
__C.detector.device = 0
__C.detector.model_base_path = os.path.join(model_base_path, "detector")

__C.detector.visualization = CN(new_allowed=True)
__C.detector.visualization.is_draw = True
__C.detector.visualization.is_show = True
__C.detector.visualization.auto_save = False
__C.detector.visualization.bbox_color = (255, 0, 0)

__C.detector.visualization.is_result_publish = False
__C.detector.visualization.result_rostopic_name = "/osr/snu_det_result_image"

# ------------------------------- #
# Multiple Target Tracker Options #
# ------------------------------- #
# TODO: Add options/parameters that can be easily modified while impacting the overall performance
__C.tracker = CN(new_allowed=True)
__C.tracker.name = "Custom"
__C.tracker.device = 0

__C.tracker.association = CN(new_allowed=True)

__C.tracker.association.trk = CN(new_allowed=True)
__C.tracker.association.trk.init_age = 3
__C.tracker.association.trk.destroy_age = 3
__C.tracker.association.trk.similarity_thresh = 0.1

__C.tracker.association.trk.similarity_weights = CN(new_allowed=True)
__C.tracker.association.trk.similarity_weights.histogram = 1.0 / 3.0
__C.tracker.association.trk.similarity_weights.iou = 1.0 / 3.0
__C.tracker.association.trk.similarity_weights.distance = 1.0 / 3.0

__C.tracker.association.trk_cand = CN(new_allowed=True)
__C.tracker.association.trk_cand.destroy_age = 3
__C.tracker.association.trk_cand.similarity_thresh = 0.6

__C.tracker.association.trk_cand.similarity_weights = CN(new_allowed=True)
__C.tracker.association.trk_cand.similarity_weights.iou = 1.0 / 2.0
__C.tracker.association.trk_cand.similarity_weights.distance = 1.0 / 2.0

__C.tracker.visualization = CN(new_allowed=True)
__C.tracker.visualization.is_draw = True
__C.tracker.visualization.is_show = True
__C.tracker.visualization.auto_save = False

__C.tracker.visualization.is_result_publish = True
__C.tracker.visualization.result_rostopic_name = "/osr/snu_trk_acl_result_image"

__C.tracker.visualization.top_view = CN(new_allowed=True)
__C.tracker.visualization.top_view.is_draw = False
__C.tracker.visualization.top_view.is_show = False
__C.tracker.visualization.top_view.map_size = (20000, 20000)
__C.tracker.visualization.top_view.trk_radius = 100

__C.tracker.visualization.top_view.is_result_publish = False
__C.tracker.visualization.top_view.result_rostopic_name = "/osr/trk_top_view_image"

# ----------------------------- #
# Action Classification Options #
# ----------------------------- #
# TODO: Add options/parameters that can be easily modified while impacting the overall performance
__C.aclassifier = CN(new_allowed=True)
__C.aclassifier.name = "Custom"
__C.aclassifier.device = 0
__C.aclassifier.model_base_path = os.path.join(model_base_path, "aclassifier")

# NOTE: For Action Classification, publishing result frame is done simultaneously with MOT result
__C.aclassifier.visualization = CN(new_allowed=True)
__C.aclassifier.visualization.is_draw = True
__C.aclassifier.visualization.is_show = True


if __name__ == "__main__":
    pass
