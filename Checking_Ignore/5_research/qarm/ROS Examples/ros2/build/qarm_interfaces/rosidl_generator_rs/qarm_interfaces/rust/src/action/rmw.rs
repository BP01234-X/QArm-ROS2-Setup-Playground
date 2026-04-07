
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Goal() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_Goal__init(msg: *mut MoveQArm_Goal) -> bool;
    fn qarm_interfaces__action__MoveQArm_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Goal>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Goal>);
    fn qarm_interfaces__action__MoveQArm_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Goal>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub task_space_pose: [f64; 4],

}



impl Default for MoveQArm_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_Goal__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Goal() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Result() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_Result__init(msg: *mut MoveQArm_Result) -> bool;
    fn qarm_interfaces__action__MoveQArm_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Result>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Result>);
    fn qarm_interfaces__action__MoveQArm_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Result>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MoveQArm_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_Result__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_Result where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Result() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_Feedback__init(msg: *mut MoveQArm_Feedback) -> bool;
    fn qarm_interfaces__action__MoveQArm_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Feedback>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Feedback>);
    fn qarm_interfaces__action__MoveQArm_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_Feedback>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position_error_norm: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation_error: f64,

}



impl Default for MoveQArm_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_Feedback__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_Feedback() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_FeedbackMessage__init(msg: *mut MoveQArm_FeedbackMessage) -> bool;
    fn qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_FeedbackMessage>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_FeedbackMessage>);
    fn qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_FeedbackMessage>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::MoveQArm_Feedback,

}



impl Default for MoveQArm_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_FeedbackMessage() }
  }
}




#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_SendGoal_Request__init(msg: *mut MoveQArm_SendGoal_Request) -> bool;
    fn qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Request>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Request>);
    fn qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Request>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::MoveQArm_Goal,

}



impl Default for MoveQArm_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal_Request() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_SendGoal_Response__init(msg: *mut MoveQArm_SendGoal_Response) -> bool;
    fn qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Response>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Response>);
    fn qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_SendGoal_Response>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for MoveQArm_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal_Response() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_GetResult_Request__init(msg: *mut MoveQArm_GetResult_Request) -> bool;
    fn qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Request>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Request>);
    fn qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Request>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for MoveQArm_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult_Request() }
  }
}


#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "qarm_interfaces__rosidl_generator_c")]
extern "C" {
    fn qarm_interfaces__action__MoveQArm_GetResult_Response__init(msg: *mut MoveQArm_GetResult_Response) -> bool;
    fn qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Response>, size: usize) -> bool;
    fn qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Response>);
    fn qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveQArm_GetResult_Response>) -> bool;
}

// Corresponds to qarm_interfaces__action__MoveQArm_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveQArm_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::MoveQArm_Result,

}



impl Default for MoveQArm_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !qarm_interfaces__action__MoveQArm_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to qarm_interfaces__action__MoveQArm_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveQArm_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveQArm_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveQArm_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "qarm_interfaces/action/MoveQArm_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult_Response() }
  }
}






#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to qarm_interfaces__action__MoveQArm_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveQArm_SendGoal;

impl rosidl_runtime_rs::Service for MoveQArm_SendGoal {
    type Request = MoveQArm_SendGoal_Request;
    type Response = MoveQArm_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__qarm_interfaces__action__MoveQArm_SendGoal() }
    }
}




#[link(name = "qarm_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to qarm_interfaces__action__MoveQArm_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveQArm_GetResult;

impl rosidl_runtime_rs::Service for MoveQArm_GetResult {
    type Request = MoveQArm_GetResult_Request;
    type Response = MoveQArm_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__qarm_interfaces__action__MoveQArm_GetResult() }
    }
}


