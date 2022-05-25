import sys
import matplotlib.pyplot as plt
from helper.msexcel import MsExcelLoaderForDA

def Main():
    args = sys.argv
    
    db = MsExcelLoaderForDA()
    r = db.LoadFile(args[1], args[2], True)
    
    sizes = db.ToFloatArrayVN(r['people'])
    y1 = db.ToFloatArrayVN(r['income'])
    y2 = db.ToFloatArrayVN(r['outcome'])
    x = db.ToFloatArrayVN(r['food_expenditure'])
    
    plt.scatter(x, y1, s = sizes, color = 'green')
    plt.scatter(x, y2, s = sizes, color = 'red', alpha = 0.5)
    
    plt.show()

Main()
