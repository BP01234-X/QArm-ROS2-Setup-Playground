// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from qarm_interfaces:msg/QArmDiagnostics.idl
// generated code does not contain a copyright notice
#include "qarm_interfaces/msg/detail/q_arm_diagnostics__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `joint_names`
#include "rosidl_runtime_c/string_functions.h"
// Member `joint_currents`
// Member `joint_pwms`
// Member `joint_temperatures`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
qarm_interfaces__msg__QArmDiagnostics__init(qarm_interfaces__msg__QArmDiagnostics * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__init(&msg->joint_names, 0)) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joint_currents, 0)) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
    return false;
  }
  // joint_pwms
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joint_pwms, 0)) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
    return false;
  }
  // joint_temperatures
  if (!rosidl_runtime_c__double__Sequence__init(&msg->joint_temperatures, 0)) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
    return false;
  }
  return true;
}

void
qarm_interfaces__msg__QArmDiagnostics__fini(qarm_interfaces__msg__QArmDiagnostics * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // joint_names
  rosidl_runtime_c__String__Sequence__fini(&msg->joint_names);
  // joint_currents
  rosidl_runtime_c__double__Sequence__fini(&msg->joint_currents);
  // joint_pwms
  rosidl_runtime_c__double__Sequence__fini(&msg->joint_pwms);
  // joint_temperatures
  rosidl_runtime_c__double__Sequence__fini(&msg->joint_temperatures);
}

bool
qarm_interfaces__msg__QArmDiagnostics__are_equal(const qarm_interfaces__msg__QArmDiagnostics * lhs, const qarm_interfaces__msg__QArmDiagnostics * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->joint_names), &(rhs->joint_names)))
  {
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joint_currents), &(rhs->joint_currents)))
  {
    return false;
  }
  // joint_pwms
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joint_pwms), &(rhs->joint_pwms)))
  {
    return false;
  }
  // joint_temperatures
  if (!rosidl_runtime_c__double__Sequence__are_equal(
      &(lhs->joint_temperatures), &(rhs->joint_temperatures)))
  {
    return false;
  }
  return true;
}

bool
qarm_interfaces__msg__QArmDiagnostics__copy(
  const qarm_interfaces__msg__QArmDiagnostics * input,
  qarm_interfaces__msg__QArmDiagnostics * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // joint_names
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->joint_names), &(output->joint_names)))
  {
    return false;
  }
  // joint_currents
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joint_currents), &(output->joint_currents)))
  {
    return false;
  }
  // joint_pwms
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joint_pwms), &(output->joint_pwms)))
  {
    return false;
  }
  // joint_temperatures
  if (!rosidl_runtime_c__double__Sequence__copy(
      &(input->joint_temperatures), &(output->joint_temperatures)))
  {
    return false;
  }
  return true;
}

qarm_interfaces__msg__QArmDiagnostics *
qarm_interfaces__msg__QArmDiagnostics__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  qarm_interfaces__msg__QArmDiagnostics * msg = (qarm_interfaces__msg__QArmDiagnostics *)allocator.allocate(sizeof(qarm_interfaces__msg__QArmDiagnostics), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(qarm_interfaces__msg__QArmDiagnostics));
  bool success = qarm_interfaces__msg__QArmDiagnostics__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
qarm_interfaces__msg__QArmDiagnostics__destroy(qarm_interfaces__msg__QArmDiagnostics * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    qarm_interfaces__msg__QArmDiagnostics__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
qarm_interfaces__msg__QArmDiagnostics__Sequence__init(qarm_interfaces__msg__QArmDiagnostics__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  qarm_interfaces__msg__QArmDiagnostics * data = NULL;

  if (size) {
    data = (qarm_interfaces__msg__QArmDiagnostics *)allocator.zero_allocate(size, sizeof(qarm_interfaces__msg__QArmDiagnostics), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = qarm_interfaces__msg__QArmDiagnostics__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        qarm_interfaces__msg__QArmDiagnostics__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
qarm_interfaces__msg__QArmDiagnostics__Sequence__fini(qarm_interfaces__msg__QArmDiagnostics__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      qarm_interfaces__msg__QArmDiagnostics__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

qarm_interfaces__msg__QArmDiagnostics__Sequence *
qarm_interfaces__msg__QArmDiagnostics__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  qarm_interfaces__msg__QArmDiagnostics__Sequence * array = (qarm_interfaces__msg__QArmDiagnostics__Sequence *)allocator.allocate(sizeof(qarm_interfaces__msg__QArmDiagnostics__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = qarm_interfaces__msg__QArmDiagnostics__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
qarm_interfaces__msg__QArmDiagnostics__Sequence__destroy(qarm_interfaces__msg__QArmDiagnostics__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    qarm_interfaces__msg__QArmDiagnostics__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
qarm_interfaces__msg__QArmDiagnostics__Sequence__are_equal(const qarm_interfaces__msg__QArmDiagnostics__Sequence * lhs, const qarm_interfaces__msg__QArmDiagnostics__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!qarm_interfaces__msg__QArmDiagnostics__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
qarm_interfaces__msg__QArmDiagnostics__Sequence__copy(
  const qarm_interfaces__msg__QArmDiagnostics__Sequence * input,
  qarm_interfaces__msg__QArmDiagnostics__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(qarm_interfaces__msg__QArmDiagnostics);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    qarm_interfaces__msg__QArmDiagnostics * data =
      (qarm_interfaces__msg__QArmDiagnostics *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!qarm_interfaces__msg__QArmDiagnostics__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          qarm_interfaces__msg__QArmDiagnostics__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!qarm_interfaces__msg__QArmDiagnostics__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
