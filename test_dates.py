import sys
sys.path.insert(0,'.')
from services.trade_data_service import fetch_real_trade_data

# Test Spain + Dates
r = fetch_real_trade_data("080410", "Spain")
print(r[:1500])
