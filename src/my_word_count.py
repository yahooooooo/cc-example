import os, fileinput, sys
import concurrent.futures
import functools

def GetWordCountsForFile(filepath):
	word_counts = {}
	for line in fileinput.input(filepath):
		line = ''.join(ch for ch in line if ch.isalnum() or ch == ' ')
		for word in line.strip().lower().split(' '):
			if word == '':
				continue
			try:
				word_counts[word] += 1
			except KeyError as e:
				word_counts[word] = 1
	return word_counts

def ReduceDictionaries(x, y):
	result = x
	for key in y.keys():
		try:
			result[key] += 1
		except KeyError as e:
			result[key] = 1
	return result

def main():
	input_dir = sys.argv[1]
	output_file = sys.argv[2]
	
	filepaths = [os.path.join(input_dir,filename) for filename in os.listdir(input_dir)]
	output = open(output_file, 'w+')

	with concurrent.futures.ProcessPoolExecutor(max_workers=25) as executor:
		word_counts = executor.map(GetWordCountsForFile, filepaths)
		result = functools.reduce(ReduceDictionaries, word_counts)
	
	for key in sorted(list(result.keys())):
		output.write(key + '\t' + str(result[key]) + '\n')

	output.close()

if __name__ == '__main__':
	main()