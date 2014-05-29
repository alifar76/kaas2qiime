# https://raw.githubusercontent.com/ivan-kryukov/Kegg-Htext-Parser/master/ko00001.keg
import os, sys, subprocess, re
from datetime import datetime


def cat_kaas_output(outputname):
	""" Function to merge KAAS output files into one file """
	kaasfiles = ""
	val = "ls *_kaas.txt"
	p = subprocess.Popen([val], shell=True, stdout=subprocess.PIPE)
	for files in p.stdout:
		kaasfiles += files.strip()+" "
	os.system("cat %s > %s" % (kaasfiles.strip(),outputname))
	return


def kass_combined_matrix(combinedfile,matrixout):
	""" Function to create KOs by Samples table for downstream analysis """
	kos = []
	infile = open(combinedfile,'rU')
	for line in infile:
		spline = line.strip().split()
		if len(spline) != 1:
			kos.append(spline[1].strip())
	unique = list(set(kos))
	val = "ls *_kaas.txt"
	outfile = open(matrixout, 'w')
	outfile.write("# Constructed from biom file"+"\n")
	filenames = []
	filenames.append('#OTU ID')
	p = subprocess.Popen([val], shell=True, stdout=subprocess.PIPE)
	for files in p.stdout:
		filenames.append(files.strip().split("_")[0])
	outfile.write('\t'.join(filenames)+"\n")
	filenames = []
	for x in unique:
		counts = []
		counts.append(x)
		p = subprocess.Popen([val], shell=True, stdout=subprocess.PIPE)
		for files in p.stdout:
			infile = open(files.strip(), 'rU')
			ko_count = 0
			for line in infile:
				spline = line.strip().split()
				if len(spline) != 1:
					if spline[1] == x:
						ko_count += 1
			counts.append(str(ko_count))
		filenames.append(counts)
	final_kos = sorted(filenames)
	for kosvals in final_kos:
		outfile.write('\t'.join(kosvals)+"\n")
	outfile.close()
	return outfile


def keggParse(filename,comparefile,keggdbfile):
	""" Function to parse KEGG database flatfile"""
	ko = []
	infile = open(comparefile, 'rU')		
	for line in infile:
		spline = line.strip().split("\t")
		ko.append(spline[0])
	unique = list(set(ko))
	outfile = open(filename,"w")
	for x in unique:
		class1_list = []
		class2_list = []
		class3_list = []
		infile = open(keggdbfile, 'rU')	
		for line in infile:
			striped = line.strip()
			kegg = re.compile(r"%s" % x).search(striped)
			class1 = re.compile(r"^A").search(striped)
			class2 = re.compile(r"^B").search(striped)
			class3 = re.compile(r"^C").search(striped)
			if class1:
				class1_list.append(striped)
			if class2:
				class2_list.append(striped)
			if class3:
				class3_list.append(striped)
			if kegg:
				outfile.write(x+"\t")
				outfile.write("KEGG Pathways"+"\t")
				outfile.write(class1_list[len(class1_list)-1].split("<b>")[1].split("</b>")[0].strip()+"\t")
				outfile.write(class2_list[len(class2_list)-1].split("<b>")[1].split("</b>")[0].strip()+"\t")
				outfile.write(re.split('\d\d\d\d\d', class3_list[len(class3_list)-1])[1].split("[")[0].strip()+"\n")						
	outfile.close()
	return outfile		
			

def metaData(filename,parsefile,kaasmatrix):
	""" Function to create metadata file to add via biom add-metadata command"""
	outfile = open(filename, 'w')
	outfile.write("#OTUID"+"\t"+"KEGG_Pathways"+"\n")
	ko = []
	infile = open(parsefile, 'rU')
	for line in infile:
		if not line.startswith("#"):
			ko.append(line.strip().split("\t")[0])
	for x in list(set(ko)):
		funcs = ""
		infile = open(parsefile, 'rU')
		for line in infile:
			if not line.startswith("#"):
				spline = line.strip().split("\t")
				if spline[0] == x:
					funcs += ";".join(spline[2:])
					funcs += "|"
		outfile.write(x+"\t"+funcs[:-1]+"\n")
	ko_check = []
	infile1 = open(kaasmatrix, 'rU')
	for line in infile1:
		if not line.startswith("#"):
			ko_check.append(line.strip().split("\t")[0])
	kegg_parse = []
	infile2 = open(parsefile, 'rU')
	for line in infile2:
		if not line.startswith("#"):
			kegg_parse.append(line.strip().split("\t")[0])
	for x in ko_check:
		if x not in kegg_parse:
			outfile.write(x+"\t"+"null"+"\n")
	outfile.close()
	return outfile	
			
			
if __name__ == "__main__":
	startTime = datetime.now()
	cat_kaas_output("combinedOutput.txt")
	kass_combined_matrix("combinedOutput.txt","kaasbiom_convert.txt")
	keggParse("Kegg_parse.txt","kaasbiom_convert.txt","ko00001.keg")		# Comparing all KAAS KEGGS
	metaData("metadata.txt","Kegg_parse.txt","kaasbiom_convert.txt")
	os.system('biom convert -i kaasbiom_convert.txt -o kaas_output.biom --table-type="ortholog table"')
	os.system('biom add-metadata -i kaas_output.biom -o kaas_meta_plus.biom --observation-metadata-fp metadata.txt --sc-pipe-separated KEGG_Pathways')
	os.system('categorize_by_function.py -i kaas_meta_plus.biom -c "KEGG_Pathways" -l 3 -o kaas_level3.biom')
	os.system('summarize_taxa_through_plots.py -i kaas_level3.biom -p qiime_params.txt -o plots_level3')
	print "\n"+"Task Completed! Time it took to complete the task: "+ str(datetime.now()-startTime)

