file = open('input.txt')
numbers = set(map(int, file.readlines()))
for num in numbers:
    if 2020 - num in numbers and num != 2020 - num:
        print("Found the number pair ", num, 2020 - num, " with product : ", num * (2020 - num))
        break

for num in numbers:
    for num2 in numbers:
        if num != num2:
            if 2020 - (num + num2) in numbers:
                print("Found the triple ", num, num2, 2020 - (num + num2), "with product : ", num * num2 * (2020 - (num + num2)))
                break
    else:
        continue
    break

