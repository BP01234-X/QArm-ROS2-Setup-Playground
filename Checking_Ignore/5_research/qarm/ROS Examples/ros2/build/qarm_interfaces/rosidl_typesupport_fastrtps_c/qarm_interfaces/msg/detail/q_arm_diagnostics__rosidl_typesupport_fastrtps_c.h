// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice
#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "qarm_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
bool cdr_serialize_qarm_interfaces__msg__QArmDiagnostics(
  const qarm_interfaces__msg__QArmDiagnostics * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
bool cdr_deserialize_qarm_interfaces__msg__QArmDiagnostics(
  eprosima::fastcdr::Cdr &,
  qarm_interfaces__msg__QArmDiagnostics * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
size_t get_serialized_size_qarm_interfaces__msg__QArmDiagnostics(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
size_t max_serialized_size_qarm_interfaces__msg__QArmDiagnostics(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
bool cdr_serialize_key_qarm_interfaces__msg__QArmDiagnostics(
  const qarm_interfaces__msg__QArmDiagnostics * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
size_t get_serialized_size_key_qarm_interfaces__msg__QArmDiagnostics(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
size_t max_serialized_size_key_qarm_interfaces__msg__QArmDiagnostics(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_qarm_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, qarm_interfaces, msg, QArmDiagnostics)();

#ifdef __cplusplus
}
#endif

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
