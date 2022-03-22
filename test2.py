class cat():
    def __init__(self,x):
        super().__init__()
        self.x=x
    def meow(self):
        return("MEOW!")

class dog():
    def __init__(self,x):
        self.x=x
        self.Momo = cat(self.x)
    def poo(self):
        self.x-=0.1
    def increase(self):
        self.x+=0.2
        return(str(self.x)+self.Momo.meow())


Hana = dog(0)
while True:
    Hana.poo()    
    count = Hana.increase()
    print(count)

