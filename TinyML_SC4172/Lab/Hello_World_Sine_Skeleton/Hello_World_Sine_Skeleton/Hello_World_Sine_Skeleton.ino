/**
 * Test sinewave neural network model
 * 
 * Author: Pete Warden
 * Modified by: Shawn Hymel
 * Date: March 11, 2020
 * https://www.digikey.sg/en/maker/projects/intro-to-tinyml-part-2-deploying-a-tensorflow-lite-model-to-arduino/59bf2d67256f4b40900a3fa670c14330
 * 
 * Copyright 2019 The TensorFlow Authors. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.

 */

// Nanao Sense board use two vitual com ports - one during bootloader, and the other during application execution 
// Double press the reset button to put the arduino board into the bootloader state, indicate by the Yellow blinking LED
// AFter the programme is down load properly

// Import TensorFlow stuff
#include "TensorFlowLite.h"
#include "tensorflow/lite/micro/kernels/micro_ops.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/version.h"
#include "DebugLog.h"

// Our model
#include "cosine_model.h"

// #define DEBUG 1 //Figure out what's going on in our model. Check the DEBUG IF defines.
#define DEBUG 0 //Run the sine program 

// Some settings
// constexpr int led_pin = LED_BUILTIN;			  // output port pin for the LED, replace 'x' with pin connecting to led
constexpr int led_pin = 23;
constexpr float pi = 3.14159265;                  // pi
constexpr float freq = 0.5;                       // Frequency (Hz) of sinewave
constexpr float period = (1 / freq) * (1000000);  // Period (microseconds)

// TFLite globals, used for compatibility with Arduino-style sketches
namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model = nullptr;
  tflite::MicroInterpreter* interpreter = nullptr;
  TfLiteTensor* model_input = nullptr;
  TfLiteTensor* model_output = nullptr;

  // Create an area of memory to use for input, output, and other TensorFlow
  // arrays. You'll need to adjust this by combiling, running, and looking
  // for errors.
  constexpr int kTensorArenaSize = 5 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];
} // namespace

void setup() {

  // Wait for Serial to connect
  Serial.begin(9600);
#if DEBUG
  while(!Serial);
#endif

  // Let's make an LED vary in brightness
  pinMode(led_pin, OUTPUT);

  // Set up logging (will report to Serial, even within TFLite functions)
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  // Map the model into a usable data structure
  model = tflite::GetModel(cosine_model);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    error_reporter->Report("Model version does not match Schema");
    while(1);
  }
  
  // This pulls in the deep learning operations that  are needed for this program
  static tflite::MicroMutableOpResolver<3> micro_resolver(error_reporter);  // choice 2
  if (micro_resolver.AddFullyConnected() != kTfLiteOk) {
    return;
  }
  if (micro_resolver.AddQuantize() != kTfLiteOk) {
    return;
  }
  if (micro_resolver.AddDequantize() != kTfLiteOk) {
    return;
  }

  // Build an interpreter to run the model
  static tflite::MicroInterpreter static_interpreter(
//***    model, resolver, tensor_arena, kTensorArenaSize, error_reporter);   // choice 1 AllOpsResolver
  model, micro_resolver, tensor_arena, kTensorArenaSize, error_reporter);  // choice 2 micromutableOpResolver
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    error_reporter->Report("AllocateTensors() failed");
    while(1);
  }

  // Assign model input and output buffers (tensors) to pointers
  model_input = interpreter->input(0);
  model_output = interpreter->output(0);

} // setup

void loop() {

#if DEBUG
  unsigned long start_timestamp = micros();

  //**for testing
  float x_val = 0.7;  // sin(1.2) = 0.9,  sin(0.7) = 0.64, sin(pi) = 0
  //if (Serial.available())>0 // if value available
  //    x_val = Serial.parseFloat();
  model_input->data.f[0] = x_val; //Copy value to input buffer (tensor)
  // Run inference
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    error_reporter->Report("Invoke failed on input: %f\n", x_val);
  }
  // Read predicted y value from output buffer (tensor)
  float y_val = model_output->data.f[0];
  Serial.print("cos(");
  Serial.print(x_val);
  Serial.print(") = ");
  Serial.println(y_val);
  Serial.print("Time to execute inference (us): ");
  Serial.println(micros() - start_timestamp);

  delay(1000); 
#endif  

#if !DEBUG
  // Get current timestamp and modulo with period
  unsigned long timestamp = micros();
  timestamp = timestamp % (unsigned long)period;

  // Calculate x value to feed to the model and convert to radian
  float x_normal = (float)timestamp / period;
  float x_val = x_normal * 2.0 * pi;

  // Copy value to input buffer (tensor)
  model_input->data.f[0] = x_val;
  // Serial.println(model_input->type);   // 1 = float, 9 = int8


  // Run inference
  TfLiteStatus invoke_status = interpreter->Invoke();
  if (invoke_status != kTfLiteOk) {
    error_reporter->Report("Invoke failed");
    return;
  }

  // Read predicted y value from output buffer (tensor)
  float y_val = model_output->data.f[0];

  // Translate to a PWM LED brightness
  int brightness = (int)(127.5 * (y_val + 1.0));
  analogWrite(led_pin, brightness);

  // Print value
  Serial.print("x: ");
  Serial.print(x_val);
  Serial.print("\tPredicted y: ");
  Serial.println(y_val);
  delay(20);
#endif // !DEBUG

}
