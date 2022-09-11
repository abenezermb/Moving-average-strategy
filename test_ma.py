import sys
from sma import SMA



help = """
Command syntax:
python3 test_ma.py sma/wma/ewma
"""
if len(sys.argv)!= 2:
    print(help)
else:
    if sys.argv[1] == 'sma':
        sma = SMA()
        sma.start()
    elif sys.argv[1] == 'wma':
        pass
    elif sys.argv[1] == 'ewma':
        pass
    else:
        print(help)