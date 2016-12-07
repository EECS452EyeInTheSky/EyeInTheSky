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
const Pixel GREEN   = { 0,     200,    0   };
const Pixel YELLOW  = { 0,      240,    255};

int blue_pixel_difference(Pixel a, Pixel b)
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
    total = total * 2;

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

int red_pixel_difference(Pixel a, Pixel b)
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
        total += 2*(a.r - b.r);
    }
    else
    {
        total += 2*( b.r - a.r);
    }
    //a.b -= b.b;
    //a.r -= b.r;
    //a.g -= b.g;
    //total += a.b >= 0 ? a.b : -a.b;
    //total += a.g >= 0 ? a.g : -a.g;
    //total += a.r >= 0 ? a.r : -a.r;
    
    return total;
}

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
    unsigned old = 999999;
    
    Point target = { 0 };
    for (ix = x_low; ix < x_high; ix+=2)
    {
        for (iy = y_low; iy < y_high; iy+=2)
        {
            Pixel p = img[ix*NUM_COL + iy];
//            printf("Pixel values: (b, g, r) (%3d, %3d, %3d)", p.b, p.g, p.r);
            if (p.b > p.g && p.b > p.r)
            {
               unsigned pDist = blue_pixel_difference(p, BLUE);     
               if (pDist < old)
               {
//                    printf("Pixel values: (b, g, r) (%3d, %3d, %3d)\n", p.b, p.g, p.r);
                    old = pDist;
                    target.y = ix;
                    target.x = iy;
               }
            }
        }
    }
    return target;
}

Point c_greenest(Pixel * img, unsigned x_low, unsigned x_high, unsigned y_low, unsigned y_high)
{
    unsigned ix;
    unsigned iy;
    unsigned old = 9999;
    Point target = { 0 };
    for (ix = x_low; ix < x_high; ix+= 5)
    {
        for (iy = y_low; iy < y_high; iy += 5)
        {
            Pixel p = img[ix*NUM_COL + iy];
            if (p.g > p.b && p.g > p.r)
            {
                unsigned pDist = pixel_difference(p, GREEN);
                if (pDist < old)
                {
                    old = pDist;
                    target.y = ix;
                    target.x = iy;
                }
            }
        }
    }
    return target;
}

Point c_redest(Pixel * img, unsigned x_low, unsigned x_high, unsigned y_low, unsigned y_high)
{
    unsigned ix;
    unsigned iy;
    unsigned old = 9999;
    Point target = { 0 };
    for (ix = x_low; ix < x_high; ix+= 5)
    {
        for (iy = y_low; iy < y_high; iy += 5)
        {
            Pixel p = img[ix*NUM_COL + iy];
            if (p.r > p.b && p.r > p.g)
            {
                unsigned pDist = red_pixel_difference(p, RED);
                if (pDist < old)
                {
                    old = pDist;
                    target.y = ix;
                    target.x = iy;
                }
            }
        }
    }
    return target;
}

Point c_yellowest(Pixel * img, unsigned x_low, unsigned x_high, unsigned y_low, unsigned y_high)
{
    unsigned ix;
    unsigned iy;
    unsigned old = 9999;
    Point target = { 0 };
    for (ix = x_low; ix < x_high; ix+= 5)
    {
        for (iy = y_low; iy < y_high; iy += 5)
        {
            Pixel p = img[ix*NUM_COL + iy];
            unsigned pDist = pixel_difference(p, YELLOW);
            if (pDist < old)
            {
                old = pDist;
                target.y = ix;
                target.x = iy;
            }
        }
    }
    return target;
}
