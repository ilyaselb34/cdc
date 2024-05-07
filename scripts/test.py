from datetime import datetime, timedelta
a=datetime(2023,1,1)
b=a
a+=timedelta(days=1)
print(a)
print(b)