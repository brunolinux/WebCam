#include <string> 
#include <iostream>
#include <fstream>
#include <vector>
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/kernels/register.h"
#include <opencv2/opencv.hpp> 

#define IMAGE_MEAN 128.0f
#define IMAGE_STD 128.0f


bool ReadLines(const std::string& file_name, std::vector<std::string>* lines);
void FeedInMat(const cv::Mat& mat, TfLiteTensor *tensor);


int main() {    
    
    std::cout << "Start" << std::endl;

    std::string model_file("../../model/detect.tflite");
    std::string image_file("../test.bmp");
    std::string label_file("../../model/coco_labels_list.txt"); 


    std::cout << "Load file name" << std::endl;
    std::vector<std::string> labels; 
    if (!ReadLines(label_file, &labels)) exit(-1);
 

    std::unique_ptr<tflite::FlatBufferModel> model;
    std::unique_ptr<tflite::Interpreter> interpreter; 

    model = tflite::FlatBufferModel::BuildFromFile(model_file.c_str());     
    if (!model) {
        std::cerr << "Failed to load model:" << model_file << std::endl;
        exit(-1);
    } else { 
        std::cout << "Model file " << model_file << " is loaded!" << std::endl;       
    }

    tflite::ops::builtin::BuiltinOpResolver resolver;
    
    tflite::InterpreterBuilder(*model, resolver)(&interpreter);
    if (!interpreter) {
        std::cerr << "Failed to construct interpreter" << std::endl;
        exit(-1);
    }

    if (interpreter->AllocateTensors() != kTfLiteOk) {
        std::cerr << "Failed to allocate tensors!" << std::endl;
        exit(-1);
    }

    //interpreter->UseNNAPI(true);
    interpreter->SetNumThreads(4);

    int image_width = 300;
    int image_height = 300;
    int image_channels = 3; 

    // input tensor
    cv::Mat mat;
    mat = cv::imread(image_file);

    TfLiteTensor *input_tensor = interpreter->tensor(interpreter->inputs()[0]);

    if (image_width != mat.cols || image_height != mat.rows) {
        cv::Mat resized;
        cv::resize(mat, resized, cv::Size(image_width, image_height));
        cv::cvtColor(resized, resized, cv::COLOR_BGR2RGB);
        FeedInMat(resized, input_tensor);
    } else {
        cv::Mat for_tf;
        cv::cvtColor(mat, for_tf, cv::COLOR_BGR2RGB);
        FeedInMat(for_tf, input_tensor);
    }
    

    if(interpreter->Invoke() != kTfLiteOk) {
        std::cerr << "Failed to invoke tflite!" << std::endl; 
    }

    const std::vector<int> outputs = interpreter->outputs();

    std::cout << "outputs: " << std::endl; 
    for (auto i=outputs.begin(); i != outputs.end(); i++) { 
        std::cout << "Index of tensor: " << *i << std::endl; 
        std::cout << "tensor: " << *i << " type:" 
                  << interpreter->tensor(*i)->type  
                  << "   size:" << interpreter->tensor(*i)->dims->size
                  << std::endl;    
    } 

    const float* detection_locations = interpreter->typed_output_tensor<float>(0);
    const float* detection_classes = interpreter->typed_output_tensor<float>(1);
    const float* detection_scores = interpreter->typed_output_tensor<float>(2);
    const int num_detections  = *interpreter->typed_output_tensor<float>(3);

    for (int d = 0; d < num_detections; d++) {
        const std::string cls = labels[detection_classes[d]];
        const float score = detection_scores[d];
        const int ymin = detection_locations[4 * d] * mat.rows;
        const int xmin = detection_locations[4 * d + 1] * mat.cols;
        const int ymax = detection_locations[4 * d + 2] * mat.rows;
        const int xmax = detection_locations[4 * d + 3] * mat.cols;
        if (score < .3f) {
            std::cout << "Ignore detection " << d << " of '" << cls << "' with score " << score
                << " @[" << xmin << "," << ymin << ":" << xmax << "," << ymax << "]";
        } else {
            std::cout << "Detected " << d << " of '" << cls << "' with score " << score
                << " @[" << xmin << "," << ymin << ":" << xmax << "," << ymax << "]";
            cv::rectangle(mat, cv::Rect(xmin, ymin, xmax - xmin, ymax - ymin),
                          cv::Scalar(0, 0, 255), 1);
            cv::putText(mat, cls, cv::Point(xmin, ymin - 5),
                        cv::FONT_HERSHEY_COMPLEX, .8, cv::Scalar(10, 255, 30));
        }

    }
    
    cv::imwrite("posttest.bmp", mat);    

    std::cout << "Finished" << std::endl;

    return 0;
}

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



void FeedInMat(const cv::Mat& mat, TfLiteTensor *tensor) {
    switch (tensor->type) {
        case kTfLiteFloat32:
            {
                float* dst = tensor->data.f;
                const int row_elems = mat.cols * mat.channels();
                for (int row = 0; row < mat.rows; row++) {
                    const uchar* row_ptr = mat.ptr(row);
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
                const int row_elems = mat.cols * mat.channels();
                for (int row = 0; row < mat.rows; row++) {
                    memcpy(dst, mat.ptr(row), row_elems);
                    dst += row_elems;
                }
            }
            break;
        default:
            std::cerr << "Should not reach here!" << std::endl;
    }
}
