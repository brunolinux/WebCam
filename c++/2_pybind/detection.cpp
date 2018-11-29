#include "detection.h"
#include <iostream>
#include <fstream>
#include <algorithm>

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


Detection::Detection(const std::string &model, const std::string &label, int thread)
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
    m_interpreter->SetNumThreads(thread);

    // Find input tensors.
    if (m_interpreter->inputs().size() != 1) {
        std::cerr << "Graph needs to have 1 and only 1 input!" << std::endl;
    }

    // input tensor
    m_input_tensor = m_interpreter->tensor(m_interpreter->inputs()[0]);


    // output pointer
    const std::vector<int> outputs = m_interpreter->outputs();
    m_detection_locations = m_interpreter->tensor(outputs.at(0));
    m_detection_classes = m_interpreter->tensor(outputs.at(1));
    m_detection_scores = m_interpreter->tensor(outputs.at(2));
    m_num_detections  = m_interpreter->tensor(outputs.at(3));

    m_output = std::make_shared<OutputInfo>();
}


// frame object detection
void Detection::frameDetect(py::array_t<uint8_t> &input) {
    assert(input.nbytes() == m_input_tensor.bytes);

    FeedInMat(input, m_input_tensor);

    if(m_interpreter->Invoke() != kTfLiteOk) {
        throw std::runtime_error("Failed to invoke tflite!");
    }



    m_output->clear();
    int num = 0;

/*
    std::cout << m_num_detections->bytes / sizeof(float) << std::endl;
    std::cout << m_detection_classes->bytes/sizeof(float) << std::endl;
    std::cout << m_detection_scores->bytes/sizeof(float) << std::endl;
    std::cout << m_detection_locations->bytes/sizeof(float)/4 << std::endl;
*/ 
    int num_detection = (int)(m_num_detections->data.f[0]);
    //std::cout << num_detection << "\t"; 
    for (int d = 0; d < num_detection; d++) {
        if (m_detection_scores->data.f[d] < m_threshold) continue;            

        
        m_output->classes.push_back(m_labels[m_detection_classes->data.f[d]]);
        m_output->scores.push_back(m_detection_scores->data.f[d]);
        m_output->locations.push_back(m_detection_locations->data.f[4 * d]);
        m_output->locations.push_back(m_detection_locations->data.f[4 * d + 1]);
        m_output->locations.push_back(m_detection_locations->data.f[4 * d + 2]);
        m_output->locations.push_back(m_detection_locations->data.f[4 * d + 3]);

        num++;
    }    

    m_output->numbers = num;
    return;
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

