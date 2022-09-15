"""Install a program as a service

Args:
  1: path to program
  2: name of service
"""
import sys

exec_path = sys.argv[1]
service_file_path = f'/lib/systemd/system/{sys.argv[2]}.service'

service_file_data = (
  '[Unit]\n'
  'Description=PiCounter\n'
  'After=network.target\n'
  '[Service]\n'
  f'ExecStart={exec_path}\n'
  'Restart=always\n'
  'User=pi\n'
  '[Install]\n'
  'WantedBy=multi-user.target\n')

with open(service_file_path, 'w') as sfp:
  sfp.write(service_file_data)
