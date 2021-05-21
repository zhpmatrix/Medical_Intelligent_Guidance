"""
	https://github.com/facebookresearch/fastText
"""
import fasttext
from sklearn.metrics import classification_report

def train():
	model = fasttext.train_supervised("Intelligent_Guidance/train.txt", lr=0.1, dim=200,
			                 epoch=300, word_ngrams=2, loss='softmax')
	model.save_model("Intelligent_Guidance/model.bin")


def test():
	classifier = fasttext.load_model("Intelligent_Guidance/model.bin")
	#批量测试
	#result = classifier.test("Intelligent_Guidance/dev.txt")
	#单个测试
	real_labels = []
	pred_labels = []
	with open("../crawler/dev.txt", "r") as reader:
		for line in reader:
			#import pdb;pdb.set_trace()
			real_labels.append(line.split()[0])
			pred_labels.append(classifier.predict([line.strip()])[0][0][0])
	report = classification_report(real_labels, pred_labels)
	print(report)

if __name__ == "__main__":
	#train()
	test()
