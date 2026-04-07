// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from qarm_interfaces:action/MoveQArm.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "qarm_interfaces/action/move_q_arm.h"


#ifndef QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__FUNCTIONS_H_
#define QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "qarm_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "qarm_interfaces/action/detail/move_q_arm__struct.h"

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm__get_type_hash(
  const rosidl_action_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm__get_type_description(
  const rosidl_action_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm__get_individual_type_description_source(
  const rosidl_action_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm__get_type_description_sources(
  const rosidl_action_type_support_t * type_support);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_Goal
 * )) before or use
 * qarm_interfaces__action__MoveQArm_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__init(qarm_interfaces__action__MoveQArm_Goal * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Goal__fini(qarm_interfaces__action__MoveQArm_Goal * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Goal *
qarm_interfaces__action__MoveQArm_Goal__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Goal__destroy(qarm_interfaces__action__MoveQArm_Goal * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__are_equal(const qarm_interfaces__action__MoveQArm_Goal * lhs, const qarm_interfaces__action__MoveQArm_Goal * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__copy(
  const qarm_interfaces__action__MoveQArm_Goal * input,
  qarm_interfaces__action__MoveQArm_Goal * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_Goal__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_Goal__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_Goal__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_Goal__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__Sequence__init(qarm_interfaces__action__MoveQArm_Goal__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Goal__Sequence__fini(qarm_interfaces__action__MoveQArm_Goal__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Goal__Sequence *
qarm_interfaces__action__MoveQArm_Goal__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Goal__Sequence__destroy(qarm_interfaces__action__MoveQArm_Goal__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_Goal__Sequence * lhs, const qarm_interfaces__action__MoveQArm_Goal__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Goal__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_Goal__Sequence * input,
  qarm_interfaces__action__MoveQArm_Goal__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_Result
 * )) before or use
 * qarm_interfaces__action__MoveQArm_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__init(qarm_interfaces__action__MoveQArm_Result * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Result__fini(qarm_interfaces__action__MoveQArm_Result * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Result *
qarm_interfaces__action__MoveQArm_Result__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Result__destroy(qarm_interfaces__action__MoveQArm_Result * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__are_equal(const qarm_interfaces__action__MoveQArm_Result * lhs, const qarm_interfaces__action__MoveQArm_Result * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__copy(
  const qarm_interfaces__action__MoveQArm_Result * input,
  qarm_interfaces__action__MoveQArm_Result * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_Result__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_Result__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_Result__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_Result__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__Sequence__init(qarm_interfaces__action__MoveQArm_Result__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Result__Sequence__fini(qarm_interfaces__action__MoveQArm_Result__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Result__Sequence *
qarm_interfaces__action__MoveQArm_Result__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Result__Sequence__destroy(qarm_interfaces__action__MoveQArm_Result__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_Result__Sequence * lhs, const qarm_interfaces__action__MoveQArm_Result__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Result__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_Result__Sequence * input,
  qarm_interfaces__action__MoveQArm_Result__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_Feedback
 * )) before or use
 * qarm_interfaces__action__MoveQArm_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__init(qarm_interfaces__action__MoveQArm_Feedback * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Feedback__fini(qarm_interfaces__action__MoveQArm_Feedback * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Feedback *
qarm_interfaces__action__MoveQArm_Feedback__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Feedback__destroy(qarm_interfaces__action__MoveQArm_Feedback * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__are_equal(const qarm_interfaces__action__MoveQArm_Feedback * lhs, const qarm_interfaces__action__MoveQArm_Feedback * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__copy(
  const qarm_interfaces__action__MoveQArm_Feedback * input,
  qarm_interfaces__action__MoveQArm_Feedback * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_Feedback__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_Feedback__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_Feedback__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_Feedback__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__Sequence__init(qarm_interfaces__action__MoveQArm_Feedback__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Feedback__Sequence__fini(qarm_interfaces__action__MoveQArm_Feedback__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_Feedback__Sequence *
qarm_interfaces__action__MoveQArm_Feedback__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_Feedback__Sequence__destroy(qarm_interfaces__action__MoveQArm_Feedback__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_Feedback__Sequence * lhs, const qarm_interfaces__action__MoveQArm_Feedback__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_Feedback__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_Feedback__Sequence * input,
  qarm_interfaces__action__MoveQArm_Feedback__Sequence * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_SendGoal__get_type_hash(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_SendGoal__get_type_description(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_SendGoal__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal__get_type_description_sources(
  const rosidl_service_type_support_t * type_support);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_SendGoal_Request
 * )) before or use
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__init(qarm_interfaces__action__MoveQArm_SendGoal_Request * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Request__fini(qarm_interfaces__action__MoveQArm_SendGoal_Request * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Request *
qarm_interfaces__action__MoveQArm_SendGoal_Request__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Request__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Request * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Request * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Request * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Request * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Request * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_SendGoal_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__init(qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__fini(qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Request__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_SendGoal_Response
 * )) before or use
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__init(qarm_interfaces__action__MoveQArm_SendGoal_Response * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Response__fini(qarm_interfaces__action__MoveQArm_SendGoal_Response * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Response *
qarm_interfaces__action__MoveQArm_SendGoal_Response__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Response__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Response * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Response * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Response * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Response * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Response * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_SendGoal_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__init(qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__fini(qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Response__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_SendGoal_Event
 * )) before or use
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__init(qarm_interfaces__action__MoveQArm_SendGoal_Event * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Event__fini(qarm_interfaces__action__MoveQArm_SendGoal_Event * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Event *
qarm_interfaces__action__MoveQArm_SendGoal_Event__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Event__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Event * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Event * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Event * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Event * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Event * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_SendGoal_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__init(qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__fini(qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence *
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__destroy(qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * lhs, const qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * input,
  qarm_interfaces__action__MoveQArm_SendGoal_Event__Sequence * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_GetResult__get_type_hash(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_GetResult__get_type_description(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_GetResult__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_GetResult__get_type_description_sources(
  const rosidl_service_type_support_t * type_support);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_GetResult_Request
 * )) before or use
 * qarm_interfaces__action__MoveQArm_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__init(qarm_interfaces__action__MoveQArm_GetResult_Request * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Request__fini(qarm_interfaces__action__MoveQArm_GetResult_Request * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Request *
qarm_interfaces__action__MoveQArm_GetResult_Request__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Request__destroy(qarm_interfaces__action__MoveQArm_GetResult_Request * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Request * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Request * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Request * input,
  qarm_interfaces__action__MoveQArm_GetResult_Request * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_GetResult_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__init(qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__fini(qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__destroy(qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * input,
  qarm_interfaces__action__MoveQArm_GetResult_Request__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_GetResult_Response
 * )) before or use
 * qarm_interfaces__action__MoveQArm_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__init(qarm_interfaces__action__MoveQArm_GetResult_Response * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Response__fini(qarm_interfaces__action__MoveQArm_GetResult_Response * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Response *
qarm_interfaces__action__MoveQArm_GetResult_Response__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Response__destroy(qarm_interfaces__action__MoveQArm_GetResult_Response * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Response * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Response * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Response * input,
  qarm_interfaces__action__MoveQArm_GetResult_Response * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_GetResult_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__init(qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__fini(qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__destroy(qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * input,
  qarm_interfaces__action__MoveQArm_GetResult_Response__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_GetResult_Event
 * )) before or use
 * qarm_interfaces__action__MoveQArm_GetResult_Event__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__init(qarm_interfaces__action__MoveQArm_GetResult_Event * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Event__fini(qarm_interfaces__action__MoveQArm_GetResult_Event * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Event *
qarm_interfaces__action__MoveQArm_GetResult_Event__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Event__destroy(qarm_interfaces__action__MoveQArm_GetResult_Event * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Event * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Event * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Event * input,
  qarm_interfaces__action__MoveQArm_GetResult_Event * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_GetResult_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__init(qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__fini(qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence *
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__destroy(qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * lhs, const qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * input,
  qarm_interfaces__action__MoveQArm_GetResult_Event__Sequence * output);

/// Initialize action/MoveQArm message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * qarm_interfaces__action__MoveQArm_FeedbackMessage
 * )) before or use
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__init(qarm_interfaces__action__MoveQArm_FeedbackMessage * msg);

/// Finalize action/MoveQArm message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_FeedbackMessage__fini(qarm_interfaces__action__MoveQArm_FeedbackMessage * msg);

/// Create action/MoveQArm message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_FeedbackMessage *
qarm_interfaces__action__MoveQArm_FeedbackMessage__create(void);

/// Destroy action/MoveQArm message.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_FeedbackMessage__destroy(qarm_interfaces__action__MoveQArm_FeedbackMessage * msg);

/// Check for action/MoveQArm message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__are_equal(const qarm_interfaces__action__MoveQArm_FeedbackMessage * lhs, const qarm_interfaces__action__MoveQArm_FeedbackMessage * rhs);

/// Copy a action/MoveQArm message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__copy(
  const qarm_interfaces__action__MoveQArm_FeedbackMessage * input,
  qarm_interfaces__action__MoveQArm_FeedbackMessage * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_type_hash_t *
qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource *
qarm_interfaces__action__MoveQArm_FeedbackMessage__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
qarm_interfaces__action__MoveQArm_FeedbackMessage__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of action/MoveQArm messages.
/**
 * It allocates the memory for the number of elements and calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__init(qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__fini(qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * array);

/// Create array of action/MoveQArm messages.
/**
 * It allocates the memory for the array and calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence *
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/MoveQArm messages.
/**
 * It calls
 * qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
void
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__destroy(qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * array);

/// Check for action/MoveQArm message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__are_equal(const qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * lhs, const qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/MoveQArm messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_qarm_interfaces
bool
qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence__copy(
  const qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * input,
  qarm_interfaces__action__MoveQArm_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // QARM_INTERFACES__ACTION__DETAIL__MOVE_Q_ARM__FUNCTIONS_H_
