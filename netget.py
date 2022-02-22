import requests
import sys
import time

units = {	
'B' : {'size':1, 'speed':'B/s'},
'KB' : {'size':1024, 'speed':'KB/s'},
'MB' : {'size':1024*1024, 'speed':'MB/s'},
'GB' : {'size':1024*1024*1024, 'speed':'GB/s'}
}

def check_unit(length): # length in bytes
	if length < units['KB']['size']:
		return 'B'
	elif length >= units['KB']['size'] and length <= units['MB']['size']:
		return 'KB'
	elif length >= units['MB']['size'] and length <= units['GB']['size']:
		return 'MB'
	elif length > units['GB']['size']:
		return 'GB'

# takes download link and directory where file to be saved.
def downloadFile(url, directory) :

	localFilename = url.split('/')[-1] # files name

	with open(directory + '/' + localFilename, 'wb') as f:
		print ("Downloading . . .\n")
		start = time.time() # start time
		r = requests.get(url, stream=True)

		# total length in bytes of the file
		total_length = float(r.headers.get('content-length'))

		d = 0 # counter for amount downloaded

		# when file is not available
		if total_length is None:
			f.write(r.content)
		else:
			for chunk in r.iter_content(8192):
				
				d += float(len(chunk))
				f.write(chunk) # writing the file in chunks of 8192 bytes

				# amount downloaded in proper units
				downloaded = d/units[check_unit(d)]['size']
				
				# converting the unit of total length or size of file from bytes.
				tl = total_length / units[check_unit(total_length)]['size']
				
				trs = d // (time.time() - start) # speed in bytes per sec
				
				#speed in proper unit
				download_speed = trs/units[check_unit(trs)]['size']
				
				speed_unit = units[check_unit(trs)]['speed'] # speed in proper units

				done = 100 * d / total_length # percentage downloaded or done.
				
				fmt_string = "\r%6.2f %s [%s%s] %7.2f%s / %4.2f %s %7.2f %s"
				
				set_of_vars = ( float(done), '%',
								'*' * int(done/2),
								'_' * int(50-done/2),
								downloaded, check_unit(d),
								tl, check_unit(total_length),
								download_speed, speed_unit)

				sys.stdout.write(fmt_string % set_of_vars)

				sys.stdout.flush()

	return (time.time() - start) # total time taken for download

def main() :
	directory = '.'
	if len(sys.argv) > 1 :
		url = sys.argv[1] # url from cmd line arg
		if len(sys.argv) > 2:
			directory = sys.argv[2]
		
		total_time = downloadFile(url, directory)
		print ('')
		print ("Download complete...")
		print("Thank you for using Zanvok NetGet Download Utility")
		print ("\rTime Elapsed: %.2fs" % total_time)
	else :
		print("No link found!")

if __name__ == "__main__" :
	main()
