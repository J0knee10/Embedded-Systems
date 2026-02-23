#include <PDM.h>
#include <arduinoFFT.h>
#include <math.h>

#include <TensorFlowLite.h>
#include <tensorflow/lite/micro/all_ops_resolver.h>
#include <tensorflow/lite/micro/micro_error_reporter.h>
#include <tensorflow/lite/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>

#include "audio_gender_classification_model.h" // Include your TFLite model as a C array
#include "mel_filter_bank.h"                   // Include the Mel filter bank as a C array

// Audio Parameters
#define SAMPLE_RATE 16000  // 16kHz sampling
#define FRAME_SIZE 512     // 32ms frame size
#define HOP_LENGTH 256     // Hop length (overlap between frames)
#define NUM_FRAMES 200     // Number of frames to store
#define NUM_MFCC 13        // Number of MFCC coefficients
#define NUM_MEL_FILTERS 26 // Number of Mel filters

// Model Parameters
#define NUM_CLASSES 2 // Female, Male

// Audio Buffer
#define BUFFER_SIZE FRAME_SIZE + (HOP_LENGTH * (NUM_FRAMES - 1))
int16_t audio_buffer[BUFFER_SIZE];
volatile bool isBufferFull = false;
volatile bool isUsingInputTensor = false;
int bufferIndex = 0;

// FFT Setup
ArduinoFFT<float> FFT;
float real[FRAME_SIZE];
float imag[FRAME_SIZE];

// global variables used for TensorFlow Lite (Micro)
tflite::MicroErrorReporter tflErrorReporter;
constexpr int tensorArenaSize = 70 * 1024;
uint8_t tensor_arena[tensorArenaSize];
tflite::MicroInterpreter* interpreter = nullptr;
const tflite::Model *model = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;

void setup()
{
    Serial.begin(115200);
    while (!Serial)
        ;

    if (Serial)
    {
        Serial.println("Serial initialized.");
    }

    // Set callback before begin
    PDM.onReceive(onPDMdata);
    PDM.setGain(0);

    if (!PDM.begin(1, SAMPLE_RATE))
    {
        Serial.println("Failed to start PDM!");
        while (1)
            ;
    }
    else
    {
        Serial.println("PDM initialized.");
    }

    // Load TFLite model
    model = tflite::GetModel(audio_gender_classification_model);
    if (model->version() != TFLITE_SCHEMA_VERSION)
    {
        Serial.println("Model schema mismatch!");
        return;
    }

    static tflite::AllOpsResolver resolver;

    // Create Interpreter
    interpreter = new tflite::MicroInterpreter(model, resolver, tensor_arena, tensorArenaSize, &tflErrorReporter);
  
    // Allocate memory from the tensor_arena for the model's tensors
    if (interpreter->AllocateTensors() != kTfLiteOk)
    {
        Serial.println("AllocateTensors() failed");
        return;
    }

    input = interpreter->input(0);
    output = interpreter->output(0);
}

void loop()
{
    if (isBufferFull && !isUsingInputTensor)
    {
        isUsingInputTensor = true;
        processBuffer();
        isUsingInputTensor = false;
    }
}

void onPDMdata()
{
    /* Callback function to handle PDM data. */

    int bytesAvailable = PDM.available();
    if (bytesAvailable > 0)
    {
        int16_t pdmBuffer[bytesAvailable / 2];
        int samplesRead = PDM.read(pdmBuffer, bytesAvailable) / 2;

        for (int i = 0; i < samplesRead; i++)
        {
            if (!isBufferFull)
            {
                audio_buffer[bufferIndex] = pdmBuffer[i];
                bufferIndex++;

                // If the buffer is full,
                if (bufferIndex >= BUFFER_SIZE)
                {
                    isBufferFull = true; // indicate ready for processing
                    bufferIndex = 0;     // reset for next round
                }
            }
        }
    }
}

