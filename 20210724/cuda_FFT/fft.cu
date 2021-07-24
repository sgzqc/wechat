#include "fft.h"
#include "cuda_runtime.h"

__device__ unsigned char getr(float x) {
    return (tanh((x - 0.375f) * 6.0f) + 1.0f) * 127.0f;
}
__device__ unsigned char getg(float x) {
    return (tanh((x - 0.6250f) * 6.0f) + 1.0f) * 127.0f;
}
__device__ unsigned char getb(float x) {
    return (exp(-20.0f * (x - 0.25f) * (x - 0.25f) - 2.0f * exp(-(x + 0.05f) * (x + 0.05f) * 144.0f)) * 0.5f + 1.0f + tanh((x - 0.875f) * 6.0f)) * 127.0f;
}
__global__ void imgfill(float2* d_k, uchar3* d_img,int size)
{
    int x = threadIdx.x + blockIdx.x * blockDim.x;
    int y = threadIdx.y + blockIdx.y * blockDim.y;
    int imgx, imgy;
    imgx = (x >= size / 2) ? x - size / 2 : x + size / 2;
    imgy = (y >= size / 2) ? y - size / 2 : y + size / 2;
    float2 k = d_k[y * size + x];
    float in = k.x * k.x + k.y * k.y;
    in = log(in * (1.0f / 256.0f/size) + 0.8f) * 0.07f;
    uchar3 c;
    c.x = getb(in);
    c.y = getg(in);
    c.z = getr(in);
    d_img[imgy * size + imgx] = c;
}

__global__ void fill(float2* d_x, uchar3* d_8uc3,int size,int w,int h) {
    int x = threadIdx.x + blockIdx.x * blockDim.x;
    int y = threadIdx.y + blockIdx.y * blockDim.y;
    int imgx, imgy;
    float cx, cy;
    unsigned char r;
    if (x >= size / 2 + w / 2) {
        imgx = 0;
        cx = size - x;
        cx = exp(-cx * cx * (1.0f / 1024.0f));
    }
    else if (x < size / 2 + w / 2 && x >= w) {
        imgx = w - 1;
        cx = x - w;
        cx = exp(-cx * cx * (1.0f / 1024.0f));
    }
    else {
        imgx = x;
        cx = 1.0f;
    }

    if (y >= size / 2 + h / 2) {
        imgy = 0;
        cy = size - y;
        cy = exp(-cy * cy * (1.0f / 1024.0f));
    }
    else if (y < size / 2 + h / 2 && y >= h) {
        imgy = h - 1;
        cy = y - h;
        cy = exp(-cy * cy * (1.0f / 1024.0f));
    }
    else {
        imgy = y;
        cy = 1.0f;
    }
    r = d_8uc3[imgy * w + imgx].x;
    d_x[y * size + x].x = r * cx * cy;
    d_x[y * size + x].y = 0;
}


void fft_tranformer(uchar3 * d_8uc3,float2 * d_x,float2 * d_k,
                    uchar3 *d_img,cufftHandle *fftPlan,
                    unsigned char * pframe,unsigned  char * pDst,
                    int width,int height,int size)
{
    cudaMemcpy(d_8uc3, pframe, width * height * 3, cudaMemcpyHostToDevice);
    fill << < dim3(size / 128, size, 1), dim3(128, 1, 1) >> > (d_x, d_8uc3,size,width,height);
    cufftExecC2C(*fftPlan, d_x, d_k, CUFFT_FORWARD);
    imgfill << < dim3(size / 128, size, 1), dim3(128, 1, 1) >> > (d_k, d_img,size);
    cudaMemcpy(pDst, d_img, size * size * 3, cudaMemcpyDeviceToHost);
}