''' 
 * All rights Reserved, Designed By HIT-Bioinformatics   
 * @Title:  cuteSV_Description.py
 * @Package: NULL
 * @Description: Descriptions of cuteSV parameters.
 * @author: tjiang
 * @date: May 1st 2019
 * @version V1.0.1   
'''
import argparse

VERSION = '1.0.1'

class cuteSVdp(object):
	'''
	Detailed descriptions of cuteSV version and its parameters.

	'''

	USAGE="""\
	Long read based fast and accurate SV detection with cuteSV.
	
	Current version: v%s
	Author: Tao Jiang
	Contact: tjiang@hit.edu.cn
	"""%(VERSION)

	MinSizeDel = 'For current version of cuteSV, it can detect deletions larger than this size.'

def parseArgs(argv):
	parser = argparse.ArgumentParser(prog="cuteSV", description=cuteSVdp.USAGE, 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	# **************Parameters of input******************
	parser.add_argument("input", 
		metavar="[BAM]", 
		type = str, 
		help ="Sorted .bam file form NGMLR or Minimap2.")
	parser.add_argument('output', 
		type = str, 
		help = "the path of [Output]")
	parser.add_argument('temp_dir', 
		type = str, 
		help = "temporary directory to use for distributed jobs")

	# ************** Other Parameters******************
	parser.add_argument('-t', '--threads', 
		help = "Number of threads to use.[%(default)s]", 
		default = 16, 
		type = int)
	parser.add_argument('-b', '--batches', 
		help = "A batches of reads to load.[%(default)s]", 
		default = 10000000, 
		type = int)
	# The description of batches needs to improve.
	parser.add_argument('-S', '--sample',
		help = "Sample name/id",
		default = "NULL",
		type = str)
	parser.add_argument('-g', '--genotype',
		help = "Enable generate genotype (True/False).[%(default)s]",
		default = "False",
		type = str)

	# **************Parameters in signatures collection******************
	GroupSignaturesCollect = parser.add_argument_group('Collection of SV signatures')
	GroupSignaturesCollect.add_argument('-p', '--max_split_parts', 
		help = "Maximum number of split segments a read may be aligned before it is ignored.[%(default)s]", 
		default = 7, 
		type = int)
	GroupSignaturesCollect.add_argument('-q', '--min_mapq', 
		help = "Minimum mapping quality value of alignment to be taken into account.[%(default)s]", 
		default = 20, 
		type = int)
	GroupSignaturesCollect.add_argument('-r', '--min_read_len', 
		help = "Ignores reads that only report alignments with not longer then bp.[%(default)s]", 
		default = 500, 
		type = int)
	# The min_read_len in last version is 2000.
	# signatures with overlap need to be filtered

	# **************Parameters in clustering******************
	GroupSVCluster = parser.add_argument_group('Generation of SV clusters')
	GroupSVCluster.add_argument('-s', '--min_support', 
		help = "Minimum number of reads that support a SV to be reported.[%(default)s]", 
		default = 3, 
		type = int)
	GroupSVCluster.add_argument('-l', '--min_length', 
		help = "Minimum length of SV to be reported.[%(default)s]", 
		default = 30, 
		type = int)

	# Just a parameter for debug.
	# Will be removed in future.
	# GroupSVCluster.add_argument('--preset',
	# 	help = "Parameter presets for different sequencing technologies (pbclr/pbccs/ont).[%(default)s]",
	# 	default = "pbccs",
	# 	type = str)

	# **************Advanced Parameters******************
	GroupAdvanced = parser.add_argument_group('Advanced')

	# ++++++INS++++++
	GroupAdvanced.add_argument('--max_cluster_bias_INS', 
		help = "Maximum distance to cluster read together for insertion.[%(default)s]", 
		default = 200, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_merging_INS', 
		help = "Do not merge breakpoints with basepair identity more than [%(default)s] for insertion.", 
		default = 0.65, 
		type = float)
	GroupAdvanced.add_argument('--diff_ratio_filtering_INS', 
		help = "Filter breakpoints with basepair identity less than [%(default)s] for insertion.", 
		default = 0.65, 
		type = float)

	# ++++++DEL++++++
	GroupAdvanced.add_argument('--max_cluster_bias_DEL', 
		help = "Maximum distance to cluster read together for deletion.[%(default)s]", 
		default = 200, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_merging_DEL', 
		help = "Do not merge breakpoints with basepair identity more than [%(default)s] for deletion.", 
		default = 0.3, 
		type = float)
	GroupAdvanced.add_argument('--diff_ratio_filtering_DEL', 
		help = "Filter breakpoints with basepair identity less than [%(default)s] for deletion.", 
		default = 0.35, 
		type = float)

	# ++++++INV++++++
	GroupAdvanced.add_argument('--max_cluster_bias_INV', 
		help = "Maximum distance to cluster read together for inversion.[%(default)s]", 
		default = 20, 
		type = int)

	# ++++++DUP++++++
	GroupAdvanced.add_argument('--max_cluster_bias_DUP', 
		help = "Maximum distance to cluster read together for duplication.[%(default)s]", 
		default = 500, 
		type = int)

	# ++++++TRA++++++
	GroupAdvanced.add_argument('--max_cluster_bias_TRA', 
		help = "Maximum distance to cluster read together for translocation.[%(default)s]", 
		default = 50, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_filtering_TRA', 
		help = "Filter breakpoints with basepair identity less than [%(default)s] for translocation.", 
		default = 0.6, 
		type = float)

	# parser.add_argument('-d', '--max_distance', 
	# 	help = "Maximum distance to group SV together..[%(default)s]", 
	# 	default = 1000, type = int)



	# These parameters are drawn lessons from pbsv v2.2.0
	# parser.add_argument('--min_del_size', 
	# 	help = "Minimum size of a deletion.[%(default)s]", 
	# 	default = 20, type = int)

	args = parser.parse_args(argv)
	return args

def Generation_VCF_header(file, contiginfo, sample):
	# General header
	file.write("##fileformat=VCFv4.2\n")
	file.write("##source=cuteSV-%s\n"%(VERSION))
	import time
	file.write("##fileDate=%s\n"%(time.strftime('%Y-%m-%d %H:%M:%S %w-%Z',time.localtime())))
	for i in contiginfo:
		file.write("##contig=<ID=%s,length=%d>\n"%(i[0], i[1]))

	# Specific header
	# ALT
	file.write("##ALT=<ID=INS,Description=\"Insertion of novel sequence relative to the reference\">\n")
	file.write("##ALT=<ID=DEL,Description=\"Deletion relative to the reference\">\n")
	file.write("##ALT=<ID=DUP,Description=\"Region of elevated copy number relative to the reference\">\n")
	file.write("##ALT=<ID=INV,Description=\"Inversion of reference sequence\">\n")
	file.write("##ALT=<ID=TRA,Description=\"Translocation\">\n")

	# INFO
	file.write("##INFO=<ID=PRECISE,Number=0,Type=Flag,Description=\"Precise structural variant\">\n")
	file.write("##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description=\"Imprecise structural variant\">\n")
	file.write("##INFO=<ID=SVTYPE,Number=1,Type=String,Description=\"Type of structural variant\">\n")
	file.write("##INFO=<ID=SVLEN,Number=1,Type=Integer,Description=\"Difference in length between REF and ALT alleles\">\n")
	file.write("##INFO=<ID=CHR2,Number=1,Type=String,Description=\"Chromosome for END coordinate in case of a translocation\">\n")
	file.write("##INFO=<ID=END,Number=1,Type=Integer,Description=\"End position of the variant described in this record\">\n")
	file.write("##INFO=<ID=CIPOS,Number=2,Type=Integer,Description=\"Confidence interval around POS for imprecise variants\">\n")
	file.write("##INFO=<ID=CIEND,Number=2,Type=Integer,Description=\"Confidence interval around END for imprecise variants\">\n")
	file.write("##INFO=<ID=MATEID,Number=.,Type=String,Description=\"ID of mate breakends\">\n")
	file.write("##INFO=<ID=RE,Number=1,Type=Integer,Description=\"Number of read support this record\">\n")

	# FORMAT
	# file.write("\n")
	file.write("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n")
	file.write("##FORMAT=<ID=DR,Number=1,Type=Integer,Description=\"# high-quality reference reads\">\n")
	file.write("##FORMAT=<ID=DV,Number=1,Type=Integer,Description=\"# high-quality variant reads\">\n")
	file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n"%(sample))