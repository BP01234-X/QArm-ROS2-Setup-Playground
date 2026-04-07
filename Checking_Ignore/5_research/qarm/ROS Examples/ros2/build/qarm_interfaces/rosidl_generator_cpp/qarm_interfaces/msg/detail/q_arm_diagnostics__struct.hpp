// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/msg/q_arm_diagnostics.hpp"


#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_HPP_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__qarm_interfaces__msg__QArmDiagnostics __attribute__((deprecated))
#else
# define DEPRECATED__qarm_interfaces__msg__QArmDiagnostics __declspec(deprecated)
#endif

namespace qarm_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct QArmDiagnostics_
{
  using Type = QArmDiagnostics_<ContainerAllocator>;

  explicit QArmDiagnostics_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit QArmDiagnostics_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _joint_names_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _joint_names_type joint_names;
  using _joint_currents_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joint_currents_type joint_currents;
  using _joint_pwms_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joint_pwms_type joint_pwms;
  using _joint_temperatures_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _joint_temperatures_type joint_temperatures;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__joint_names(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->joint_names = _arg;
    return *this;
  }
  Type & set__joint_currents(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joint_currents = _arg;
    return *this;
  }
  Type & set__joint_pwms(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joint_pwms = _arg;
    return *this;
  }
  Type & set__joint_temperatures(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->joint_temperatures = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> *;
  using ConstRawPtr =
    const qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__qarm_interfaces__msg__QArmDiagnostics
    std::shared_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__qarm_interfaces__msg__QArmDiagnostics
    std::shared_ptr<qarm_interfaces::msg::QArmDiagnostics_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const QArmDiagnostics_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->joint_names != other.joint_names) {
      return false;
    }
    if (this->joint_currents != other.joint_currents) {
      return false;
    }
    if (this->joint_pwms != other.joint_pwms) {
      return false;
    }
    if (this->joint_temperatures != other.joint_temperatures) {
      return false;
    }
    return true;
  }
  bool operator!=(const QArmDiagnostics_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct QArmDiagnostics_

// alias to use template instance with default allocator
using QArmDiagnostics =
  qarm_interfaces::msg::QArmDiagnostics_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace qarm_interfaces

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__STRUCT_HPP_
