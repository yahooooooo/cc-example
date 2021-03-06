import os, fileinput, sys
import concurrent.futures	

class CountDict:
	"""CountDict maintains the histogram of word counts.
	Since there are few distinct word counts by line in a large corpus
	and most of these are concentrated at lower values,
	maintaining the number of times a word count has appeared
	is far more scalable for storage and computing median."""

	count_dict = {}
	total_count = 0
	median = -1

	def InsertElement(self, x):
		"""Insert a count into count_dict and recalculate the median."""
		self.total_count += 1
		try:
			self.count_dict[x] += 1
		except KeyError as e:
			self.count_dict[x] = 1
		self.RecalculateMedian()

	def RecalculateMedian(self):
		"""Recalculate the median using the histogram of word counts."""
		self.median = -1		
		unique_counts = sorted(list(self.count_dict.keys()))

		cum_sum = [0.0]
		for key in unique_counts:
			cum_sum.append(self.count_dict[key] + cum_sum[len(cum_sum)-1])
		cum_sum = cum_sum[1:]

		for i in range(len(cum_sum)):
			if cum_sum[i] == self.total_count/2.0:
				self.median = (unique_counts[i] + unique_counts[i+1])/2.0
				break
			if cum_sum[i] > self.total_count/2.0:
				self.median = 1.0*unique_counts[i]
				break

	def GetMedian(self):
		"""Return current median."""
		return self.median

def GetWordCountsByLine(filepath):
	"""Create a list of word counts for a document."""
	word_counts = []
	for line in fileinput.input(filepath):
		if line.strip() == '':
			word_count = 0
		else:
			word_count = line.strip().count(' ') + 1
		word_counts.append(word_count)
	return word_counts

def main():
	input_dir = sys.argv[1]
	output_file = sys.argv[2]
	
	countDict = CountDict()
	filepaths = [os.path.join(input_dir,filename) for filename in os.listdir(input_dir)]
	output = open(output_file, 'w+')

	with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
		print('Reading files from {i}'.format(i=input_dir))
		# read files in parallel using concurrent.futures API
		for input_file, word_counts in zip(filepaths, executor.map(GetWordCountsByLine, filepaths)):
			print('Calculating and writing running median for {i}...'.format(i=input_file))
			# calculate and write running median
			for word_count in word_counts:
				countDict.InsertElement(word_count)
				output.write(str(countDict.GetMedian()) + '\n')
		print('Done calculating and writing running median to {o}...'.format(o=output_file))

	output.close()

if __name__ == '__main__':
	main()