void processBuffer()
{
    /* Process the audio buffer. */

    Serial.println("Processing buffer.");

    // Find the max value in the audio buffer
    int16_t maxVal = 0;
    for (int i = 0; i < BUFFER_SIZE; i++)
    {
        int16_t absValue = abs(audio_buffer[i]);
        if (absValue > maxVal)
        {
            maxVal = absValue; // Ensure maxVal is the largest absolute value
        }
    }

    // Process and save frames to input tensor
    for (int i = 0; i < NUM_FRAMES; i++)
    {
        // Create a frame from the audio buffer
        float frame[FRAME_SIZE];
        for (int j = 0; j < FRAME_SIZE; j++)
        {
            frame[j] = (float)audio_buffer[i * HOP_LENGTH + j];
        }

        if (maxVal > 0)
        {
            // Normalize the audio buffer
            for (int n = 0; n < FRAME_SIZE; n++)
            {
                frame[n] = frame[n] / (float)maxVal;
            }
        }

        // Compute MFCCs for the frame
        float mfcc[NUM_MFCC];
        computeMFCC(frame, mfcc, FRAME_SIZE);

        // Copy the MFCCs to the input tensor with offset for each frame
        for (int k = 0; k < NUM_MFCC; k++)
        {
            // Input tensor is of shape: [1, 13, 500, 1]
            // Flatbuffer: [MFCC0_frame0, MFCC0_frame1, ..., MFCC0_frame499, MFCC1_frame0, MFCC1_frame1, ..., MFCC1_frame499, ...]
            // Copy the MFCC to the correct location for each frame, using frame index of frameCount
            input->data.f[k * NUM_FRAMES + i] = mfcc[k]; // i is the frame index
        }
    }

    // Audio buffer already copied to input tensor
    isBufferFull = false;

    // Run inference
    runInference();
}

void runInference()
{
    /* Run inference on the input tensor. */
    Serial.println("Running inference.");

    TfLiteStatus invokeStatus = interpreter->Invoke();
    if (invokeStatus != kTfLiteOk)
    {
        Serial.println("Invoke failed");
        return;
    }

    float score = output->data.f[0]; // Use the single score from the output
    float confidence;

    // Classify based on the score (sigmoid output)
    Serial.print("Predicted gender: ");
    if (score < 0.5) // If the score is < 0.5, classify as Female
    {
        Serial.println("Female");
        confidence = (1.0f - score) * 100;
    }
    else // If the score is > 0.5, classify as Male
    {
        Serial.println("Male");
        confidence = score * 100;
    }

    // Print the score
    Serial.print("Confidence: ");
    Serial.print(confidence, 2);
    Serial.println("%");
    Serial.println("");

    // Clear or reset the input tensor
    memset(input->data.f, 0, input->bytes); // set all bytes of the input tensor to zero
}

void computeMFCC(float *frame, float *mfcc, int frameSize)
{
    /* Compute MFCCs for a single frame.*/

    // Step 1: Apply Hanning window
    for (int i = 0; i < frameSize; i++)
    {
        frame[i] *= 0.5f * (1 - cos(2 * M_PI * i / (frameSize - 1))); // Hanning window

        real[i] = frame[i]; // Copy audio data to real part
        imag[i] = 0.0f;     // Initialize imaginary part to zero
    }

    // Step 2: Perform FFT
    FFT.compute(real, imag, frameSize, FFT_FORWARD);

    // Step 3: Compute power spectrum (square of magnitudes)
    float powerSpectrum[frameSize / 2];
    for (int i = 0; i < frameSize / 2; i++)
    {
        powerSpectrum[i] = real[i] * real[i] + imag[i] * imag[i];
    }

    // Step 4: Apply Mel filter bank
    float melSpectrum[NUM_MEL_FILTERS] = {0.0f};
    for (int filter = 0; filter < NUM_MEL_FILTERS; filter++)
    {
        for (int bin = 0; bin <= frameSize / 2; bin++)
        {
            melSpectrum[filter] += mel_filter_bank[filter][bin] * powerSpectrum[bin];
        }
    }

    // Step 4.5: Convert to log scale
    for (int filter = 0; filter < NUM_MEL_FILTERS; filter++)
    {
        if (melSpectrum[filter] != 0)
        {
            melSpectrum[filter] = 10 * log10(melSpectrum[filter]);
        }
    }

    // Step 5: Compute DCT
    for (int i = 0; i < NUM_MFCC; i++)
    {
        mfcc[i] = 0.0f;
        for (int j = 0; j < NUM_MEL_FILTERS; j++)
        {
            mfcc[i] += melSpectrum[j] * cos(M_PI * i * (2 * j + 1) / (2 * NUM_MEL_FILTERS));
        }
    }

    // Step 6: Apply orthonormal normalization
    mfcc[0] *= sqrt(1.0f / NUM_MEL_FILTERS); // scale the first coefficient
    for (int i = 1; i < NUM_MFCC; i++)
    {
        mfcc[i] *= sqrt(2.0f / NUM_MEL_FILTERS);
    }
}
