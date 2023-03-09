import os
import pathlib

entries = os.listdir('C:\\Andre\\MasterCim\\Fontes\\V21.04.01')
for entry in entries:
    tipo = pathlib.Path(entry).suffix
    if  not (tipo == '.pas' or tipo=='.dcu' or tipo=='.dfm' or tipo=='.dpr' or tipo=='.res' or tipo=='.PAS' or tipo=='.dof' or tipo=='.drc' or tipo=='.ddp' or tipo=='.~dfm' or tipo=='.~pas' or tipo=='.DFM' or tipo=='.map'):
        print(entry)