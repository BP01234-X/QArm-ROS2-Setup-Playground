// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include <cstddef>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "qarm_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace qarm_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
cdr_serialize(
  const qarm_interfaces::msg::QArmDiagnostics & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  qarm_interfaces::msg::QArmDiagnostics & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
get_serialized_size(
  const qarm_interfaces::msg::QArmDiagnostics & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
max_serialized_size_QArmDiagnostics(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
cdr_serialize_key(
  const qarm_interfaces::msg::QArmDiagnostics & ros_message,
  eprosima::fastcdr::Cdr &);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
get_serialized_size_key(
  const qarm_interfaces::msg::QArmDiagnostics & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
max_serialized_size_key_QArmDiagnostics(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace qarm_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_qarm_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, qarm_interfaces, msg, QArmDiagnostics)();

#ifdef __cplusplus
}
#endif

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
