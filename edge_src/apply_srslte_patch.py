import os
dir_path = os.path.dirname(os.path.realpath(__file__))
# srslte_path = os.path.join(dir_path, "srsLTE")
for path, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith(".patch"):
            p = os.path.join(path, f)
            print(p)
            cmd = "patch -p0 --directory=" + dir_path + " < "+p
            print(cmd)
            os.system(cmd)
        else:
            continue
