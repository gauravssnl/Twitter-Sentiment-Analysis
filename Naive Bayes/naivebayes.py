from textblob.classifiers import NaiveBayesClassifier
import csv

def generate_training_csv():
	with open('train.csv', encoding='iso-8859-1') as f:
		csv_reader = csv.reader(f)
		column_header = next(csv_reader)
		with open('train_textblob.csv', 'w', encoding="iso-8859-1") as wf:
			data = ""
			count = 0
			for row in csv_reader:
				if count <= 10:
					data += row[2] + ","  
					if row[1] == 1:
						data += "pos\n"
					else:
						data += "neg\n"
					count += 1
					wf.write(data)
			print('Training Data write complete')


if __name__ == '__main__':
	#generate_training_csv()
	with open('train_textblob.csv', encoding='iso-8859-1') as fp:
		#print(fp.readlines())
		csv_reader = csv.reader(fp)
		print(next(csv_reader))
		cl = NaiveBayesClassifier(fp, format='csv')
		print('NaiveBayesClassifier Training completed')
		print(dir(cl))
		print(cl.prob_classify('I am bad'))
