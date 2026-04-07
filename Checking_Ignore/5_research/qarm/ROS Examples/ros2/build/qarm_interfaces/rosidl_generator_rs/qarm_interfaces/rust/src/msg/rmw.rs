#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__msg__QArmDiagnostics() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__msg__QArmDiagnostics__init(msg: *mut QArmDiagnostics) -> bool;
    fn qarm_interfaces__msg__QArmDiagnostics__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QArmDiagnostics>, size: usize) -> bool;
    fn qarm_interfaces__msg__QArmDiagnostics__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QArmDiagnostics>);
    fn qarm_interfaces__msg__QArmDiagnostics__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QArmDiagnostics>, out_seq: *mut rosidl_runtime_rs::Sequence<QArmDiagnostics>) -> bool;
}

// Corresponds to qarm_interfaces__msg__QArmDiagnostics
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QArmDiagnostics {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Name
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// JointCurrent
    pub joint_currents: rosidl_runtime_rs::Sequence<f64>,

    /// JointPWM
    pub joint_pwms: rosidl_runtime_rs::Sequence<f64>,

    /// JointTemperature
    pub joint_temperatures: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for QArmDiagnostics {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__msg__QArmDiagnostics__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__msg__QArmDiagnostics__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QArmDiagnostics {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__msg__QArmDiagnostics__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__msg__QArmDiagnostics__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__msg__QArmDiagnostics__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QArmDiagnostics {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QArmDiagnostics where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/msg/QArmDiagnostics";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__msg__QArmDiagnostics() }
  }
}


