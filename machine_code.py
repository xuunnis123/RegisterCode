import platform
import subprocess
import json
import base64
from argparse import ArgumentParser


def pack_machine_code(code):
    content = {
        'code': code,
        'version': 0
    }
    return base64.b64encode(bytes(json.dumps(content), 'utf-8')).decode()


def get_machine_code():
    hd_id_str = ''
    if platform.system() == 'Windows':
        hd_id_str = subprocess.check_output('wmic csproduct get UUID')
        hd_id_str = hd_id_str.decode().split('\n')[1].strip()
    else:
        dmidecode = subprocess.Popen(
            ['dmidecode'],
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        while True:
            line = dmidecode.stdout.readline()
            if "UUID:" in str(line):
                hd_id_str = str(line).split("UUID:", 1)[1].split()[0]
                break
            if not line:
                break
        dmidecode.wait()
        if int(dmidecode.returncode) != 0:
            return ''

    return pack_machine_code(hd_id_str.replace('-', '').upper())


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--output', type=str, dest="output", default='code.txt')
    args = parser.parse_args()

    code = get_machine_code()
    print('{padding} CODE START {padding}'.format(padding='*' * 35))
    print(code)
    print('{padding}  CODE END  {padding}'.format(padding='*' * 35))
    with open(args.output, 'w') as outfile:
        outfile.write(code.strip())
    input("Press any key to continue")
