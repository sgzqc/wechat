cmake_minimum_required(VERSION 3.5.1)
project(fft_video)

set(CMAKE_CXX_STANDARD 14)

find_package(CUDA REQUIRED)
include(cudaCMake/FindCUDA.cmake)
set(CUDA_NVCC_FLAGS "${CUDA_NVCC_FLAGS} -Wno-deprecated-gpu-targets")
message(STATUS "CUDA library status:")
message(STATUS "    version: ${CUDA_VERSION}")
message(STATUS "    libraries: ${CUDA_LIBRARIES}")
message(STATUS "    libraries: ${CUDA_CUFFT_LIBRARIES}")
message(STATUS "    libraries: ${CUDA_nppc_LIBRARY}")
message(STATUS "    libraries: ${CUDA_npps_LIBRARY}")
message(STATUS "    libraries: ${CUDA_nppisu_LIBRARY}")
message(STATUS "    libraries: ${CUDA_nppicom_LIBRARY}")
message(STATUS "    libraries: ${CUDA_nppig_LIBRARY}")

#
set(CUDA_FILES
       ./fft.cu
        )
cuda_add_library(fft_cu STATIC ${CUDA_FILES} )


find_package(OpenCV REQUIRED)
message(STATUS "OpenCV library status:")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")

include_directories(
        ./include

        ${OpenCV_INCLUDE_DIRS}
        ${OpenCV_INCLUDE_DIRS}/opencv
        ${OpenCV_INCLUDE_DIRS}/opencv2
        ${CUDA_INCLUDE_DIRS}

)

add_executable(fft_video main.cpp

        )

target_link_libraries(fft_video PUBLIC
        ${OpenCV_LIBS}
        ${CUDA_LIBRARIES}
        ${CUDA_nppc_LIBRARY}
        ${CUDA_npps_LIBRARY}
        ${CUDA_nppisu_LIBRARY}
        ${CUDA_nppicom_LIBRARY}
        ${CUDA_nppig_LIBRARY}
        ${CUDA_nppial_LIBRARY}
        ${CUDA_nppicc_LIBRARY}
        ${CUDA_nppicom_LIBRARY}
        ${CUDA_CUFFT_LIBRARIES}
        fft_cu
        )