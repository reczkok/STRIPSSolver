f = open("solution.txt", "r")
input = f.read()

# Parse the input
input = input.split("\n")
output = []
for line in input:
    line = line.split("-->")
    output.append(line[0])

for i in output:
    print(i)

