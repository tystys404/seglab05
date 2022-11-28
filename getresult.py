import os
import subprocess


# cmd = "./randominput.out " + "input/4A/stdin_format.txt" + " >randomin.txt"
# print(subprocess.getoutput(cmd))

# for pos in ["input/4A/stdin_format.txt", "input/50A/stdin_format.txt"]:
#     inputcmd = "./randominput.out " + pos + " >randomin.txt"


def getresult(path1, path2):
    if "4A" in path1 and "4A" in path2:
        print(1)
        cmd = "./randominput.out " + "input/4A/stdin_format.txt" + " >randomin.txt"
        subprocess.getoutput(cmd)
        cutstring1 = path1[0:-4] + ".out"
        cutstring2 = path2[0:-4] + ".out"
        cmmd1 = "./" + cutstring1 + " <randomin.txt"
        print(cmmd1)
        cmmd2 = "./" + cutstring2 + " <randomin.txt"
        print(cmmd2)
        for i in range(0, 51, 1):
            out0 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            oout0 = str(out0.communicate())
            out1 = subprocess.Popen(cmmd1, shell=True, stdout = subprocess.PIPE)
            # oout1 = str(out0.communicate())
            out2 = subprocess.Popen(cmmd2, shell=True, stdout = subprocess.PIPE)
            # oout2 = str(out0.communicate())
            if out1 == out2:
                print("yes")
            else:
                print("no")


getresult("input/4A/48762087.cpp", "input/4A/84822639.cpp")
