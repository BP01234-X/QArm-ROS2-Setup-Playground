// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from qarm_interfaces:action/MoveQArm.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "qarm_interfaces/action/detail/move_q_arm__functions.h"
#include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_Goal_type_support_ids_t;

static const _MoveQArm_Goal_type_support_ids_t _MoveQArm_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_Goal_type_support_symbol_names_t _MoveQArm_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_Goal)),
  }
};

typedef struct _MoveQArm_Goal_type_support_data_t
{
  void * data[2];
} _MoveQArm_Goal_type_support_data_t;

static _MoveQArm_Goal_type_support_data_t _MoveQArm_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_Goal_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_Goal__get_type_hash,
  &qarm_interfaces__action__MoveQArm_Goal__get_type_description,
  &qarm_interfaces__action__MoveQArm_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Goal>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_Goal)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_Result_type_support_ids_t;

static const _MoveQArm_Result_type_support_ids_t _MoveQArm_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_Result_type_support_symbol_names_t _MoveQArm_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_Result)),
  }
};

typedef struct _MoveQArm_Result_type_support_data_t
{
  void * data[2];
} _MoveQArm_Result_type_support_data_t;

static _MoveQArm_Result_type_support_data_t _MoveQArm_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_Result_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_Result_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_Result_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_Result__get_type_hash,
  &qarm_interfaces__action__MoveQArm_Result__get_type_description,
  &qarm_interfaces__action__MoveQArm_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Result>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_Result)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_Feedback_type_support_ids_t;

static const _MoveQArm_Feedback_type_support_ids_t _MoveQArm_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_Feedback_type_support_symbol_names_t _MoveQArm_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_Feedback)),
  }
};

typedef struct _MoveQArm_Feedback_type_support_data_t
{
  void * data[2];
} _MoveQArm_Feedback_type_support_data_t;

static _MoveQArm_Feedback_type_support_data_t _MoveQArm_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_Feedback_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_Feedback__get_type_hash,
  &qarm_interfaces__action__MoveQArm_Feedback__get_type_description,
  &qarm_interfaces__action__MoveQArm_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Feedback>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_Feedback)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_SendGoal_Request_type_support_ids_t;

static const _MoveQArm_SendGoal_Request_type_support_ids_t _MoveQArm_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_SendGoal_Request_type_support_symbol_names_t _MoveQArm_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Request)),
  }
};

typedef struct _MoveQArm_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _MoveQArm_SendGoal_Request_type_support_data_t;

static _MoveQArm_SendGoal_Request_type_support_data_t _MoveQArm_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_SendGoal_Request_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_hash,
  &qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_description,
  &qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Request>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Request)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_SendGoal_Response_type_support_ids_t;

static const _MoveQArm_SendGoal_Response_type_support_ids_t _MoveQArm_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_SendGoal_Response_type_support_symbol_names_t _MoveQArm_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Response)),
  }
};

typedef struct _MoveQArm_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _MoveQArm_SendGoal_Response_type_support_data_t;

static _MoveQArm_SendGoal_Response_type_support_data_t _MoveQArm_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_SendGoal_Response_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_hash,
  &qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_description,
  &qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Response>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Response)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_SendGoal_Event_type_support_ids_t;

static const _MoveQArm_SendGoal_Event_type_support_ids_t _MoveQArm_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_SendGoal_Event_type_support_symbol_names_t _MoveQArm_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Event)),
  }
};

typedef struct _MoveQArm_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _MoveQArm_SendGoal_Event_type_support_data_t;

static _MoveQArm_SendGoal_Event_type_support_data_t _MoveQArm_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_SendGoal_Event_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_SendGoal_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_SendGoal_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_hash,
  &qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_description,
  &qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Event>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_SendGoal_Event)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_SendGoal_type_support_ids_t;

static const _MoveQArm_SendGoal_type_support_ids_t _MoveQArm_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_SendGoal_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_SendGoal_type_support_symbol_names_t _MoveQArm_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_SendGoal)),
  }
};

typedef struct _MoveQArm_SendGoal_type_support_data_t
{
  void * data[2];
} _MoveQArm_SendGoal_type_support_data_t;

static _MoveQArm_SendGoal_type_support_data_t _MoveQArm_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_SendGoal_service_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveQArm_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<qarm_interfaces::action::MoveQArm_SendGoal>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<qarm_interfaces::action::MoveQArm_SendGoal>,
  &qarm_interfaces__action__MoveQArm_SendGoal__get_type_hash,
  &qarm_interfaces__action__MoveQArm_SendGoal__get_type_description,
  &qarm_interfaces__action__MoveQArm_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<qarm_interfaces::action::MoveQArm_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_GetResult_Request_type_support_ids_t;

