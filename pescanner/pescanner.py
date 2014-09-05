#/usr/bin/env python
import pexpect
import json
import sys

class R2:
  def __init__(self, filename):
    self.process = pexpect.spawn('r2', ['-q0', filename])
    self._expect_eof_()
  
  def _expect_eof_(self):
    self.process.expect("\x00")
  
  def cmd(self, cmd):
    self.process.sendline(cmd)
    self._expect_eof_()
    return self.process.before

  def cmd_json(self, cmd):
    return json.loads(self.cmd(cmd))

  def get_metadata(self):
    infos = self.cmd_json("ij")
    file_path = infos['core']['file']
    file_size = infos['core']['size']
    file_type = "This should be gathered from /m at magic offset but not working correctly"
    date = "Not yet implemented in R2"
    ep = hex(self.cmd_json("iej")[0]) 
    crc = self.cmd("#crc32 $s @ 0").replace("\n","").replace("\r","")
    md5 = self.cmd("#md5 $s @ 0").replace("\n","").replace("\r","")
    sha1 = self.cmd("#sha1 $s @ 0").replace("\n","").replace("\r","")
    ssdeep = "Not yet implemented in R2"

    print ("\nMeta-data")
    print ("================================================================================")
    print ("File:	%s" 				% file_path)
    print ("Size:	%d bytes"			% file_size)
    print ("Type:	%s" 				% file_type)
    print ("MD5:	%s" 				% md5)
    print ("SHA1:	%s" 				% sha1)
    print ("Ssdeep:	%s" 				% ssdeep)
    print ("Compilation date:	%s"  			% date)
    print ("EP:	%s <- This looks false"			% ep)
    print ("CRC:	%s <- This looks false"		% crc)

  def get_sections(self):
    print ("\nSections")
    print ("================================================================================")
    print ("Name		VirtAddr		VirtSize		RawSize	Entropy		")
    print ("--------------------------------------------------------------------------------")
    for section in self.cmd_json("iSj"):
        print ("{}		{}		Not in iSj		{}	TODO".format(section["name"],hex(section["vaddr"]),hex(section["size"])))

  def get_yara(self):
    print ("\nYara Result")
    print ("================================================================================")
    print self.cmd("yara scan")

  def get_suspicious_api(self):
    print ("Imports")
    print ("================================================================================")
    for imports in self.cmd_json("iij"):
        print ("%s" % imports["name"])

  def get_rsrc(self):	
    print ("\nResources")
    print ("================================================================================")
    print("Not implemented in r2")

  def get_tls(self):	
    print ("\nTLS")
    print ("================================================================================")
    print("Not implemented in r2")

  def get_version_info(self):	
    print ("\nVersion Info")
    print ("================================================================================")
    print("Not implemented in r2")


if __name__ == "__main__":
  r3 = R2(sys.argv[1])
  r3.get_metadata()
  r3.get_sections()
  r3.get_yara()
  r3.get_suspicious_api()
  r3.get_rsrc()
  r3.get_tls()
  r3.get_version_info()
