#
# Rift Artifact Location Fetcher
#
# Developed by Emanuel Claesson (https://github.com/EClaesson)
# This is for Python 2.7.3, there are no guarantee it will work properly on other versions.
# This script is under public domain.
# The data is fetched from Telarapedia.com and is released under Attribution-NonCommercial-ShareAlike 3.0 Unported (http://creativecommons.org/licenses/by-nc-sa/3.0/)
#
# Warning for the faint hearted. The code below is not very well structured. :(
#

import sys, urllib2, re, json, os

zones = ['Silverwood', 'Stonefield', 'Gloamwood', 'Scarlet_Gorge', 'Scarwood_Reach', 'Moonshade_Highlands', 'Iron_Pine_Peak', 'Shimmersand', 'Stillmoor', 'Freemarch', 'Droughtlands']

if len(sys.argv) == 4:
	zone   = sys.argv[1]
	format = sys.argv[2].lower()
	split  = sys.argv[3].lower()
	
	if format not in ['json', 'lua']:
		print('Unknown output format')
		sys.exit()
		
	if split not in ['true', 'false']:
		print('Unknown split flag')
		sys.exit()
		
	split = split == 'true'
	
	zones_to_fetch = []
	
	fetched_data = {}
	
	if zone == '*':
		for z in zones:
			zones_to_fetch.append(z)
	else:
		for z in zone.split(','):
			if z not in zones:
				print('Unknown zone')
				sys.exit()
			zones_to_fetch.append(z)
			
	for z in zones_to_fetch:
		url = ''
	
		if z == 'Freemarch': # Non-consistent format
			url = 'http://telarapedia.com/wiki/Freemarch_artifact_locations/coordinates'
		
		elif z == 'Droughtlands': # Non-consistent format
			url = 'http://telarapedia.com/wiki/Droughtlands_artifact_locations'
			
		else:
			url = 'http://telarapedia.com/wiki/' + z + '_artifact_locations#tab=Location_List'
			
		print('Fetching ' + z + ' (' + url + ')'),
		
		data = urllib2.urlopen(url).read()
		
		print(str(len(data)) + ' bytes')
		
		reg = re.compile('(\\d+),(\\d+)', re.IGNORECASE | re.DOTALL)
		matches = re.findall(reg, data)
		fetched_data[z] = []
		
		for m in matches:
			fetched_data[z].append((int(m[0]), int(m[1])))
			
	output= ''
	file = None
	
	if not os.path.exists('fetched'): os.makedirs('fetched')
	
	for k, v in fetched_data.iteritems():
		if format == 'json':
			output = json.dumps({k: v}, sort_keys = True, indent = 4, separators = (',', ': '))
		
		else:
			output = ''
			output += k + '_artifacts = {\n'
			
			for val in v:
				output += '\t{' + str(val[0]) + ', ' + str(val[1]) + '},\n'
			
			output += '}'
	
		output += '\n\n'
	
		if not split:
			if file == None:
				file = open('fetched/artifacts.' + format, 'w')
				
			file.write(output)
			file.flush()
			
		else:
			file = open('fetched/' + k + '_artifacts.' + format, 'w')
			file.write(output)
			print('Wrote \'fetched/' + k + '_artifacts.' + format + '\'')
			file.flush()
			
	if not split:
		print('Wrote \'fetched/artifacts.' + format + '\'')
		
	file.close()
	
	print('[DONE]')
	
else:
	print("""Usage: python art-fetch.py <zone> <format> <split>
	zone   : Comma-separated (no-spaces) list of zones, or * for all.
	format : lua or json
	split  : true if you want each zone in a separate file, false otherwise
	
	Zone Names:""")
	
	for zone in zones:
		print("\t" + zone)