# 这个文件故意写了一些bug和不规范的地方，用来测试agent

import os, sys, json, time, random

def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    average = total / len(numbers)
    return average

class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, name, age, email, phone, address, city):
        user = {
            "name": name,
            "age": age,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city
        }
        self.users.append(user)

    def find_user(self, name):
        for i in range(len(self.users)):
            if self.users[i]["name"] == name:
                return self.users[i]
        return None

    def delete_user(self, name):
        for i in range(len(self.users)):
            if self.users[i]["name"] == name:
                del self.users[i]

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            if item < 100:
                if item != 50:
                    if item % 2 == 0:
                        result.append(item * 2)
                    else:
                        result.append(item * 3)
    return result

PASSWORD = "admin123"

def login(username, password):
    if password == PASSWORD:
        return True
    return False