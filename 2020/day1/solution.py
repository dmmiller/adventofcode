file = open('input.txt')
numbers = map(int, file.readlines())
number_map = dict(map(lambda x : (x, 1), numbers))
for num in number_map:
    if 2020 - num in number_map:
        print("Found the number pair ", num, 2020 - num, " with product : ", num * (2020 - num))
        break

for num in number_map:
    for num2 in number_map:
        if num != num2:
            if 2020 - (num + num2) in number_map:
                print("Found the triple ", num, num2, 2020 - (num + num2), "with product : ", num * num2 * (2020 - (num + num2)))
                break
    else:
        continue
    break

