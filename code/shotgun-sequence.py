import fileinput
import Queue

# All of the short reads
# At each iteration, this list will have
# two reads removed and one concatenation added
# of the two short reads -- the two with the largest overlap
reads = []

# A priority queue keeping track of
# the max overlap between pairs of strings
queue = Queue.PriorityQueue()

# Finds the shortest superstring
# of the two given strings
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


def add_to_queue(i, j):
  s1 = reads[i]
  s2 = reads[j]
  combined = find_shortest_superstring(s1, s2)
  #print("combined " + s1 + " and " +s2+ " to find " + combined)
  overlap = len(s1) + len(s2) - len(combined)
  queue.put((-overlap, combined, i, j))


for line in fileinput.input():
    line = line.strip()
    reads.append(line)

# loop over n choose 2 pairs of short reads
# and add them to the queue
for i in range(len(reads)-1):
  s1 = reads[i]
  for j in range(i+1, len(reads)):
    add_to_queue(i, j)
    
# Get the most overlapping pair and process it,
# cancel out the old strings, add the new one in
while queue.qsize() > 0:
  # pop from the queue to see which reads should be merged next
  best_pair_info = queue.get()
  i, j = best_pair_info[2:]
  combined_string = best_pair_info[1]
  
  # if either string has previous been merged, continue...
  if reads[i] == None or reads[j] == None:
    continue

  # cancel out the now-merged reads
  reads[i] = None
  reads[j] = None

  # append the new, larger read
  reads.append(combined_string)

  # compare remaining short reads to this new combined read
  # and add the comparisons to the queue
  for i in range(len(reads)-1):
    if reads[i] != None:
      add_to_queue(i, len(reads)-1)

print(reads[-1])
   

