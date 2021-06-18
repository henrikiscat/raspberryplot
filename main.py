import matplotlib.pyplot as plt
import ast
import pandas as pd
from matplotlib.widgets import CheckButtons
import matplotlib.colors as clrs


def my_plotter(ax, data, param_dict):
    return ax.plot(data, **param_dict)


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
    for var in messages[0:7]:
        columns_ += list(var.keys())
    df = pd.DataFrame(index=total_time, columns=columns_)
    df_pec = pd.read_csv('Test15448_head_removed.csv', index_col=11)
    for j in range(len(messages)):
        for key in messages[j]:
            df.at[total_time[j], str(key)] = messages[j][key]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 8))
    ax1.set_title('Raspberry log, TestID: 15488')
    ax2.set_title('PEC log, TestID: 15488')
    ax2.set_xlabel('Total time [s]')
    ax1.set_ylabel('mV')
    ax2.set_ylabel('mV')

    plt.subplots_adjust(left=0.26)
    df_pec = df_pec.iloc[:, 24:(24 + 30)]
    df = df[df.index > 105]
    #print(({x:x.split()[0] for x in df_pec.columns}))
    df_pec.rename(columns = {x:x.split()[0] for x in df_pec.columns},inplace=True)
    print(df_pec.columns)
    lines = [ax1.plot(df[x].index, df[x].values, label=x, marker='.', markersize=5) for x in df.columns]
    lines_pec = [ax2.plot(df_pec[x].index, df_pec[x].values, label=x, marker='.', markersize=5) for x in df_pec.columns]
    colors = [clrs.to_rgba(x.get_color()) for x in ax1.get_lines()]
    box = plt.Rectangle(width=0.1, height=0.1, xy=(0, 1))
    rax = plt.axes([0.02, 0.1, 0.19, 0.7])
    labels = df.columns.values.tolist()
    labels_pec = df_pec.columns.values.tolist()
    print("rasp: {}, pec: {}".format(labels, labels_pec))
    visibility = [line[0].get_visible() for line in lines]
    check = CheckButtons(rax, labels, visibility)
    i = 0
    for label in check.labels:
        label.set_color(colors[i])
        i += 1

    def func(label):
        index = labels.index(label)
        index_pec = labels_pec.index(label)
        lines[index][0].set_visible(not lines[index][0].get_visible())
        lines_pec[index_pec][0].set_visible(not lines_pec[index_pec][0].get_visible())
        plt.draw()

    check.on_clicked(func)
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

