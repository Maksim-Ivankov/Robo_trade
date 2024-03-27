# with open("strat_1_set.txt",encoding='utf-8') as file:
#     for item in file:
#         print(item)

set_settings_strat_1 = []
        
with open("strat_1_set.txt",encoding='utf-8') as file:
    for line in file:
        if len(line.rstrip().split(',')) != 7: print(f'ОШИБКА! Неправильное кол-во настроек в строке {line.rstrip()}')
        set_settings_strat_1.append(line.rstrip().split(','))
        
print(len(set_settings_strat_1))
print(set_settings_strat_1)