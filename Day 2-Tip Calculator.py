print("Welcome to the Tip Calculator!")
bill = float(input("What was your bill?: $"))
tip_percent = int(input("How many percent do you want to tip? 10, 12 or 15?: "))
people = int(input("How many people are splitting the bill?: "))

tip = (tip_percent/100) * bill
total = bill + tip
final = round(total/people, 2)

print(f"Each person should pay ${final}.")