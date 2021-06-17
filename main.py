import matplotlib.pyplot as plt
import ast
import pandas as pd


with open('logfile9_12_7.log', 'r') as f:
    lines = f.readlines()
    messages = []
    total_time = []
    for line_ in lines[2:]:
        if "Errorframe" not in line_:
            messages.append(ast.literal_eval(str("{" + line_[10:].split('{')[-1])))
            total_time.append(float(line_[10:].split('{')[0].rstrip().rstrip(',')))
    columns_ = []
    dt = 100
    for j in range(len(total_time) - 1):
        dt_new = total_time[j + 1] - total_time[j]
        if dt_new < dt:
            dt = dt_new
            print("Timestamp: {}, deltatime: {}".format(total_time[j], dt))
    for var in messages[0:7]:
        columns_ += list(var.keys())

    df = pd.DataFrame(index=total_time, columns=columns_)
    for j in range(len(messages)):
        for key in messages[j]:
            df.at[total_time[j], str(key)] = messages[j][key]
    plt.plot(df.index, df.values, '-+')
    plt.legend(columns_, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()


def write_csv():
    values_csv = "time,"
    for col in columns_:
        values_csv += (col + ",")
    values_csv.rstrip(',')
    values_csv += "\n"
    j = 0
    k = 0
    with open('raspberry_log.csv', 'w') as csv_f:
        for mess in messages:
            values_csv += "{}".format(total_time[j])
            values_csv += "," * k
            for val in mess.values():
                values_csv += ",{}".format(val)
            values_csv += "," * (18 - (k + len(mess.values())))
            j += 1
            if k > (18 - len(mess)):
                k = 0
            else:
                k = k + len(mess)
            values_csv += "\n"
        csv_f.write(values_csv)


#write_csv()


