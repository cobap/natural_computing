import sys, os

arquivo = None
for line in sys.stdin:
	arquivo = line
arquivo = arquivo.replace('\n', '')
with open("./results/" + arquivo + ".csv", "r") as fin:
    with open("./results/" + arquivo + "_limpo.csv", "w") as fout:
        for line in fin:
        	fout.write(line.replace('(', '').replace(")", "").replace("\'", "\""))
os.remove("./results/" + arquivo + ".csv")
