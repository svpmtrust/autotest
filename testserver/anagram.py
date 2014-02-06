

fi = open("input.txt",'r')
out = fi.readlines()
x = []



for line in out:
    x.extend(line.split(' '))
    
    
for i in range(len(x)):
    for j in range(len(x)):
        if i != j:
            if (x[i] != x[j]) and (''.join(sorted(x[i])) == ''.join(sorted(x[j]))):
                print x[i]


