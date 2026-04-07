// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__rosidl_typesupport_introspection_c.h"
#include "qarm_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__functions.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_currents`
// Member `joint_pwms`
// Member `joint_temperatures`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  qarm_interfaces__msg__QArmDiagnostics__init(message_memory);
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_fini_function(void * message_memory)
{
  qarm_interfaces__msg__QArmDiagnostics__fini(message_memory);
}

size_t qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_names(
  const void * untyped_member)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return member->size;
}

const void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_names(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__String__Sequence * member =
    (const rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_names(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  return &member->data[index];
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const rosidl_runtime_c__String * item =
    ((const rosidl_runtime_c__String *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_names(untyped_member, index));
  rosidl_runtime_c__String * value =
    (rosidl_runtime_c__String *)(untyped_value);
  *value = *item;
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  rosidl_runtime_c__String * item =
    ((rosidl_runtime_c__String *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_names(untyped_member, index));
  const rosidl_runtime_c__String * value =
    (const rosidl_runtime_c__String *)(untyped_value);
  *item = *value;
}

bool qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_names(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__String__Sequence * member =
    (rosidl_runtime_c__String__Sequence *)(untyped_member);
  rosidl_runtime_c__String__Sequence__fini(member);
  return rosidl_runtime_c__String__Sequence__init(member, size);
}

size_t qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_currents(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_currents(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_currents(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_currents(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_currents(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_currents(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_currents(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_currents(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_pwms(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_pwms(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_pwms(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_pwms(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_pwms(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_pwms(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_pwms(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_pwms(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

size_t qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_temperatures(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_temperatures(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_temperatures(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_temperatures(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_temperatures(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_temperatures(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_temperatures(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_temperatures(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_member_array[5] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces__msg__QArmDiagnostics, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "joint_names",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces__msg__QArmDiagnostics, joint_names),  // bytes offset in struct
    NULL,  // default value
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_names,  // size() function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_names,  // get_const(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_names,  // get(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_names,  // fetch(index, &value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_names,  // assign(index, value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_names  // resize(index) function pointer
  },
  {
    "joint_currents",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces__msg__QArmDiagnostics, joint_currents),  // bytes offset in struct
    NULL,  // default value
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_currents,  // size() function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_currents,  // get_const(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_currents,  // get(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_currents,  // fetch(index, &value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_currents,  // assign(index, value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_currents  // resize(index) function pointer
  },
  {
    "joint_pwms",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces__msg__QArmDiagnostics, joint_pwms),  // bytes offset in struct
    NULL,  // default value
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_pwms,  // size() function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_pwms,  // get_const(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_pwms,  // get(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_pwms,  // fetch(index, &value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_pwms,  // assign(index, value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_pwms  // resize(index) function pointer
  },
  {
    "joint_temperatures",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces__msg__QArmDiagnostics, joint_temperatures),  // bytes offset in struct
    NULL,  // default value
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__size_function__QArmDiagnostics__joint_temperatures,  // size() function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_const_function__QArmDiagnostics__joint_temperatures,  // get_const(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__get_function__QArmDiagnostics__joint_temperatures,  // get(index) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__fetch_function__QArmDiagnostics__joint_temperatures,  // fetch(index, &value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__assign_function__QArmDiagnostics__joint_temperatures,  // assign(index, value) function pointer
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__resize_function__QArmDiagnostics__joint_temperatures  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_members = {
  "qarm_interfaces__msg",  // message namespace
  "QArmDiagnostics",  // message name
  5,  // number of fields
  sizeof(qarm_interfaces__msg__QArmDiagnostics),
  false,  // has_any_key_member_
  qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_member_array,  // message members
  qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_init_function,  // function to initialize message memory (memory has to be allocated)
  qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_type_support_handle = {
  0,
  &qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_members,
  get_message_typesupport_handle_function,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_hash,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_description,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_qarm_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, qarm_interfaces, msg, QArmDiagnostics)() {
  qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_type_support_handle.typesupport_identifier) {
    qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &qarm_interfaces__msg__QArmDiagnostics__rosidl_typesupport_introspection_c__QArmDiagnostics_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
