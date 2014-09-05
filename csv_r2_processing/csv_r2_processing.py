#/usr/bin/env python

import csv
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

if __name__ == "__main__":
  r3 = R2(sys.argv[2])
  csv_file_path = sys.argv[1]
  csv_file = csv.reader(open(csv_file_path, 'rb'), delimiter=',', quotechar='"')
  cmd_name = csv_file.next()
  r2_cmds = csv_file.next()
  csv_file = csv.writer(open(csv_file_path, 'w+b'), delimiter=',', quotechar='"')
  csv_file.writerow(cmd_name)
  csv_file.writerow(r2_cmds)
  r2_result = []
  for r2_cmd in r2_cmds:
     r2_result.append(r3.cmd(r2_cmd))
  csv_file.writerow(r2_result)