import sys
def getCleanTransactions(path_):
  ### Should handle duplicate items in transactions and duplicate transactions 
  clean_lines = []
  with open(path_, 'r') as fp:
    lines = fp.readlines()
    for line in lines:
      line = line.strip()
      if line == '':
        continue
      items = list(set(line.split(' '))) ## get items and remove duplicates
      items.sort(key = int) ## sort items by int order
      line = ' '.join(items) ## form back string of itemset
      clean_lines.append(line)
  clean_lines.sort()  ## sort all transactions in string order
  return set(clean_lines)


dspath = sys.argv[1]
d = getCleanTransactions(dspath)
d_decomp = getCleanTransactions(sys.argv[2])

loss = (len(d.union(d_decomp)) - len(d.intersection(d_decomp)))/len(d)

print("Loss: " + str(loss))
