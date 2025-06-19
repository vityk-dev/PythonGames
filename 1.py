class CoffeMachine:
    def __init__(self,milk,coffee,water,sugar):
        self.milk = milk
        self.coffee = coffee 
        self.water = water
        self.sugar = sugar
        self.price = {"capucino": 3.5, "late": 3, "americano": 4, "espresso": 4.4}

    def dictHelp(self):
        if x in self.price.keys():
            return self.price[x]
        else:
            return "Don't have that"
        
print("What coffee whould you like:")        
x = input()
coffee = CoffeMachine(1,2,3,4)
result = coffee.dictHelp()
print("Price is:" + str(result))
