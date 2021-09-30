from os import system
import re
d = {'atc':'','sc':0,'method':False}
var = {'program':['method','']}
def format(txt):
	txt = txt.replace(r'\$',r'\dollar')
	for item,dt in var.items():
		txt = txt.replace(f'${item}',dt[1])
	txt = txt.replace(r'\dollar','$')
	return txt
def parse(code):
	global var
	code = re.sub(r'//[^\n]*','',code)
	if d['atc'] == '':
		cd = code
		code = code.split(' ')
		cmd = code[0]
		print(cmd)
		if cmd == 'START':
			d['sc'] += 1
			d['atc'] = code[1]
		elif cmd == 'COMMAND':
			var[code[1].split('=')[0]] = ['command',['',var[code[1].split('=')[1]][1],[]]]
			print(var[code[1].split('=')[0]])
		elif cmd == 'METHOD':
			var[code[1]] = ['method','']
		elif cmd == 'EXECUTE':
			dt = var[code[1]][1]
			om = d['method']
			d['method'] = True
			#ov = var
			#var = {}
			cnt = 0
			for item in dt[2]:
				var[str(cnt)] = item
				cnt += 1 
			for line in dt[1].split('\n'):
				parse(line)
			#var = ov
			d['method'] = om
		elif cmd == 'SYSRUN':
			if d['method']:
				system(format(cd.replace(cmd+' ','',1)))
		elif cmd == '':
			pass
		elif cmd == 'ADDATTRIBUTE':
			var[code[1].split('=')[0]][1][2].append(code[1].split('=')[1])
		else:
			print(f'CommandError: Unknown command "{cmd}".')
			quit()
	else:
		line = code
		if line.startswith('START'):
			d['sc'] += 1
			var[d['atc']][1] += line+'\n'
		elif line.startswith('END'):
			d['sc'] -= 1
			if d['sc'] == 0:
				cd = line
				code = line.split(' ')
				cmd = code[0]
				if cmd == 'END':
					d['atc'] = ''
		else:
			var[d['atc']][1] += line+'\n'
code = open(input('Filename: ')).read()
code += '\nCOMMAND i=program\nEXECUTE i'
for line in code.split('\n'):
	parse(line)
print(var)