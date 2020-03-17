# LyfeOnEdge March 17 2020
# GPL3
# Python3 module / script for generating .edz style archives.
import os, sys, time, struct, zipfile, random
from uuid import UUID
from io import BytesIO

MAGIC = 0x4E5A4445 #EDZN
u64_MAX = 0xFFFFFFFFFFFFFFFF

# Original zipit code:
# http://stackoverflow.com/a/6078528
#
# Call `zipit` with the path to either a directory or a file.
# All paths packed into the zip are relative to the directory
# or the directory of the file.

# zipit has been modified to not require an archive name (since it's not writing to one)
# it now uses a bytes object to store the zip contents so it never hits disk
def zipit(path):
	virtual_zip = BytesIO()
	archive = zipfile.ZipFile(virtual_zip, "w", zipfile.ZIP_DEFLATED)
	if os.path.isdir(path):
		_zippy(path, path, archive)
	else:
		_, name = os.path.split(path)
		archive.write(path, name)
	return virtual_zip
	
def _zippy(base_path, path, archive):
	paths = os.listdir(path)
	print(paths)
	for p in paths:
		p = os.path.join(path, p)
		if os.path.isdir(p):
			_zippy(base_path, p, archive)
		else:
			archive.write(p, os.path.relpath(p, base_path))

class Edizip:
	"""Object to handle zipping edizip files"""
	def __init__(self, magic = MAGIC):
		self.magic = magic

	def set_magic(self, magic: int):
		"""Change magic"""
		self.magic = magic

	def generate_random_UID(self):
		"""Generate a random UID for the header"""
		UID = random.randint(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
		print(f"Generated random UID {UID}")
		return UUID(int=UID)

	def make_header(self, TID: int, UID: int, DELTA: bool = False):
		"""returns an edz header in bytes object form"""
		t = int(time.time()) #Get current time since epoch in decimal
		print(f"Making header: Magic - {self.magic}, TID - {TID}, UID - {UID}, Delta - {DELTA}, Timestamp - {t}")
		packed_header = struct.pack("<IQQQQ?",
			int(self.magic), #u32 - I
			int(TID), #u64 - Q
			int((UID.int >> 64) & u64_MAX), #u128 1/2 - Q
			int(UID.int & u64_MAX), #u128 2/2 - Q
			int(t),  #u64 - Q
			DELTA # bit - ?
		)
		print(f"Header: {packed_header}")
		return packed_header

	def edizip(self, header, target: str, output_target: str = None):
		"""Function to make edizip, returns edz location if sucessful"""
		try:
			target = os.path.abspath(target)
			if output_target:
				outfile = output_target
			else:
				outfile = os.path.join(target, os.path.basename(target) + ".edz")
			#Zip target dir
			print(f"Creating virtual zip of {target}")
			zip_bytes_object = zipit(target)
			print(f"Making .edz at {outfile}...")
			with open(outfile, "w+b") as out:
				print("Writing header...")
				out.write(header)
				print("Writing zip contents...")
				out.write(zip_bytes_object.getvalue())
			print("Success!")
			return outfile
		except Exception as e:
			print(f"Failed to create edizip from target {target} - {e}")
			print("Attempting cleanup...")
			try:
				if os.path.isfile(outfile):
					print(f"Removing possibly invalid archive {outfile}")
					os.remove(outfile)
			except:
				pass

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("target", help = "Target dir to archive")
	parser.add_argument("--output", help = "edizip output location, defaults to `target/target.edz` if not set")
	args = parser.parse_args()

	zipper = Edizip()
	uid = zipper.generate_random_UID()
	header = zipper.make_header("0", uid)
	zipper.edizip(header, args.target, args.output)