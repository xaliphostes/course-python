def readData(filename):
    f = open(filename, "r")
    for line in f:
        tokens = line.split(' ')  # c'est un tableau de str
        nx = float(tokens[0])
        ny = float(tokens[1])
        print('[',nx,ny,'],')
        
readData('data/matelles-joints.txt')