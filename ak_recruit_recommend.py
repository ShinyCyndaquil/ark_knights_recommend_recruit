import pandas as pd
from itertools import combinations

r_db = pd.read_csv('operator_recruit_list.csv', sep=';')
print(r_db.shape)
r_db = r_db[r_db['available'] == 'O']
r_db = r_db.sort_values(by=['star'], ascending=False)

print('5개 태그 입력하세요..')
input_tags = []
for i in range(5):
    input_tags.append(input('{}번째 태그 : '.format(i + 1)))

print('입력한 태그:', input_tags)

tag_combinations = []

for i in range(1, 6):
    tag_combinations = tag_combinations + [list(c) for c in list(combinations(input_tags, i))]

#print(tag_combinations)

output_text = ''

min_star = 7
certainties = []
guarantees = []  # 4 or more stars confirmed

for tag_comb in tag_combinations:
    min_star = 7
    available_chars = []
    trig = 0
    for index, row in r_db.iterrows():
        op_tags = row.iloc[2:8].values.tolist()
        if all(elem in op_tags for elem in tag_comb):
            if trig == 0:
                for tag_elem in tag_comb:
                    output_text = output_text + tag_elem + ', '
                trig = 1
                output_text = output_text[:-2] + ': '
            op_name = row['name']
            available_chars.append(op_name)
            op_star = row['star']
            if min_star > op_star:
                min_star = op_star
            output_text = output_text + op_name + ', '
    if len(available_chars) == 1:
        certainties.append([available_chars[0], tag_comb])
    if 3 < min_star <= 6:
        guarantees.append([min_star, available_chars, tag_comb])
    if trig == 1:
        output_text = output_text[:-2] + '\n'

output_text = output_text + '\n확정 태그들:\n'
if not certainties:
    output_text = output_text + '없음\n'
else:
    for ct in certainties:
        for tag in ct[1]:
            output_text = output_text + tag + ', '
        output_text = output_text[:-2] + ': ' + ct[0] + '\n'

output_text = output_text + '\n4성 이상 태그들:\n'
if not guarantees:
    output_text = output_text + '없음\n'
else:
    guarantees = sorted(guarantees, key=lambda x: x[0], reverse=True)
    for gt in guarantees:
        output_text = output_text + '최소 ' + str(gt[0]) + '성, '
        for tag in gt[2]:
            output_text = output_text + tag + ', '

        output_text = output_text[:-2] + ' : '
        for op in gt[1]:
            output_text = output_text + op + ', '
        output_text = output_text[:-2] + '\n'

print(output_text)

with open('ak_recruit_output.txt', 'w') as f:
    f.write(output_text)
