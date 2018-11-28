#include "detection.h"
#include <iostream>
#include <fstream>

#define IMAGE_MEAN 128.0f
#define IMAGE_STD 128.0f


bool ReadLines(const std::string& file_name, std::vector<std::string>* lines) {
    std::ifstream file(file_name);
    if (!file) {
        std::cerr << "Failed to open file " << file_name;
        return false;
    }
    std::string line;
    while (std::getline(file, line)) lines->push_back(line);
    return true;
}


Detection::Detection(const std::string &model, const std::string &label)
{ 
    if (!ReadLines(label, &m_labels)) exit(-1);

    m_model = tflite::FlatBufferModel::BuildFromFile(model.c_str());     
    if (!m_model) {
        std::cerr << "Failed to load model:" << model << std::endl;
        exit(-1);
    } 

    tflite::ops::builtin::BuiltinOpResolver resolver;
    
    tflite::InterpreterBuilder(*m_model, resolver)(&m_interpreter);

    if (!m_interpreter) {
        std::cerr << "Failed to construct interpreter" << std::endl;
        exit(-1);
    }

    if (m_interpreter->AllocateTensors() != kTfLiteOk) {
        std::cerr << "Failed to allocate tensors!" << std::endl;
        exit(-1);
    }    

    //m_interpreter->UseNNAPI(true);
    m_interpreter->SetNumThreads(4);

    // Find input tensors.
    if (m_interpreter->inputs().size() != 1) {
        std::cerr << "Graph needs to have 1 and only 1 input!" << std::endl;
    }

    // input tensor
    m_input_tensor = m_interpreter->tensor(m_interpreter->inputs()[0]);


    // output pointer
    const std::vector<int> outputs = m_interpreter->outputs();
    m_detection_locations = m_interpreter->tensor(outputs.at(0))->data.f;
    m_detection_classes = m_interpreter->tensor(outputs.at(1))->data.f;
    m_detection_scores = m_interpreter->tensor(outputs.at(2))->data.f;
    m_num_detections  = m_interpreter->tensor(outputs.at(3))->data.f;
}


// frame object detection
OutputInfo Detection::frameDetect(py::array_t<uint8_t> &input) {
    FeedInMat(input, m_input_tensor);


    if(m_interpreter->Invoke() != kTfLiteOk) {
        throw std::runtime_error("Failed to invoke tflite!");
    }

    //
    OutputInfo output; 
    int num = 0;

    for (int d = 0; d < (int)(*m_num_detections); d++) {
        //std::cout << "num :" << d << std::endl;
        if (m_detection_scores[d] < m_threshold) continue;            


        output.classes.push_back(m_labels[m_detection_classes[d]]);
        output.scores.push_back(m_detection_scores[d]);
        output.locations.push_back(m_detection_locations[4 * d]);
        output.locations.push_back(m_detection_locations[4 * d + 1]);
        output.locations.push_back(m_detection_locations[4 * d + 2]);
        output.locations.push_back(m_detection_locations[4 * d + 3]);

        num++;
    }    

    output.numbers = num;
    return output;
}



void Detection::FeedInMat(py::array_t<uint8_t> &input, TfLiteTensor *tensor) {
    switch (tensor->type) {
        case kTfLiteFloat32:
            {
                float* dst = tensor->data.f;
                const int row_elems = input.shape(1) * input.shape(2);
                for (int row = 0; row < input.shape(0); row++) {
                    const uint8_t* row_ptr = input.data(row * row_elems);
                    for (int i = 0; i < row_elems; i++) {
                        dst[i] = (row_ptr[i] - IMAGE_MEAN) / IMAGE_STD;
                    }
                    dst += row_elems;
                }
            }
            break;
        case kTfLiteUInt8:
            {
                uint8_t* dst = tensor->data.uint8;
                memcpy(dst, input.data(), input.nbytes());
                //dst = input.data();
            }
            break;
        default:
            std::cerr << "Should not reach here!" << std::endl;
    }
}

