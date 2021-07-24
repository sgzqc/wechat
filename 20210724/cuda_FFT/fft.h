
#include "cuda_runtime.h"
#include "cufft.h"
#include <cuda.h>
#include "device_launch_parameters.h"
#include "cuda_runtime.h"




void fft_tranformer(uchar3 * d_8uc3,float2 * d_x,float2 * d_k,
                    uchar3* d_img,cufftHandle *fftPlan,
               unsigned char * pframe,unsigned  char * pDst,
               int width,int height,int size);



