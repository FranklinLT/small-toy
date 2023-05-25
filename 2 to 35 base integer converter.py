# Only used for integer conversion from base 2 to 35
a = str(input('Please enter the number you need to convert: '))
n = int(input('Please enter the original base: '))
m = int(input('Please enter the base you need to convert: '))
p = 0
x = 1
y = ''
for i in a:
    if ord(i) >= 65:
        p = p + (ord(i) - 55)*n**(len(a) - x)
        x = x + 1
    else:
        p = p + int(i)*n**(len(a) - x)
        x = x + 1
print('The decimal representation of this number is: ',p)
while p > 0:
    z = p % m
    p = p // m
    if z > 9:
        z = chr(z + 55)
    y = str(z) + y
print('Your',m,'base expression number is: ',y)