static const _MoveQArm_GetResult_Request_type_support_ids_t _MoveQArm_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_GetResult_Request_type_support_symbol_names_t _MoveQArm_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_GetResult_Request)),
  }
};

typedef struct _MoveQArm_GetResult_Request_type_support_data_t
{
  void * data[2];
} _MoveQArm_GetResult_Request_type_support_data_t;

static _MoveQArm_GetResult_Request_type_support_data_t _MoveQArm_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_GetResult_Request_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_hash,
  &qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_description,
  &qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Request>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_GetResult_Request)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_GetResult_Response_type_support_ids_t;

static const _MoveQArm_GetResult_Response_type_support_ids_t _MoveQArm_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_GetResult_Response_type_support_symbol_names_t _MoveQArm_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_GetResult_Response)),
  }
};

typedef struct _MoveQArm_GetResult_Response_type_support_data_t
{
  void * data[2];
} _MoveQArm_GetResult_Response_type_support_data_t;

static _MoveQArm_GetResult_Response_type_support_data_t _MoveQArm_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_GetResult_Response_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_hash,
  &qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_description,
  &qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Response>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_GetResult_Response)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_GetResult_Event_type_support_ids_t;

static const _MoveQArm_GetResult_Event_type_support_ids_t _MoveQArm_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_GetResult_Event_type_support_symbol_names_t _MoveQArm_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_GetResult_Event)),
  }
};

typedef struct _MoveQArm_GetResult_Event_type_support_data_t
{
  void * data[2];
} _MoveQArm_GetResult_Event_type_support_data_t;

static _MoveQArm_GetResult_Event_type_support_data_t _MoveQArm_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_GetResult_Event_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_GetResult_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_GetResult_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_hash,
  &qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_description,
  &qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Event>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_GetResult_Event)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_GetResult_type_support_ids_t;

static const _MoveQArm_GetResult_type_support_ids_t _MoveQArm_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_GetResult_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_GetResult_type_support_symbol_names_t _MoveQArm_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_GetResult)),
  }
};

typedef struct _MoveQArm_GetResult_type_support_data_t
{
  void * data[2];
} _MoveQArm_GetResult_type_support_data_t;

static _MoveQArm_GetResult_type_support_data_t _MoveQArm_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_GetResult_service_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveQArm_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<qarm_interfaces::action::MoveQArm_GetResult>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<qarm_interfaces::action::MoveQArm_GetResult>,
  &qarm_interfaces__action__MoveQArm_GetResult__get_type_hash,
  &qarm_interfaces__action__MoveQArm_GetResult__get_type_description,
  &qarm_interfaces__action__MoveQArm_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<qarm_interfaces::action::MoveQArm_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__functions.h"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveQArm_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveQArm_FeedbackMessage_type_support_ids_t;

static const _MoveQArm_FeedbackMessage_type_support_ids_t _MoveQArm_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveQArm_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveQArm_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveQArm_FeedbackMessage_type_support_symbol_names_t _MoveQArm_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, action, MoveQArm_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, action, MoveQArm_FeedbackMessage)),
  }
};

typedef struct _MoveQArm_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _MoveQArm_FeedbackMessage_type_support_data_t;

static _MoveQArm_FeedbackMessage_type_support_data_t _MoveQArm_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveQArm_FeedbackMessage_message_typesupport_map = {
  2,
  "qarm_interfaces",
  &_MoveQArm_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_MoveQArm_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_MoveQArm_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveQArm_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveQArm_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_hash,
  &qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_description,
  &qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::action::MoveQArm_FeedbackMessage>()
{
  return &::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm_FeedbackMessage)() {
  return get_message_type_support_handle<qarm_interfaces::action::MoveQArm_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "qarm_interfaces/action/detail/move_q_arm__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace qarm_interfaces
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t MoveQArm_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL,
  &qarm_interfaces__action__MoveQArm__get_type_hash,
  &qarm_interfaces__action__MoveQArm__get_type_description,
  &qarm_interfaces__action__MoveQArm__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace qarm_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<qarm_interfaces::action::MoveQArm>()
{
  using ::qarm_interfaces::action::rosidl_typesupport_cpp::MoveQArm_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  MoveQArm_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::qarm_interfaces::action::MoveQArm::Impl::SendGoalService>();
  MoveQArm_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::qarm_interfaces::action::MoveQArm::Impl::GetResultService>();
  MoveQArm_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::qarm_interfaces::action::MoveQArm::Impl::CancelGoalService>();
  MoveQArm_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::qarm_interfaces::action::MoveQArm::Impl::FeedbackMessage>();
  MoveQArm_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::qarm_interfaces::action::MoveQArm::Impl::GoalStatusMessage>();
  return &MoveQArm_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, qarm_interfaces, action, MoveQArm)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<qarm_interfaces::action::MoveQArm>();
}

#ifdef __cplusplus
}
#endif
