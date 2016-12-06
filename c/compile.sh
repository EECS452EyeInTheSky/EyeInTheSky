gcc -Wall -fPIC $1.c
gcc -shared -o $1.so $1.o

