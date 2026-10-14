# Point-LIO evaluation on Go2 with Unitree L2

Build from `source/unitree_mujoco/ros2_ws`:

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select point_lio_unilidar
source install/setup.bash
```

Start the existing sensor publishers (for example, the existing FAST-LIO launch), then run:

```bash
ros2 launch point_lio_unilidar point_lio.launch.py
```

Point-LIO consumes `/utlidar/time_corrected/cloud` and `/imu/data_fastlio` and publishes `/pointlio/odom`, `/pointlio/path`, `/pointlio/cloud_registered`, and `/pointlio/cloud_registered_body` continuously. `/pointlio/laser_map` contains only the initial map, is published once, and is retained for late subscribers. Its TF is `camera_init_correct -> pointlio_init -> pointlio_body`; the first link is identity for visualization only. It does not supply any downstream navigation or control pose. The cloud's `time` field must be seconds relative to its start stamp. The launch computes lidar-to-IMU extrinsics using the same geometry helper as FAST-LIO. PCD saving and runtime pose logs are disabled. Stop the Point-LIO launch to remove its TF and outputs without affecting FAST-LIO.

The Go2 profile uses a 200 m local map cube with `mapping.det_range: 30.0`. Keep `cube_side_length > 3 * det_range`; the original L2 profile used 100 m with the 200 m cube, causing Point-LIO to shift its local map every scan and its pose to diverge.
