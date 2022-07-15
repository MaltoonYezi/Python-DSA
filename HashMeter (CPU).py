import hashlib
from time import time

#Value that we hash
field_order = int(str(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F), 16)

#time variables
timeOne = time()
timeTwo=0

#Measures how many iterations has been done already
counter = 0

#Initial hashing
m=hashlib.sha256(str(field_order).encode('utf-8')).hexdigest()

while True:
    m=hashlib.sha256(str(m).encode('utf-8')).hexdigest()
    counter+=1
    timeTwo = time()
    if (timeTwo-timeOne) >=10:
        print("The hash speed is: ", counter/(timeTwo-timeOne), "h/s")
        timeOne = time()
        counter = 0