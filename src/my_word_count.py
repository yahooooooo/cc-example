import os, fileinput, sys
import concurrent.futures
import functools

def GetWordCountsForFile(filepath):
	"""Create a <word,count> mapping for each document."""
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
	"""Reduce dictionaries x and y by adding counts for each word."""
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

	with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
		print('Reading files from {i}'.format(i=input_dir))
		# read files and convert to word count dictionaries in parallel using concurrent.futures API
		word_counts = executor.map(GetWordCountsForFile, filepaths)
		print('Calculating final word counts...')
		# reduce word count dictionaries obtained from various documents by key
		result = functools.reduce(ReduceDictionaries, word_counts)
		print('Writing word counts to {o} in alphabetical order...'.format(o=output_file))
		# write the resultant word counts alphabetically to output file 
		for key in sorted(list(result.keys())):
			output.write(key + '\t' + str(result[key]) + '\n')
		print('Done writing word counts to {o} in alphabetical order...'.format(o=output_file))

	output.close()

if __name__ == '__main__':
	main()