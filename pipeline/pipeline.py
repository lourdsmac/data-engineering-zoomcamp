import sys
import pandas as pd
# import pandas as pd #libary for data processing and manipulation
# 30.30

print('arguments', sys.argv)
month = int(sys.argv[1])
print(f'hello pipeline, month= {month}')

df = pd.DataFrame({"Day": [1, 2, 3], "Num_Passengers": [4, 5, 6]})
df['Month'] = month # Adding a new column 'Month' with the value from command line argument
print(df.head())

df.to_parquet(f'/tmp/pipeline_output_month={month}.parquet', index=False)

