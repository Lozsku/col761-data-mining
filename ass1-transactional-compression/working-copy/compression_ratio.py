import sys
def getNumberOfItems(path_):
  count = 0
  with open(path_, 'r') as fp:
    lines = fp.readlines()
    for line in lines:
      count += len(line.split(' '))
  return count

def getCompressionRatio(original_items_count, cdspath):
  compress_count = getNumberOfItems(cdspath)
  return (original_items_count - compress_count) / original_items_count

dspath = sys.argv[1]
original_items_count = getNumberOfItems(dspath)

ratio = getCompressionRatio(original_items_count, sys.argv[2])

print('Ratio: '+ str(ratio))
