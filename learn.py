

# fruits = ['apple', 'banana', 'cherry']
# for fruit in fruits:
#   print(fruit);

# num = 9;
# print("Positive" if num > 0 else "Negative");

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# squared_numbers = [number ** 2 for number in numbers]
# print(squared_numbers)

# doubled_numbers = list(map(lambda x: x * 2, numbers))
# print(doubled_numbers)

# even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
# print(even_numbers)

# odd_numbers = list(filter(lambda x: x % 2, numbers))
# print(odd_numbers)

# phone_number = input("Enter your phone number: ")
# result = phone_number.replace("0", "+63", 1)
# print(result)

# Validate user inout exercise
# username = input("Enter your username: ")

# if len(username) > 12:
#   print("Username is no more than 12 characters long")
# elif not username.find(" ") == -1:
#   print("Username must not contain any spaces")
# elif not username.isdigit:
#   print("Username must not contain digits")

# menu = {"egg": 10, "bacon": 20, "sausage": 30, "spam": 40, "ham": 50}
# print(menu["bacon"])

# carts = []
# total = 0

# for key, value in menu.items():
#   print(f"{key}: {value}")

# while True:
#   order = input("Enter your order: ").strip().lower()
#   if order == "quit":
#     break
#   elif order in menu:
#     carts.append(order)
#     print(f"{order.capitalize()} added to cart")
#   else:
#     print("Invalid order")

# # print(f"Your cart: {carts}")

# for cart in carts:
#   print(cart, end=" ")
#   print()
#   total += menu[cart]
# print(f"Your total is: {total}")

# ARGS AND KWARGS ---------------------------------------------------
# *args (tuple) allow to pass multiple non-key arguments
# **kwargs (dictionary) allow to pass multiple keyword arguments

# def sum_numbers(*args):
#   total = 0;
#   for num in args:
#     total += num

#   return total

# print(sum_numbers(5, 5, 5,5))

# def my_company(**kwargs):
#   for key, value in kwargs.items():
#     print(f"{key}: {value}")

# print(my_company(Company="GO-AI", Location="Kwun Tong"))

# list comprehension = [expression for value in iterable if condition]
# multiply_by_two = [x * 2 for x in range(1, 21)]
# print(multiply_by_two)

# numbers = [1, -1, 2, -5, 3, -2, 4, 6, 8, 10]
# # positive_number = [num for num in numbers if num >= 0]
# # print(positive_number)
# even_numbers = [num for num in numbers if num % 2 == 0]
# print(even_numbers)
# odd_numbers = [num for num in numbers if num % 2]
# print(odd_numbers)

# if __name__ == '__main__' (this script cna be imported OR run standalone). Funtions and classes in this module can be reused without the main block of code executing. 
# Example:

# def reusable_func():
#   print("Can accessed this function or class")

# def main():
#   print("This is the main script from learn.py, so it only runs if it runs the current script")


# OBJECTS ---------------------------------------------------
# class Car:
#   num_cars = 0

#   def __init__(self, model, year):
#     self.model = model
#     self.year = year
#     Car.num_cars += 1

#   def my_car(self):
#     print(f"You're driving a {self.model} - {self.year}")

# car1 = Car("GTR", 2005)
# car2 = Car("Nissan", 2002)
# car3 = Car("Carrero", 2010)
# # car1.my_car()
# print(Car.num_cars)

# if __name__ == '__main__':
#   main()

# INHERITANCE ---------------------------------------------------
# class Animal:
#   def __init__(self, name):
#     self.name = name
  
#   def eating(self):
#      print(f"{self.name} is eating")

# class Prey(Animal):
#     def flee(self):
#        print(f"{self.name} is fleeing")

# class Predator(Animal):
#    def hunting(self):
#       print(f"{self.name} is hunting")

# class Mouse(Prey):
#    pass

# class Cat(Predator):
#    pass

# cat = Cat("Tom")
# cat.hunting()
# cat.eating()
# mouse = Mouse("Jerry")
# mouse.flee()
# mouse.eating()

