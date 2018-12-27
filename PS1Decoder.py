#!/usr/bin/env python
import sys
import re
import math
import base64

val_entropy = 3.25
var_new_object = 0
var_generic = 0
var_int = 0
var_float = 0
var_string = 0
var_string_concat = 0
var_empty_string = 0
var_null = 0
var_true = 0
var_false = 0

def is_int(val):
    if type(val) == int:
        return True
    else:
    	try:
    		int(val)
    		return True
    	except:
    		return False

def is_float(val):
    if type(val) == float:
        return True
    else:
    	try:
    		float(val)
    		return True
    	except:
    		return False

def entropy(string):
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy

def var_rename(var_name, line):
	global var_generic
	global var_new_object
	global var_int
	global var_float
	global var_string
	global var_string_concat
	global var_empty_string
	global var_null
	global var_true
	global var_false

	init_var_rslt = re.findall(r'(' + re.escape(var_name) + r'(\s+)?\=((\s+)?(\'|\"|\$)?.+(\;)?))', line)

	for n_rslt in init_var_rslt:
		init_var = n_rslt[2].strip('\n; ')

		# check true
		if(init_var.lower() == '$true'):
			var_true = var_true + 1
			return('var_true_' + str(var_true))

		# check false
		if(init_var.lower() == '$false'):
			var_false = var_false + 1
			return('var_false' + str(var_false))

		# check null
		if(init_var.lower() == '$null'):
			var_null = var_null + 1
			return('var_null_' + str(var_null))

		# check new-object
		elif(init_var.find('New-Object') != -1 and init_var.find('New-Object') == 0):
			var_new_object = var_new_object + 1
			return('var_new_object_' + str(var_new_object))

		# check int
		elif(init_var.find('\'') == -1 and init_var.find('"') == -1 and init_var.find('$') == -1 and is_int(init_var)):
			var_int = var_int + 1
			return('var_int_' + init_var + '_' + str(var_int))

		# check float
		elif(init_var.find('\'') == -1 and init_var.find('"') == -1 and init_var.find('$') == -1 and is_float(init_var)):
			var_float = var_float + 1
			return('var_float_' + init_var.replace('.', '__') + '_' + str(var_float))

		# check empty string
		elif(init_var == '\'\'' or init_var == '""'):
			var_empty_string = var_empty_string + 1
			return('var_empty_str_' + str(var_empty_string))

		# check string
		elif(init_var[0] == '\'' or init_var[0] == '"') and (init_var[-1] == '\'' or init_var[-1] == '"'):
			concat_rslt = re.findall(r'(\'|\"|\})(\s+)?\+(\s+)?(\'|\"|\$)', init_var)

			if concat_rslt:
				var_string_concat = var_string_concat + 1
				return('var_str_concat_' + str(var_string_concat))
			else:
				var_string = var_string + 1
				return('var_str_' + init_var.replace('"', '').replace(' ', '_').replace('.', '__').replace('`', '_backslash_').replace('+', 'concat') + '_' + str(var_string))

		else:
			var_generic = var_generic + 1
			return('var_' + str(var_generic))
	
	var_generic = var_generic + 1
	return('var_' + str(var_generic))

def deobfuscate(input_file):
	var_func_count = 0

	print('[Info] Reading %s' % input_file)

	with open(input_file, 'r') as fp_all:
		cnt_all = fp_all.read()
	fp_all.close()

	with open(input_file, 'r') as fp:
		for cnt in enumerate(fp):
			# base64 decode
			base64_rslt = re.search(r'(\$\(\[Text.Encoding\]::(ASCII|Unicode)\.GetString\(\[Convert\]::FromBase64String\(\'(.+)\'\)\)\))', cnt[1])
			
			if base64_rslt:
				if base64_rslt.group(2) == 'ASCII':
					base64decode_rslt = base64_rslt.group(3).decode('base64')

				else:
					base64decode_rslt = base64_rslt.group(3).decode('base64').replace('\x00', '')

				cnt_all = cnt_all.replace(base64_rslt.group(0), '"' + base64decode_rslt.replace('"', '`"') + '"')

			# regex function
			var_func = re.findall(r'((?i)Function\s+(\w+)(\s+)?)', cnt[1])
			
			for n in var_func:
				# verifica entropia de la funcion encontrada
				entropy_rslt = entropy(n[1])

				if entropy_rslt >= val_entropy:
					cnt_all = cnt_all.replace(n[1], 'funcion_' + str(var_func_count))
					var_func_count = var_func_count + 1
	fp.close()

	for cnt in cnt_all.splitlines():
		# regex var
		var_rslt = re.findall(r'(\$(\{)?(global:|private:)?(\w+)(\})?)', cnt)

		for n in var_rslt:
			# verifica entropia de la variable encontrada
			entropy_rslt = entropy(n[3])

			if entropy_rslt >= val_entropy:
				cnt_all = cnt_all.replace(n[3], var_rename(n[0], cnt))

	output_filename = input_file[:-4] + '_decoded.ps1'
	print('[Info] Generating %s_decoded.ps1 file ...' % input_file[:-4])

	with open(output_filename, 'w') as fp:
		fp.write(cnt_all)
		fp.close()
	return

def usage():
	print('%s script_powershell.ps1' % sys.argv[0])

def main():
	print('PS1 Decoder by .:UND3R:.\n')
	if len(sys.argv) != 2:
	  	usage()
	  	exit()

	deobfuscate(sys.argv[1])
	print('[Info] %s decoded successfully :}' % sys.argv[1])

if __name__== '__main__':
  main()