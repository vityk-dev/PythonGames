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
             
x = input("What coffee whould you like:")
coffee = CoffeMachine(1,2,3,4)
result = coffee.dictHelp()
print("Price is:" + str(result))

#git init
#git add .
#git commit - m "123"
#git push


class BestCoffee:
  def __init__(self):
      self.ingridients = [10000, 1000, 500] # milk_ml, coffee_gr, sugar_gr

      self.coffee_recipes = {
                    "capucino": [100, 40],
                     "latte": [230, 40],
                     "americano": [0, 18],
                     "espresso": [0, 40]
      }
      self.quantity = []


  def coffeeCount(self, coffeetype):


    if coffeetype not in self.coffee_recipes:
      return f"We don't have that, we only have {self.coffee_recipes.keys()}"

    recipe = self.coffee_recipes[coffeetype]


    if recipe[0] == 0:
      quant = self.ingridients[1] / recipe[1]

    else:
      x= self.ingridients[0] / recipe[0]
      y = self.ingridients[1] / recipe[1]
      quant = min(x,y)

    return int(quant)

z = input("What coffee are you interested in:")

coffee = CoffeMachine()
best = BestCoffee()
price = coffee.dictHelp()
best.coffeeCount(z)
cups = best.coffeeCount(z)
t_price = cups * price
print(cups)
print(price)
print(t_price)