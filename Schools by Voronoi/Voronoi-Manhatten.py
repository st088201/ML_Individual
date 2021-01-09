import matplotlib.pyplot as plt
from random import random
"""STEP 1 - function defining"""


def decode(string):
    string = string[1:len(string) - 1]
    lst = (string[:string.find(',')] + ' ' + string[string.find(',') + 1:]).split()
    for i in range(len(lst)):
        lst[i] = float(lst[i])
    return lst
# turns string (a, b) into list[a, b]


def get_entrance(point, num, streets):
    spec_streets = []
    spec_streets[:] = streets
    spec_streets.append(point[num])
    spec_streets.sort(key=float)
    pos = spec_streets.index(point[num])

    if spec_streets[pos+1] == point[num]:
        # if house is straight on the street
        return pos
    elif pos == len(spec_streets) - 1:
        return pos - 1
    elif pos == 0:
        return 0
    elif min(abs(float(spec_streets[pos])-float(spec_streets[pos+1])),
            abs(float(spec_streets[pos])-float(spec_streets[pos-1]))) == abs(float(spec_streets[pos])-float(spec_streets[pos+1])):
        # if closer street is next
        return pos
    else:
        return pos-1


def get_border(school_1, school_2, number_1, number_2, line_array):
    x1, x2 = school_1[0], school_2[0]
    y1, y2 = school_1[1], school_2[1]
    if y1 != y2:
        k = (x2-x1)/(y1-y2)
        b = (y1+y2 - k*(x1+x2))/2
    else:
        k = 'inf'
        b = (x1+x2)/2
    line_array[number_1][number_2][0], line_array[number_1][number_2][1] = k, b
# fills array of ks and bs of borderlines between 1 and 2 areas


def get_furthest(house_coordinates, num1, num2, line_array, school_array):
    k, b = line_array[num1][num2][0], line_array[num1][num2][1]
    school1_x, school1_y = float(school_array[num1][0]), float(school_array[num1][1])
    if k == 'inf':
        if school1_x <= b:
            school_left = num1
            school_right = num2
        else:
            school_left = num2
            school_right = num1

        if house_coordinates[0] <= b:
            return school_right
        else:
            return school_left
    else:
        if school1_y >= k*school1_x+b:
            school_high = num1
            school_low = num2
        else:
            school_high = num2
            school_low = num1
        if float(house_coordinates[1]) >= k*float(house_coordinates[0])+b:
            return school_low
        else:
            return school_high
# returns number of school furthest of two from house 


def visualize(massive_of_points, color, name):
    for point in massive_of_points:
        plt.scatter(point[0], point[1], c=color, label=name)


"""STEP 2 - data input handling"""
streets_vertical_raw = sorted(input().split(), key=float)
streets_vertical = [float(street) for street in streets_vertical_raw]
streets_horizontal_raw = sorted(input().split(), key=float)
streets_horizontal = [float(street) for street in streets_horizontal_raw]
n_schools = 12
n_houses = 5
schools = [[round(4*i*random())/2, round(4*i*random())/2] for i in range(n_schools)]
houses = [[round(4*i*random())/2, round(4*i*random())/2] for i in range(n_houses)]
print('Schools:', schools)
print('Houses:', houses)
"""
schools_raw = input().split()
schools = []
houses_raw = input().split()
houses = []
n_schools = len(schools_raw)
"""

# array to store k and b of regions' borders
lines = [[[i, i] for i in range(n_schools)] for j in range(n_schools)]
"""
for school in schools_raw:
    schools.append(decode(school))
for house in houses_raw:
    houses.append(decode(house))
    """
for i in range(n_schools):
    for j in range(n_schools):
        if i != j:
            get_border(schools[i], schools[j], i, j, lines)
# del streets_horizontal_raw, streets_vertical_raw, houses_raw, schools_raw
# filled array of borders
coffee_shops = []

"""STEP 3 - Search for nearest school for every house"""
y_min = min(streets_horizontal)
y_max = max(streets_horizontal)
x_min = min(streets_vertical)
x_max = max(streets_vertical)
for building in houses:
    coffee_shop = [streets_vertical[get_entrance(building, 0, streets_vertical)], streets_horizontal[get_entrance(building, 1, streets_horizontal)]]
    print('Coffee for', building, 'at', coffee_shop)
    coffee_shops.append(coffee_shop)
    possible_schools = [i for i in range(n_schools)]
    for i in range(n_schools-1):
        if possible_schools[0] == get_furthest(coffee_shop, possible_schools[0], possible_schools[1], lines, schools):
            possible_schools.pop(0)
        else:
            possible_schools.pop(1)
    for school_num in possible_schools:
        print('Best school for', building, 'is', schools[school_num])
    x_min = min(x_min, building[0])
    x_max = max(x_max, building[0])
    y_min = min(y_min, building[1])
    y_max = max(y_max, building[1])
for building in schools:
    x_min = min(x_min, building[0])
    x_max = max(x_max, building[0])
    y_min = min(y_min, building[1])
    y_max = max(y_max, building[1])

# for every house find nearest schools by elimination method

"""STEP 4 - Data output"""
for street in streets_horizontal:
    plt.hlines(float(street), x_min, x_max, colors='black')

for street in streets_vertical:
    plt.vlines(float(street), y_min, y_max, colors='black')

visualize(schools, 'red', 'Schools')
visualize(coffee_shops, 'brown', 'Coffee Shops')
visualize(houses, 'blue', 'Houses')
plt.title('City map')
plt.show()


