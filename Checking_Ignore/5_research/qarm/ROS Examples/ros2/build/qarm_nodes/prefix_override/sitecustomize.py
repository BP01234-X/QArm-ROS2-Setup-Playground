import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/quanser/Documents/Quanser_Academic_Resources/5_research/qarm/ROS Examples/ros2/install/qarm_nodes'
