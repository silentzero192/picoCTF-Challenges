input = 39722847074734820757600524178581224432297292490103995912415595360101562905

blue_excel = 8
red_excel = 40

red_excel_one_rotation = red_excel // blue_excel
blue_excel_total_rotations = input * red_excel_one_rotation

# print(blue_excel_total_rotations)
blue_excel_total_rotations = (
    198614235373674103788002620892906122161486462450519979562077976800507814525
)

flag = hex(blue_excel_total_rotations)
print(bytes.fromhex(flag[2:]).decode())