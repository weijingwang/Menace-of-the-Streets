from re import X


class dog():
    def __init__(self,x):
        self.x=x
    def poo(self):
        self.x-=0.1
    def increase(self):
        self.x+=1
        return(self.x)

hana = dog(0)
while True:
    hana.poo()
    count = hana.increase()
    print(count)

