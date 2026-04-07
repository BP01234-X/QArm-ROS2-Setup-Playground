// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/msg/q_arm_diagnostics.h"


#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_H_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'joint_names'
#include "rosidl_runtime_c/string.h"
// Member 'joint_currents'
// Member 'joint_pwms'
// Member 'joint_temperatures'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/QArmDiagnostics in the package qarm_interfaces.
typedef struct qarm_interfaces__msg__QArmDiagnostics
{
  std_msgs__msg__Header header;
  /// Name
  rosidl_runtime_c__String__Sequence joint_names;
  /// JointCurrent
  rosidl_runtime_c__double__Sequence joint_currents;
  /// JointPWM
  rosidl_runtime_c__double__Sequence joint_pwms;
  /// JointTemperature
  rosidl_runtime_c__double__Sequence joint_temperatures;
} qarm_interfaces__msg__QArmDiagnostics;

// Struct for a sequence of qarm_interfaces__msg__QArmDiagnostics.
typedef struct qarm_interfaces__msg__QArmDiagnostics__Sequence
{
  qarm_interfaces__msg__QArmDiagnostics * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} qarm_interfaces__msg__QArmDiagnostics__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_H_
