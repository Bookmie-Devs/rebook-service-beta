

names = ['enoch','steven','mike','mike','havy','enoch','brown','kofi']

# print(list(set(names)))

new_list = []
for name in names:
    if name not in new_list:
        new_list.append(name)

print(new_list)

