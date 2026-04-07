#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to qarm_interfaces__msg__QArmDiagnostics

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QArmDiagnostics {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Name
    pub joint_names: Vec<std::string::String>,

    /// JointCurrent
    pub joint_currents: Vec<f64>,

    /// JointPWM
    pub joint_pwms: Vec<f64>,

    /// JointTemperature
    pub joint_temperatures: Vec<f64>,

}



impl Default for QArmDiagnostics {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::QArmDiagnostics::default())
  }
}

impl rosidl_runtime_rs::Message for QArmDiagnostics {
  type RmwMsg = super::msg::rmw::QArmDiagnostics;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_currents: msg.joint_currents.into(),
        joint_pwms: msg.joint_pwms.into(),
        joint_temperatures: msg.joint_temperatures.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_currents: msg.joint_currents.as_slice().into(),
        joint_pwms: msg.joint_pwms.as_slice().into(),
        joint_temperatures: msg.joint_temperatures.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      joint_currents: msg.joint_currents
          .into_iter()
          .collect(),
      joint_pwms: msg.joint_pwms
          .into_iter()
          .collect(),
      joint_temperatures: msg.joint_temperatures
          .into_iter()
          .collect(),
    }
  }
}


