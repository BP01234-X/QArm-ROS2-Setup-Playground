// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__functions.h"
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace qarm_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void QArmDiagnostics_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) qarm_interfaces::msg::QArmDiagnostics(_init);
}

void QArmDiagnostics_fini_function(void * message_memory)
{
  auto typed_message = static_cast<qarm_interfaces::msg::QArmDiagnostics *>(message_memory);
  typed_message->~QArmDiagnostics();
}

size_t size_function__QArmDiagnostics__joint_names(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return member->size();
}

const void * get_const_function__QArmDiagnostics__joint_names(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void * get_function__QArmDiagnostics__joint_names(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<std::string> *>(untyped_member);
  return &member[index];
}

void fetch_function__QArmDiagnostics__joint_names(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const std::string *>(
    get_const_function__QArmDiagnostics__joint_names(untyped_member, index));
  auto & value = *reinterpret_cast<std::string *>(untyped_value);
  value = item;
}

void assign_function__QArmDiagnostics__joint_names(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<std::string *>(
    get_function__QArmDiagnostics__joint_names(untyped_member, index));
  const auto & value = *reinterpret_cast<const std::string *>(untyped_value);
  item = value;
}

void resize_function__QArmDiagnostics__joint_names(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<std::string> *>(untyped_member);
  member->resize(size);
}

size_t size_function__QArmDiagnostics__joint_currents(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__QArmDiagnostics__joint_currents(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__QArmDiagnostics__joint_currents(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__QArmDiagnostics__joint_currents(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__QArmDiagnostics__joint_currents(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__QArmDiagnostics__joint_currents(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__QArmDiagnostics__joint_currents(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__QArmDiagnostics__joint_currents(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__QArmDiagnostics__joint_pwms(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__QArmDiagnostics__joint_pwms(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__QArmDiagnostics__joint_pwms(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__QArmDiagnostics__joint_pwms(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__QArmDiagnostics__joint_pwms(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__QArmDiagnostics__joint_pwms(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__QArmDiagnostics__joint_pwms(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__QArmDiagnostics__joint_pwms(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

size_t size_function__QArmDiagnostics__joint_temperatures(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<double> *>(untyped_member);
  return member->size();
}

const void * get_const_function__QArmDiagnostics__joint_temperatures(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<double> *>(untyped_member);
  return &member[index];
}

void * get_function__QArmDiagnostics__joint_temperatures(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<double> *>(untyped_member);
  return &member[index];
}

void fetch_function__QArmDiagnostics__joint_temperatures(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__QArmDiagnostics__joint_temperatures(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__QArmDiagnostics__joint_temperatures(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__QArmDiagnostics__joint_temperatures(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

void resize_function__QArmDiagnostics__joint_temperatures(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<double> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember QArmDiagnostics_message_member_array[5] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces::msg::QArmDiagnostics, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "joint_names",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces::msg::QArmDiagnostics, joint_names),  // bytes offset in struct
    nullptr,  // default value
    size_function__QArmDiagnostics__joint_names,  // size() function pointer
    get_const_function__QArmDiagnostics__joint_names,  // get_const(index) function pointer
    get_function__QArmDiagnostics__joint_names,  // get(index) function pointer
    fetch_function__QArmDiagnostics__joint_names,  // fetch(index, &value) function pointer
    assign_function__QArmDiagnostics__joint_names,  // assign(index, value) function pointer
    resize_function__QArmDiagnostics__joint_names  // resize(index) function pointer
  },
  {
    "joint_currents",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces::msg::QArmDiagnostics, joint_currents),  // bytes offset in struct
    nullptr,  // default value
    size_function__QArmDiagnostics__joint_currents,  // size() function pointer
    get_const_function__QArmDiagnostics__joint_currents,  // get_const(index) function pointer
    get_function__QArmDiagnostics__joint_currents,  // get(index) function pointer
    fetch_function__QArmDiagnostics__joint_currents,  // fetch(index, &value) function pointer
    assign_function__QArmDiagnostics__joint_currents,  // assign(index, value) function pointer
    resize_function__QArmDiagnostics__joint_currents  // resize(index) function pointer
  },
  {
    "joint_pwms",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces::msg::QArmDiagnostics, joint_pwms),  // bytes offset in struct
    nullptr,  // default value
    size_function__QArmDiagnostics__joint_pwms,  // size() function pointer
    get_const_function__QArmDiagnostics__joint_pwms,  // get_const(index) function pointer
    get_function__QArmDiagnostics__joint_pwms,  // get(index) function pointer
    fetch_function__QArmDiagnostics__joint_pwms,  // fetch(index, &value) function pointer
    assign_function__QArmDiagnostics__joint_pwms,  // assign(index, value) function pointer
    resize_function__QArmDiagnostics__joint_pwms  // resize(index) function pointer
  },
  {
    "joint_temperatures",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(qarm_interfaces::msg::QArmDiagnostics, joint_temperatures),  // bytes offset in struct
    nullptr,  // default value
    size_function__QArmDiagnostics__joint_temperatures,  // size() function pointer
    get_const_function__QArmDiagnostics__joint_temperatures,  // get_const(index) function pointer
    get_function__QArmDiagnostics__joint_temperatures,  // get(index) function pointer
    fetch_function__QArmDiagnostics__joint_temperatures,  // fetch(index, &value) function pointer
    assign_function__QArmDiagnostics__joint_temperatures,  // assign(index, value) function pointer
    resize_function__QArmDiagnostics__joint_temperatures  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers QArmDiagnostics_message_members = {
  "qarm_interfaces::msg",  // message namespace
  "QArmDiagnostics",  // message name
  5,  // number of fields
  sizeof(qarm_interfaces::msg::QArmDiagnostics),
  false,  // has_any_key_member_
  QArmDiagnostics_message_member_array,  // message members
  QArmDiagnostics_init_function,  // function to initialize message memory (memory has to be allocated)
  QArmDiagnostics_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t QArmDiagnostics_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &QArmDiagnostics_message_members,
  get_message_typesupport_handle_function,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_hash,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_description,
  &qarm_interfaces__msg__QArmDiagnostics__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace qarm_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<qarm_interfaces::msg::QArmDiagnostics>()
{
  return &::qarm_interfaces::msg::rosidl_typesupport_introspection_cpp::QArmDiagnostics_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, qarm_interfaces, msg, QArmDiagnostics)() {
  return &::qarm_interfaces::msg::rosidl_typesupport_introspection_cpp::QArmDiagnostics_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
