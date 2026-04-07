// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from qarm_interfaces:action/MoveQArm.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/action/move_q_arm.h"


#ifndef QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__STRUCT_H_
#define QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_Goal
{
  double task_space_pose[4];
} qarm_interfaces__action__MoveQArm_Goal;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_Goal.
typedef struct qarm_interfaces__action__MoveQArm_Goal__Sequence
{
  qarm_interfaces__action__MoveQArm_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_Result
{
  bool success;
  rosidl_runtime_c__String message;
} qarm_interfaces__action__MoveQArm_Result;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_Result.
typedef struct qarm_interfaces__action__MoveQArm_Result__Sequence
{
  qarm_interfaces__action__MoveQArm_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_Result__Sequence;

// Constants defined in the message

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_Feedback
{
  double position_error_norm;
  double orientation_error;
} qarm_interfaces__action__MoveQArm_Feedback;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_Feedback.
typedef struct qarm_interfaces__action__MoveQArm_Feedback__Sequence
{
  qarm_interfaces__action__MoveQArm_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "qarm_interfaces/action/detail/move_q_arm__struct.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  qarm_interfaces__action__MoveQArm_Goal goal;
} qarm_interfaces__action__MoveQArm_SendGoal_Request;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_SendGoal_Request.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence
{
  qarm_interfaces__action__MoveQArm_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} qarm_interfaces__action__MoveQArm_SendGoal_Response;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_SendGoal_Response.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence
{
  qarm_interfaces__action__MoveQArm_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  qarm_interfaces__action__MoveQArm_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  qarm_interfaces__action__MoveQArm_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence request;
  qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence response;
} qarm_interfaces__action__MoveQArm_SendGoal_Event;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_SendGoal_Event.
typedef struct qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence
{
  qarm_interfaces__action__MoveQArm_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} qarm_interfaces__action__MoveQArm_GetResult_Request;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_GetResult_Request.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence
{
  qarm_interfaces__action__MoveQArm_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Response
{
  int8_t status;
  qarm_interfaces__action__MoveQArm_Result result;
} qarm_interfaces__action__MoveQArm_GetResult_Response;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_GetResult_Response.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence
{
  qarm_interfaces__action__MoveQArm_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  qarm_interfaces__action__MoveQArm_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  qarm_interfaces__action__MoveQArm_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence request;
  qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence response;
} qarm_interfaces__action__MoveQArm_GetResult_Event;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_GetResult_Event.
typedef struct qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence
{
  qarm_interfaces__action__MoveQArm_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.h"

/// Struct defined in action/MoveQArm in the package qarm_interfaces.
typedef struct qarm_interfaces__action__MoveQArm_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  qarm_interfaces__action__MoveQArm_Feedback feedback;
} qarm_interfaces__action__MoveQArm_FeedbackMessage;

// Struct for a sequence of qarm_interfaces__action__MoveQArm_FeedbackMessage.
typedef struct qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence
{
  qarm_interfaces__action__MoveQArm_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__STRUCT_H_
