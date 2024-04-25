def sub(n):
    print(f'sub({n})')
    if n<=1 : return n
    return sub(n-1) + sub(n-2)
sub(3)
#반복구조 팩토리얼 알고리즘
def factorial(n):
    num = 1
    for i in range(n,0,-1):
        num = num*i
    return num
snum = int(input('숫자를 입력하세요 '))

print(factorial(snum))

#하노이탑
def hanoi(n,aa,bb,cc):#aa 첫번째 bb 두번째 cc 세번째
    if(n==1):
        print('원판 1: %s-->%s'% (aa,cc))
    else :
        hanoi(n-1,aa,cc,bb)
        print('원판 %d : %s --> %s'% (n,bb,cc))
        hanoi(n-1,cc,aa,bb)

hanoi(4,'A','B','C')