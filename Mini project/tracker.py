# Name: Kananreet Kaur
# Roll No.2501730375
# Date: 2 November 2025
# Course title: Daily Calorie Tracker
print("Welcome to the Daily Calorie Tracker!")
print("This Daily calorie Tracker will help you keep an account of your calories intake and help you stay fit and healthy!. ")
print("Let's get started!")
meals = []
calories = []
n = int(input("How many meals do you want to log today? "))

for i in range(n):
    mealname = input(f"\nEnter the name of meal #{i+1}: ")
    mealcal = float(input(f"Enter calories for {mealname}: "))
    meals.append(mealname)
    calories.append(mealcal)
totalcalories = sum(calories)
averagecalories = totalcalories / len(calories)

dailylimit = float(input("\nEnter your daily calorie limit: "))
if totalcalories > dailylimit:
    print("Looks like it was a cheat day today?")
else:
    print("Yay! You are on healthy track!")
print("YOUR DAILY CALORIE SUMMARY ")
print(f"{'Meal Name':<20}{'Calories':>10}")

for i in range(len(meals)):
    print(f"{meals[i]:<20}{calories[i]:>10.2f}")

print("----------------------------------------------")
print(f"{'Total:':<20}{totalcalories:>10.2f}")
print(f"{'Average:':<20}{averagecalories:>10.2f}")
print("==============================================")
print("==============================================\n")
