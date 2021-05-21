import json
import pandas as pd
import jieba
class DataUtils:
    def get_data(self, data_path):
        data = []
        with open(data_path, "r") as reader:
            for line in reader:
                jsonline = json.loads(line.strip())
                raw_label = jsonline["label"].split("_")
                label = [label for label in raw_label if "科" in label]
                #存在多个命中时，默认第一个
                if len(label) > 0:
                    data.append({"question":jsonline["question"], "label":label[0]})
        return data

if __name__ == "__main__":
    utils = DataUtils()
    data2021 = utils.get_data("2021_haodaifu_data.csv")
    data2020 = utils.get_data("2020_haodaifu_data.csv")
    raw_data = pd.DataFrame(data2021 + data2020)
    
    data = []
    class_thresh = 500
    class_num = raw_data["label"].value_counts().to_dict()
    for key, value in class_num.items():
        if value > class_thresh:
            data.extend(raw_data[raw_data["label"] == key].values.tolist())
    data = pd.DataFrame(data, columns = ["question", "label"])
    data = data.sample(frac=1)
    
    split_ratio = 0.8
    train_end_index = int(data.shape[0] * split_ratio)

    train = []
    dev = []
    for i in range(0, train_end_index):
        train.append(data.iloc[i])
    for i in range(train_end_index, data.shape[0]):
        dev.append(data.iloc[i])
    print(pd.DataFrame(train)["label"].value_counts())
    print(pd.DataFrame(dev)["label"].value_counts())    
    print(data.shape)
    def save_data(data, save_path):
        with open(save_path, "w") as writer:
            for line in data:
                question = " ".join(list(jieba.cut(line["question"])))
                writer.write("__label__"+line["label"]+" "+question+"\n")
    save_data(train, "train.txt")
    save_data(dev, "dev.txt")
