#This node focus on showing all the possible information of the qarm, such as:
# - current joint states
# - current end effector pose + rotation [x, y, z, gripper_radians]
# - current camera RGBD data
# - distance/error to the goal pose
# - joint limit status (if any joint is close to its limit)
# - approximated velocity of end effector based on time difference between current and previous pose (delta)
# - State Mode:
#   - Idle: when the arm is not moving and no goal is set
#   - Moving: when the arm is actively moving towards a goal
#   - Error: when there is an error in the arm (e.g., joint limit reached, communication error, etc.)
#   - Goal Reached: when the arm has successfully reached the goal pose within a certain threshold
#   - Manual Control: when the arm is being controlled manually (e.g., via joystick or direct joint commands)
# This node can be used for debugging and monitoring the state of the qarm during operation.
# Made by BP01234-X


# Inputs for when running launch:
#   - goal_pose: [x, y, z, gripper_radians] (default: [0.45, 0.0, 0.5, 0.0])
#   - goal per joints (shoulder, arm, wrist, gripper) (default: [0.0, 0.0, 0.0, 0.0])
#   - LED command (default: [0.0, 0.0, 0.0] for RGB)
#   - Control Mode (pose_goal, joint_goal, manual_control1:keyboard, manual_control2:joystick, speed per time step)
#   - Damping Lambda for control near singularities (default: 0.01) (TODO) SEE HOW TO IMPLEMENT THIS AS A CHANGING PARAMETER



# Actual Jacobian Determinant
# Singularities (when the determinant is zero) Alarm:
#   - Rank(J)
#   - Condition Number of J
#   - Minimum Singular Value of J
#   - Visual Indicator (e.g., LED color change, dashboard warning)
#   - Damped Least Square method lambda for control near singularities (TODO)

