import math

# variables
# tableau
# boucles
# tests conditionnels
# fonction

a = [1, 2, 3]
b = True

f = open("fake.txt", "w")
f.write('Hello world')

#for toto in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
#    print(toto)


# ----------------------------------------------------------------------------------------


def printSomething(a, b):
    print(a,b)

printSomething(1, 2) # 1 2
printSomething(a=1, b=2)  # 1 2
printSomething(b=1, a=2)  # 2 1

def empty():
    return math.pi

print( empty() )

# ----------------------------------------------------------------------------------------


a = [1, 2, 3, 4]
print(a)
print(a[0])
print(a[3])

b = ['coucou', 'hello', 'world']
print(b) # coucou hello world

b.reverse()
print(b) # world hello coucou

b.insert(0, b[2])
b.pop()
print(b)

c = [2, 3, 2, 7, 9]
print(c.count(7))

# --------------------------------------------------------------------------

a = 10

if a == 3:
    print('a vaut 3')
elif a == 2:
    print('a vaut 2')
else:
    print('a ne vaut ni 2 ni 3')


if a >= 1 and a <= 6:
    print('a est entre 1 et 6')
else:
    print("a n'est pas entre 1 et 6")

print("Mon nom est \"toto\"")
print('Mon nom est "toto"')

print(f"la variable a vaut {a} et c'est tout")
print("la variable a vaut " + str(a) + " et c'est tout")


s = 'coucou'
print(s.capitalize())

