import sys
from pip._internal import main as pip_main

def install(package):
  pip_main(['install', package])

failed_libs = []
if __name__ == '__main__':
  with open(sys.argv[1]) as f:
    for line in f:
      try:
        install(line)
      except:
        print("-"*80)
        print("Failed to install", line)
        failed_libs.append(line)
        print("-"*80)

    print("-"*80)
    print("Failed to install", failed_libs)
    print("-"*80)
