import os
import re
import sys
import argparse

proto_dir = os.path.abspath(os.path.dirname(__file__))
compiled_proto_dir = os.path.abspath(
    os.path.join(proto_dir, '..', 'pycue', 'opencue', 'compiled_proto')
)
print(os.path.join(proto_dir, '..', 'pycue', 'opencue', 'compiled_proto'))

regex = re.compile(r'import (\w+)')


def run(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=compiled_proto_dir)

    namespace = parser.parse_args(args)
    path = namespace.path

    if not os.path.isdir(path):
        raise ValueError('Directory "{}" does not exist'.format(path))

    index = [os.path.splitext(x)[0] for x in os.listdir(path)
             if x.endswith('.py')]

    def sub_imports(result):
        if result:
            _mod = result.group(1)
            if _mod in index:
                return 'from . import {}'.format(_mod)
            return 'import {}'.format(_mod)

    for module in index:
        mod_path = os.path.join(path, module + '.py')

        with open(mod_path, 'r') as f:
            code = f.read()

        new_code = re.sub(regex, sub_imports, code)

        with open(mod_path, 'w') as f:
            f.write(new_code)


if __name__ == '__main__':
    run()
