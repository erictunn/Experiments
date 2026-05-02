#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>

#include <algorithm>
#include <atomic>
#include <cmath>
#include <thread>
#include <vector>

namespace {
constexpr double kEscapeRadiusSquared = 4.0;
constexpr double kLog2 = 0.69314718055994530942;

void compute_rows(
    float* output,
    int x_res,
    int y_res,
    double x_min,
    double x_step,
    double y_min,
    double y_step,
    int max_iterations,
    std::atomic<int>& next_row,
    int chunk_size
) {
    for (;;) {
        const int row_start = next_row.fetch_add(chunk_size, std::memory_order_relaxed);
        // Loop until all rows are processed
        if (row_start >= y_res) {
            return;
        }

        const int row_end = std::min(row_start + chunk_size, y_res);
        for (int py = row_start; py < row_end; ++py) {
            const double c_y = y_min + static_cast<double>(py) * y_step;
            float* row = output + static_cast<std::size_t>(py) * static_cast<std::size_t>(x_res);

            double c_x = x_min;
            for (int px = 0; px < x_res; ++px, c_x += x_step) {
                const double shifted_x = c_x - 0.25;
                const double q = shifted_x * shifted_x + c_y * c_y;
                const bool in_main_cardioid = q * (q + shifted_x) <= 0.25 * c_y * c_y;
                const bool in_period_two_bulb = (c_x + 1.0) * (c_x + 1.0) + c_y * c_y <= 0.0625;
                if (in_main_cardioid || in_period_two_bulb) {
                    row[px] = 0.0f;
                    continue;
                }

                double zx = 0.0;
                double zy = 0.0;
                double zx2 = 0.0;
                double zy2 = 0.0;
                int iteration = 0;

                while (zx2 + zy2 < kEscapeRadiusSquared && iteration < max_iterations) {
                    zy = 2.0 * zx * zy + c_y;
                    zx = zx2 - zy2 + c_x;
                    zx2 = zx * zx;
                    zy2 = zy * zy;
                    ++iteration;
                }

                if (iteration == max_iterations) {
                    row[px] = 0.0f;
                    continue;
                }

                const double magnitude = std::sqrt(zx2 + zy2);
                row[px] = static_cast<float>(
                    iteration + 1.0 - std::log(std::log(magnitude)) / kLog2
                );
            }
        }
    }
}

PyObject* generate_mandelbrot(PyObject* /*self*/, PyObject* args) {
    double x_min = 0.0;
    double x_max = 0.0;
    double y_min = 0.0;
    double y_max = 0.0;
    int x_res = 0;
    int y_res = 0;
    int max_iterations = 0;

    if (!PyArg_ParseTuple(args, "ddddiii", &x_min, &x_max, &y_min, &y_max, &x_res, &y_res, &max_iterations)) {
        return nullptr;
    }
    // Validate input parameters
    if (x_res <= 0 || y_res <= 0) {
        PyErr_SetString(PyExc_ValueError, "Resolution must be positive.");
        return nullptr;
    }
    if (max_iterations <= 0) {
        PyErr_SetString(PyExc_ValueError, "max_iterations must be positive.");
        return nullptr;
    }

    npy_intp dims[2] = {y_res, x_res};
    PyObject* array = PyArray_SimpleNew(2, dims, NPY_FLOAT32);
    if (array == nullptr) {
        return nullptr;
    }

    auto* output = static_cast<float*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(array)));
    const double x_step = (x_max - x_min) / static_cast<double>(x_res);
    const double y_step = (y_max - y_min) / static_cast<double>(y_res);

    const unsigned int raw_worker_count = std::thread::hardware_concurrency();
    const unsigned int worker_count = std::max(
        1u,
        std::min(raw_worker_count == 0 ? 1u : raw_worker_count, static_cast<unsigned int>(y_res))
    );
    const int chunk_size = std::max(1, y_res / static_cast<int>(worker_count * 4));

    std::atomic<int> next_row{0};
    std::vector<std::thread> workers;
    workers.reserve(worker_count);

    Py_BEGIN_ALLOW_THREADS
    for (unsigned int i = 0; i < worker_count; ++i) {
        workers.emplace_back(
            compute_rows,
            output,
            x_res,
            y_res,
            x_min,
            x_step,
            y_min,
            y_step,
            max_iterations,
            std::ref(next_row),
            chunk_size
        );
    }

    for (auto& worker : workers) {
        worker.join();
    }
    Py_END_ALLOW_THREADS

    return array;
}

// Module definition
PyMethodDef module_methods[] = {
    {"generate", generate_mandelbrot, METH_VARARGS, "Generate a Mandelbrot image."},
    {nullptr, nullptr, 0, nullptr},
};

// Module definition structure
PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "mandel_lib",
    "Fast Mandelbrot generator.",
    -1,
    module_methods,
};
}  // namespace

// Module initialization function
PyMODINIT_FUNC PyInit_mandel_lib(void) {
    import_array();
    return PyModule_Create(&module_def);
}
