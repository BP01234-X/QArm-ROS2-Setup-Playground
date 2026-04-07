// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/msg/q_arm_diagnostics.hpp"


#ifndef QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__TRAITS_HPP_
#define QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "qarm_interfaces/msg/detail/q_arm_diagnostics__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace qarm_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const QArmDiagnostics & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: joint_names
  {
    if (msg.joint_names.size() == 0) {
      out << "joint_names: []";
    } else {
      out << "joint_names: [";
      size_t pending_items = msg.joint_names.size();
      for (auto item : msg.joint_names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_currents
  {
    if (msg.joint_currents.size() == 0) {
      out << "joint_currents: []";
    } else {
      out << "joint_currents: [";
      size_t pending_items = msg.joint_currents.size();
      for (auto item : msg.joint_currents) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_pwms
  {
    if (msg.joint_pwms.size() == 0) {
      out << "joint_pwms: []";
    } else {
      out << "joint_pwms: [";
      size_t pending_items = msg.joint_pwms.size();
      for (auto item : msg.joint_pwms) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: joint_temperatures
  {
    if (msg.joint_temperatures.size() == 0) {
      out << "joint_temperatures: []";
    } else {
      out << "joint_temperatures: [";
      size_t pending_items = msg.joint_temperatures.size();
      for (auto item : msg.joint_temperatures) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const QArmDiagnostics & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: joint_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_names.size() == 0) {
      out << "joint_names: []\n";
    } else {
      out << "joint_names:\n";
      for (auto item : msg.joint_names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_currents
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_currents.size() == 0) {
      out << "joint_currents: []\n";
    } else {
      out << "joint_currents:\n";
      for (auto item : msg.joint_currents) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_pwms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_pwms.size() == 0) {
      out << "joint_pwms: []\n";
    } else {
      out << "joint_pwms:\n";
      for (auto item : msg.joint_pwms) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: joint_temperatures
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_temperatures.size() == 0) {
      out << "joint_temperatures: []\n";
    } else {
      out << "joint_temperatures:\n";
      for (auto item : msg.joint_temperatures) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const QArmDiagnostics & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace qarm_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use qarm_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const qarm_interfaces::msg::QArmDiagnostics & msg,
  std::ostream & out, size_t indentation = 0)
{
  qarm_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use qarm_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const qarm_interfaces::msg::QArmDiagnostics & msg)
{
  return qarm_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<qarm_interfaces::msg::QArmDiagnostics>()
{
  return "qarm_interfaces::msg::QArmDiagnostics";
}

template<>
inline const char * name<qarm_interfaces::msg::QArmDiagnostics>()
{
  return "qarm_interfaces/msg/QArmDiagnostics";
}

template<>
struct has_fixed_size<qarm_interfaces::msg::QArmDiagnostics>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<qarm_interfaces::msg::QArmDiagnostics>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<qarm_interfaces::msg::QArmDiagnostics>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // QARM_INTERFACES__MSG__DETAIL__Q_ARM_DIAGNOSTICS__TRAITS_HPP_
