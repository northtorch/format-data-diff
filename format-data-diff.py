import sys
import json

if len(sys.argv) < 3:
    print("Usage: python format-data-diff.py <input_file> <output_file>")
    sys.exit(1)

DEFAULT_VALUE = -1

ret = {}

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, mode='r', encoding='utf-8', newline='\n') as f:
    column_count = 0
    while True:
        line = f.readline().strip()
        if not line:
            break
        # データ読み込み
        pos, dat = json.loads(line)
        key = dat[0]
        data = dat[1:]
        if column_count < 1:
            # 最初の行でカラム数を取得
            column_count = len(data)
        if key not in ret:
            # 初見のプライマリキーなら、器を作成する
            ret[key] = []
            for i in range(column_count):
                ret[key].append(
                    {
                        "before": DEFAULT_VALUE,
                        "after": DEFAULT_VALUE
                    })
        # データを格納
        d = ret[key]
        for idx, dat in enumerate(data):
            if pos == "-":
                d[idx]["before"] = dat
            else:
                d[idx]["after"] = dat

with open(output_file, mode='w', encoding='shift_jis') as f:
    header = "key"
    for i in range(column_count):
        header += f",before_{i},after_{i}"
    header += "\r\n"
    f.write(header)
    for key, dat_list in ret.items():
        dat_str = key
        for d in dat_list:
            dat_str += f",{d['before']},{d['after']}"
        dat_str += "\r\n"
        f.write(dat_str)
