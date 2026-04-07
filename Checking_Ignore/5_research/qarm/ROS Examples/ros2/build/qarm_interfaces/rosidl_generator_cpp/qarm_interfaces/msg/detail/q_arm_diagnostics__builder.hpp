// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/msg/q_arm_diagnostics.hpp"


#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__BUILDER_HPP_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace qarm_interfaces
{

namespace msg
{

namespace builder
{

class Init_QArmDiagnostics_joint_temperatures
{
public:
  explicit Init_QArmDiagnostics_joint_temperatures(::qarm_interfaces::msg::QArmDiagnostics & msg)
  : msg_(msg)
  {}
  ::qarm_interfaces::msg::QArmDiagnostics joint_temperatures(::qarm_interfaces::msg::QArmDiagnostics::_joint_temperatures_type arg)
  {
    msg_.joint_temperatures = std::move(arg);
    return std::move(msg_);
  }

private:
  ::qarm_interfaces::msg::QArmDiagnostics msg_;
};

class Init_QArmDiagnostics_joint_pwms
{
public:
  explicit Init_QArmDiagnostics_joint_pwms(::qarm_interfaces::msg::QArmDiagnostics & msg)
  : msg_(msg)
  {}
  Init_QArmDiagnostics_joint_temperatures joint_pwms(::qarm_interfaces::msg::QArmDiagnostics::_joint_pwms_type arg)
  {
    msg_.joint_pwms = std::move(arg);
    return Init_QArmDiagnostics_joint_temperatures(msg_);
  }

private:
  ::qarm_interfaces::msg::QArmDiagnostics msg_;
};

class Init_QArmDiagnostics_joint_currents
{
public:
  explicit Init_QArmDiagnostics_joint_currents(::qarm_interfaces::msg::QArmDiagnostics & msg)
  : msg_(msg)
  {}
  Init_QArmDiagnostics_joint_pwms joint_currents(::qarm_interfaces::msg::QArmDiagnostics::_joint_currents_type arg)
  {
    msg_.joint_currents = std::move(arg);
    return Init_QArmDiagnostics_joint_pwms(msg_);
  }

private:
  ::qarm_interfaces::msg::QArmDiagnostics msg_;
};

class Init_QArmDiagnostics_joint_names
{
public:
  explicit Init_QArmDiagnostics_joint_names(::qarm_interfaces::msg::QArmDiagnostics & msg)
  : msg_(msg)
  {}
  Init_QArmDiagnostics_joint_currents joint_names(::qarm_interfaces::msg::QArmDiagnostics::_joint_names_type arg)
  {
    msg_.joint_names = std::move(arg);
    return Init_QArmDiagnostics_joint_currents(msg_);
  }

private:
  ::qarm_interfaces::msg::QArmDiagnostics msg_;
};

class Init_QArmDiagnostics_header
{
public:
  Init_QArmDiagnostics_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_QArmDiagnostics_joint_names header(::qarm_interfaces::msg::QArmDiagnostics::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_QArmDiagnostics_joint_names(msg_);
  }

private:
  ::qarm_interfaces::msg::QArmDiagnostics msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::qarm_interfaces::msg::QArmDiagnostics>()
{
  return qarm_interfaces::msg::builder::Init_QArmDiagnostics_header();
}

}  // namespace qarm_interfaces

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__BUILDER_HPP_
