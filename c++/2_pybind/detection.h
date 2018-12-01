#pragma once 

#include <string>
#include "tensorflow/lite/model.h"
#include "tensorflow/lite/kernels/register.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h> 

namespace py = pybind11;


struct OutputInfo{
    OutputInfo () {
        clear();    
    }

    std::vector<float> locations;
    std::vector<std::string> classes; 
    std::vector<float> scores;
    int numbers = 0; 

    void clear() { 
        locations.clear();
        classes.clear();
        scores.clear();
        numbers = 0;
    };
} ;


class Detection {

public:
    Detection(const std::string &model, const std::string &label, int thread);
    
    void frameDetect(py::array_t<uint8_t> &input, OutputInfo &output);

    int width() const {
        return m_input_tensor->dims->data[2];
    }

    int height() const {
        return m_input_tensor->dims->data[1];
    }

    int input_channels() const {
        return m_input_tensor->dims->data[3];
    }

    double get_threshold() const {
        return m_threshold;
    } 

    void set_threshold(double threshold) { 
        m_threshold = threshold;
    }

private: 
    void FeedInMat(py::array_t<uint8_t> &input, TfLiteTensor *tensor);

    std::unique_ptr<tflite::FlatBufferModel> m_model;
    std::unique_ptr<tflite::Interpreter> m_interpreter;
    std::vector<std::string> m_labels;

    TfLiteTensor* m_input_tensor = nullptr;


    TfLiteTensor* m_detection_locations = nullptr;
    TfLiteTensor* m_detection_classes = nullptr;
    TfLiteTensor* m_detection_scores = nullptr;
    TfLiteTensor* m_num_detections  = nullptr;   


    double m_threshold = 0.5; 
};




PYBIND11_MODULE(detection, m) {
    py::class_<Detection>(m, "Detection")
        .def(py::init<const std::string &, const std::string &, int>())
        .def("frameDetect", &Detection::frameDetect)
        .def("width", &Detection::width)
        .def("height", &Detection::height)
        .def("channel", &Detection::input_channels)
        .def_property("threshold", &Detection::get_threshold, &Detection::set_threshold);

    py::class_<OutputInfo>(m, "OutputInfo")
        .def(py::init())
        .def_readwrite("locations", &OutputInfo::locations)
        .def_readwrite("classes", &OutputInfo::classes)
        .def_readwrite("scores", &OutputInfo::scores)
        .def_readwrite("numbers", &OutputInfo::numbers);
}

