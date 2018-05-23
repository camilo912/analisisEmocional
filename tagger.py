import pandas as pd
import numpy as np

if __name__ == "__main__":
    data_frame = pd.read_csv("airlines.csv", encoding="iso8859_16")
    data_frame["feeling"] = np.random.rand(data_frame.shape[0])
    for i in range(data_frame.shape[0]):
        if(data_frame["rating"][i] < 4):
            data_frame['feeling'][i] = "sad"
        elif(data_frame["rating"][i] < 8):
            data_frame['feeling'][i] = "normal"
        else:
            data_frame['feeling'][i] = "happy"

    data_frame.to_csv("saved.csv")
