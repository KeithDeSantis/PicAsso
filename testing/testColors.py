# Used to print the dominant colors cause terminal is being stupid
import sys
f = open('./resources/rgb_values.txt', 'r')

colors = f.readlines()

rgbs = [[]]
width = 0

rgb_row = 0
for color in colors:
    if(color == '>\n'):
        width = len(rgbs[0])
        rgb_row += 1
        rgbs.append([])
    else:
        rgbs[rgb_row].append(color.split('\t'))
        for trio in rgbs[rgb_row]:
            for num in trio:
                num.replace('\n', '')

#jankey way to get rid of newline
for row in rgbs:
    for color in row:
        color[2] = color[2][:-2]

string_to_print = ''
counter = 0
for rgb_row in rgbs:
    for rgb in rgb_row:
        if (counter >= width):
            string_to_print = string_to_print + '\n'
            counter = 0
        string_to_print = string_to_print + f"\x1b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m*\x1b[0m\t"
        counter += 1
print(string_to_print)