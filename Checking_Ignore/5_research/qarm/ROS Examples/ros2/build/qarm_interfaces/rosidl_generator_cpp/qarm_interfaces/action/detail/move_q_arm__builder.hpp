// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from qarm_interfaces:action/MoveQArm.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/action/move_q_arm.hpp"


#ifndef QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__BUILDER_HPP_
#define QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_Goal_task_space_pose
{
public:
  Init_MoveQArm_Goal_task_space_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::qarm_interfaces::action::MoveQArm_Goal task_space_pose(::qarm_interfaces::action::MoveQArm_Goal::_task_space_pose_type arg)
  {
    msg_.task_space_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_Goal>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_Goal_task_space_pose();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_Result_message
{
public:
  explicit Init_MoveQArm_Result_message(::qarm_interfaces::action::MoveQArm_Result & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_Result message(::qarm_interfaces::action::MoveQArm_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_Result msg_;
};

class Init_MoveQArm_Result_success
{
public:
  Init_MoveQArm_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_Result_message success(::qarm_interfaces::action::MoveQArm_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveQArm_Result_message(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_Result>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_Result_success();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_Feedback_orientation_error
{
public:
  explicit Init_MoveQArm_Feedback_orientation_error(::qarm_interfaces::action::MoveQArm_Feedback & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_Feedback orientation_error(::qarm_interfaces::action::MoveQArm_Feedback::_orientation_error_type arg)
  {
    msg_.orientation_error = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_Feedback msg_;
};

class Init_MoveQArm_Feedback_position_error_norm
{
public:
  Init_MoveQArm_Feedback_position_error_norm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_Feedback_orientation_error position_error_norm(::qarm_interfaces::action::MoveQArm_Feedback::_position_error_norm_type arg)
  {
    msg_.position_error_norm = std::move(arg);
    return Init_MoveQArm_Feedback_orientation_error(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_Feedback>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_Feedback_position_error_norm();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_SendGoal_Request_goal
{
public:
  explicit Init_MoveQArm_SendGoal_Request_goal(::qarm_interfaces::action::MoveQArm_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_SendGoal_Request goal(::qarm_interfaces::action::MoveQArm_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Request msg_;
};

class Init_MoveQArm_SendGoal_Request_goal_id
{
public:
  Init_MoveQArm_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_SendGoal_Request_goal goal_id(::qarm_interfaces::action::MoveQArm_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MoveQArm_SendGoal_Request_goal(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_SendGoal_Request>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_SendGoal_Request_goal_id();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_SendGoal_Response_stamp
{
public:
  explicit Init_MoveQArm_SendGoal_Response_stamp(::qarm_interfaces::action::MoveQArm_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_SendGoal_Response stamp(::qarm_interfaces::action::MoveQArm_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Response msg_;
};

class Init_MoveQArm_SendGoal_Response_accepted
{
public:
  Init_MoveQArm_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_SendGoal_Response_stamp accepted(::qarm_interfaces::action::MoveQArm_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_MoveQArm_SendGoal_Response_stamp(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_SendGoal_Response>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_SendGoal_Response_accepted();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_SendGoal_Event_response
{
public:
  explicit Init_MoveQArm_SendGoal_Event_response(::qarm_interfaces::action::MoveQArm_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_SendGoal_Event response(::qarm_interfaces::action::MoveQArm_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Event msg_;
};

class Init_MoveQArm_SendGoal_Event_request
{
public:
  explicit Init_MoveQArm_SendGoal_Event_request(::qarm_interfaces::action::MoveQArm_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_MoveQArm_SendGoal_Event_response request(::qarm_interfaces::action::MoveQArm_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_MoveQArm_SendGoal_Event_response(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Event msg_;
};

class Init_MoveQArm_SendGoal_Event_info
{
public:
  Init_MoveQArm_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_SendGoal_Event_request info(::qarm_interfaces::action::MoveQArm_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_MoveQArm_SendGoal_Event_request(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_SendGoal_Event>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_SendGoal_Event_info();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_GetResult_Request_goal_id
{
public:
  Init_MoveQArm_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::qarm_interfaces::action::MoveQArm_GetResult_Request goal_id(::qarm_interfaces::action::MoveQArm_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_GetResult_Request>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_GetResult_Request_goal_id();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_GetResult_Response_result
{
public:
  explicit Init_MoveQArm_GetResult_Response_result(::qarm_interfaces::action::MoveQArm_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_GetResult_Response result(::qarm_interfaces::action::MoveQArm_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Response msg_;
};

class Init_MoveQArm_GetResult_Response_status
{
public:
  Init_MoveQArm_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_GetResult_Response_result status(::qarm_interfaces::action::MoveQArm_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_MoveQArm_GetResult_Response_result(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_GetResult_Response>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_GetResult_Response_status();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_GetResult_Event_response
{
public:
  explicit Init_MoveQArm_GetResult_Event_response(::qarm_interfaces::action::MoveQArm_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_GetResult_Event response(::qarm_interfaces::action::MoveQArm_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Event msg_;
};

class Init_MoveQArm_GetResult_Event_request
{
public:
  explicit Init_MoveQArm_GetResult_Event_request(::qarm_interfaces::action::MoveQArm_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_MoveQArm_GetResult_Event_response request(::qarm_interfaces::action::MoveQArm_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_MoveQArm_GetResult_Event_response(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Event msg_;
};

class Init_MoveQArm_GetResult_Event_info
{
public:
  Init_MoveQArm_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_GetResult_Event_request info(::qarm_interfaces::action::MoveQArm_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_MoveQArm_GetResult_Event_request(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_GetResult_Event>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_GetResult_Event_info();
}

}  // namespace qarm_interfaces


namespace qarm_interfaces
{

namespace action
{

namespace builder
{

class Init_MoveQArm_FeedbackMessage_feedback
{
public:
  explicit Init_MoveQArm_FeedbackMessage_feedback(::qarm_interfaces::action::MoveQArm_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::action::MoveQArm_FeedbackMessage feedback(::qarm_interfaces::action::MoveQArm_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_FeedbackMessage msg_;
};

class Init_MoveQArm_FeedbackMessage_goal_id
{
public:
  Init_MoveQArm_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveQArm_FeedbackMessage_feedback goal_id(::qarm_interfaces::action::MoveQArm_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MoveQArm_FeedbackMessage_feedback(msg_);
  }

private:
  ::qarm_interfaces::action::MoveQArm_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::action::MoveQArm_FeedbackMessage>()
{
  return qarm_interfaces::action::builder::Init_MoveQArm_FeedbackMessage_goal_id();
}

}  // namespace qarm_interfaces

#endif  // QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__BUILDER_HPP_
