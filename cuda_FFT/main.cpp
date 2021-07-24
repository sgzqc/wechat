#include <iostream>
#include <string>
#include<opencv2/opencv.hpp>
#include "fft.h"
using namespace  std;


int test_video()
{
    string video_name = "./badapple.mp4";
    cv::VideoCapture vc(video_name);
    double fps = vc.get(CV_CAP_PROP_FPS);
    int width = int(vc.get(CV_CAP_PROP_FRAME_WIDTH));
    int height = int(vc.get(CV_CAP_PROP_FRAME_HEIGHT));

    int size = 1024;
    cv::Mat frame(height, width, CV_8UC3, cv::Scalar(0, 0, 0));
    cv::Mat ff(size, size, CV_8UC3, cv::Scalar(0, 0, 0));
    cv::VideoWriter writer;
    writer.open("./badapplek.mp4", cv::VideoWriter::fourcc('a', 'v', 'c', '1'), fps, cv::Size(size, size));

    if(!vc.isOpened())
    {
       std::cout<<"Read video failed.."<<std::endl;
       return -1;
    }

    cufftHandle fftPlan;
    cufftPlan2d(&fftPlan, size, size, CUFFT_C2C);
    float2* d_x, *d_k;
    uchar3* d_8uc3, *d_img;
    cudaMalloc(&d_x, width * 2 * height * 2 * sizeof(float2));
    cudaMalloc(&d_k, width * 2 * height * 2 * sizeof(float2));
    cudaMalloc(&d_8uc3, width * height * 3);
    cudaMalloc(&d_img, width * 2 * height * 2 * 3);

    int cnt = 0;
    while(vc.read(frame  ))
    {
        if(cnt % 100 ==0)
        {
            std::cout<< "Process frame="<< cnt <<" width="<<frame.cols << " and height="<<frame.rows << std::endl;
        }
        unsigned  char *pSrc = frame.ptr<uchar>(0);
        unsigned  char * pDst = ff.ptr<uchar>(0);

        fft_tranformer(d_8uc3, d_x,d_k,
                       d_img,&fftPlan,
                       pSrc,pDst,
                       width,height,size);

        cv::Mat small_img = ff(cv::Rect(0,0,320,240));
        cv::resize(frame,small_img,cv::Size(320,240));
        writer << ff;
        cnt ++;
    }
    vc.release();
    writer.release();
    return 0;

}

void test_img()
{
    string img_name = "./16--94_color.jpg";
    cv::Mat frame = cv::imread(img_name);
    int width = frame.cols;
    int height = frame.rows;

    int size = 1024;
    cv::Mat ff(size, size, CV_8UC3, cv::Scalar(0, 0, 0));

    cufftHandle fftPlan;
    cufftPlan2d(&fftPlan, size, size, CUFFT_C2C);
    float2* d_x, *d_k;
    uchar3* d_8uc3, *d_img;
    cudaMalloc(&d_x, width * 2 * height * 2 * sizeof(float2));
    cudaMalloc(&d_k, width * 2 * height * 2 * sizeof(float2));
    cudaMalloc(&d_8uc3, width * height * 3);
    cudaMalloc(&d_img, width * 2 * height * 2 * 3);

    unsigned  char *pSrc = frame.ptr<uchar>(0);
    unsigned  char * pDst = ff.ptr<uchar>(0);
    fft_tranformer(d_8uc3, d_x,d_k,
                       d_img,&fftPlan,
                       pSrc,pDst,
                       width,height,size);

    cv::Mat small_img,out_img;
    cv::resize(ff,small_img,cv::Size(width,height));
    cv::hconcat(frame,small_img,out_img);

    cv::imwrite("./out3.jpg",out_img);

}

int main()
{
   //test_video();
   test_img();
   return 0;
}
