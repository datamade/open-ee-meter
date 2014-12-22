import sys
import pandas as pd

csv1 = pd.read_csv( sys.argv[1] )
csv2 = pd.read_csv( sys.argv[2] )

merged = csv1.merge(csv2, on=sys.argv[3])

merged.to_csv("build/merged.csv", index=False)
