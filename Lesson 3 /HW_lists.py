
# Списки

# Створіть масив colors з елементами "Жовтий", "Синій"
colors = ["Жовтий", "Синій"]
print(colors)


# В кінець масиву додати "Червоний"
colors.append("Червоний")
print('В кінець масиву додати "Червоний": ', colors)


# Замініть передостаннє значення з кінця масиву на "Чорний". 
# При цьому вважайте, що довжина масиву невідома
colors[-2] = "Чорний"
print('Замініть передостаннє значення з кінця масиву на "Чорний": ', colors)


# Видаліть перше значення і виведіть масив на екран
del(colors[0])
print('Видаліть перше значення і виведіть масив на екран:', colors)


# Додайте в початок значення "Зелений" і "Помаранчевий"
colors=["Зелений", "Помаранчевий"]+colors
print('Додайте в початок значення "Зелений" і "Помаранчевий":', colors)





