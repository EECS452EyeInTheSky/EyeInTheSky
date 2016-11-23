sudo hciconfig hci0 up
while [ 1 ]; do
    
    sudo rfcomm connnect /dev/rfcomm0 $MAC
    
