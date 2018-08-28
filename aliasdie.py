import sys
import random

n = input("How many Sides? ")
print("Probabilities of Sides:")
probs = []
for i in range(0,n):
    prob = input(str(i) + ": ")
    probs.append(prob)
greater = []
lesser = []
sum = 0
for i in range(0,n):
    sum += probs[i]
if sum !=1:
    print(probs)
    raise Exception("Probabilities don't sum to 1")
for i in range(0,n):
    probs[i] = probs[i] * n
    if probs[i] > 1:
        greater.append(i)
    if probs[i] < 1:
        lesser.append(i)
alias = []
for i in range(0,n):
    alias.append(-1)
print(alias)
while lesser and greater:
    i = lesser.pop()
    diff = 1 - probs[i]
    j = greater.pop()
    alias[i] = j
    probs[j] = probs[j] - diff
    if round(probs[j],10) < 1:
        lesser.append(j)
    elif probs[j] > 1:
        greater.append(j)
if lesser or greater:
    print("probs: " + str(probs))
    print("alias: " + str(alias))
    print("lesser: " + str(lesser))
    print("greater: " + str(greater))
    raise Exception("Initialization failed")
while True:
    inp = input("1 for roll 0 for exit")
    if inp == 0:
        break
    else:
        for i in range(0,20):
            i = random.randint(0,n-1)
            cointoss = random.random()
            if cointoss <= probs[i]:
                print(i)
            else:
                print(alias[i])