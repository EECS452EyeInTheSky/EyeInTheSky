#include <stdio.h>

#define NUM_COL 1600
#define NUM_ROW 1400

void test_method()
{
    printf("Test!\n");
}


typedef struct Pixel
{
    unsigned char b;
    unsigned char g;
    unsigned char r;
} Pixel;

typedef struct Point
{
    unsigned x;
    unsigned y;
} Point;

const Pixel BLUE    = { 255,    0,      0   };
const Pixel RED     = { 80,     0,      255 };
const Pixel GREEN   = { 90,     160,    0   };
const Pixel YELLOW  = { 0,      200,    150 };

int pixel_difference(Pixel a, Pixel b)
{
    int total = 0;
    if (a.b > b.b)
    {
        total += a.b - b.b;
    }
    else
    {
        total += b.b - a.b; 
    }

    if (a.g > b.g)
    {
        total += a.g - b.g;
    }
    else
    {
        total += b.g - a.g;
    }

    if (a.r > b.r)
    {
        total += a.r - b.r;
    }
    else
    {
        total += b.r - a.r;
    }
    //a.b -= b.b;
    //a.r -= b.r;
    //a.g -= b.g;
    //total += a.b >= 0 ? a.b : -a.b;
    //total += a.g >= 0 ? a.g : -a.g;
    //total += a.r >= 0 ? a.r : -a.r;
    
    return total;
}

Point c_bluest(Pixel * img, unsigned x_low, unsigned x_high, unsigned y_low, unsigned y_high)
{
    unsigned ix;
    unsigned iy;
    unsigned old;
    
    Point target = { 0 };
    for (ix = x_low; ix <= x_high; ix++)
    {
        for (iy = y_low; iy <= y_high; iy++)
        {
            Pixel p = img[ix*NUM_COL + iy];
            if (p.b > p.g && p.b > p.r)
            {
               unsigned pDist = pixel_difference(p, BLUE);     
               if (pDist < old)
               {
                    old = pDist;
                    target.x = ix;
                    target.y = iy;
               }
            }
        }
    }
    return target;
}