#SUPER ---------------------------------------------------
# class Shape:
#   def __init__(self, color, is_filled):
#     self.color = color
#     self.is_filled = is_filled

#   def describe(self):
#     print(f"It is color {self.color} and it is {'FILLED' if self.is_filled else 'NOT FILLED'}")

# class Circle(Shape):
#   def __init__(self, color, is_filled, radius):
#     super().__init__(color, is_filled)
#     self.radius = radius

# class Square(Shape):
#   def __init__(self, color, is_filled, width):
#     super().__init__(color, is_filled)
#     self.width = width

# circle = Circle(color="red", is_filled=True, radius=5)
# print(circle.color)
# circle.describe()
# square = Square(color="red", is_filled=False, width=30)
# print(square.is_filled)
# square.describe()

# WRITING FILES ----------------------------------------------------
# import os
# import json
# import csv

# user_name = ["John", "Doe", "Jane", "Doe"]
# employees = {
#   "name": "John Doe",
#   "age": 30,
#   "position": "Software Engineer"
# }
# tableData = [
#   ["Name", "Age", "Position"],
#   ["John Doe", 30, "Software Engineer"],
#   ["Jane Doe", 25, "Data Analyst"]
# ]

# file_path = "output.txt"
# file_path2 = "output.json"
# file_path3 = "output.csv"

# try:
#   with open(file_path, "w") as file:
#     for user in user_name:
#       file.write(user + "\n")
#     print("File created")
# except FileExistsError:
#   print("File already exists")

# # try:
# #   with open(file_path, "x") as file:
# #     file.write("\n" + text)
# #     print("File created")
# # except FileExistsError:
# #   print("File already exists")

# # JSON FILE WRITE ---------------------------------------------------
# try:
#   with open(file_path2, "w") as file:
#     json.dump(employees, file, indent=4)
#     print("File created")
# except FileExistsError:
#   print("File already exists")

# # CSV WRITE
# try:
#   with open(file_path3, "x", newline="") as file:
#     writer = csv.writer(file)
#     # for row in tableData:
#     #   writer.writerow(row)
#     writer.writerows(tableData)
#     print("File created")
# except FileExistsError:
#   print("File already exists")


# READ FILES ---------------------------------------------------

# READ TXT FILE
# try:
#   with open(file_path, "r") as file:
#     content = file.read()
#     print(content)
# except FileNotFoundError:
#   print("File not found")
# except PermissionError:
#   print("You don't have permission to read this file")

# READ JSON FILE
# try:
#   with open(file_path2, "r") as file:
#     content = json.load(file)
#     print(content)
# except FileNotFoundError:
#   print("File not found")
# except PermissionError:
#   print("You don't have permission to read this file")
# except Exception:
#   print("Invalid JSON format")

# READ CSV FILE
# try:
#   with open(file_path3, "r") as file:
#     content = csv.reader(file)
#     for line in content:
#       print(line)

# except FileNotFoundError:
#   print("File not found")
# except PermissionError:
#   print("You don't have permission to read this file")
# except Exception:
#   print("Invalid CSV format")

# DATE AND TIME -----------------------------
# import datetime
# data_and_time = datetime.datetime.now()
# formatted_date = data_and_time.strftime("%d %m, %Y, %H:%M:%S")
# print(formatted_date)

# MULTITHREADING -----------------------------------------------
# import threading
# import time

# def process_one(file_name, extension):
#   time.sleep(2)
#   print(f"Finish processing {file_name}.{extension}")

# def process_two():
#   time.sleep(4)
#   print("Finish processing file 2")

# def process_three():
#   time.sleep(6)
#   print("Finish processing file 3")

# file1 = threading.Thread(target=process_one, args=("file1", "pdf"))
# file1.start()
# file2 = threading.Thread(target=process_two)
# file2.start()
# file3 = threading.Thread(target=process_three)
# file3.start()

# Wait for the threads to finish to continue the other program
# file1.join()
# file2.join()
# file3.join()
# print("All processed done!")