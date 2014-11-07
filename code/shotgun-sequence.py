import fileinput

# NOTE: Developed on Python 2.7.6

# All of the short reads
# At each iteration, this list will have
# two reads removed and one concatenation added
# of the two short reads -- the two with the largest overlap
reads = []

# Finds the shortest superstring
# of the two given strings
# runtime = O(k^2)
def find_shortest_superstring(s1, s2):
  # some weird shit here
  # overlap from beginning of s1 and end of s2
  if s1 == "" or s2 == "":
    #print("You dun goofed")
    exit(1)
  if len(s1) > len(s2):
    bigger = s1
    smaller = s2
  else:
    bigger = s2
    smaller = s1
  small_size = len(smaller)
  big_size = len(bigger)
  # see if smaller is contained in bigger
  for i in range(big_size-small_size):
    if smaller == bigger[i:i+small_size]:
      return bigger
  # Find largest overlap, tail of smaller, start of bigger
  # start from biggest overlap and work outwords from both sides
  for i in range(small_size):
    if smaller[i:] == bigger[0:small_size-i]:
      return smaller + bigger[small_size-i:]
    if smaller[0:small_size-i] == bigger[big_size-small_size+i:]:
      return bigger + smaller[small_size-i:]
  # no overlap found, return the bare concatenation
  return smaller + bigger


for line in fileinput.input():
    line = line.strip()
    reads.append(line)

best_superstring = None
best_index = None
best_overlap = None

while len(reads) != 1:
  r1 = reads.pop(0)
  for i in range(len(reads)):
    r2 = reads[i]
    concat = find_shortest_superstring(r1, r2)
    overlap = len(r1) + len(r2) - len(concat)
    if best_overlap == None or overlap > best_overlap:
      best_overlap = overlap
      best_index = i
      best_concat = concat
  reads.pop(best_index)
  reads.append(best_concat)
  best_superstring = None
  best_index = None
  best_overlap = None

print(reads[0])

