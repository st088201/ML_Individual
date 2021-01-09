line1 = str(input())
line2 = str(input())

line1 = line1.strip()
line2 = line2.strip()
len1 = len(line1)
len2 = len(line2)

# Step 1:  Creating matrix of zeros for future usability

score = [[0]*(len1+1) for i in range(len2+1)]

# Step 2: Setting weight of various cases of letters mutual status

weight_match = 1
weight_mismatch = -1
weight_gap = -1

# Step 3: defining function to check two letters status: match, mismatch, or one of them is '-'


def match_score(first, second):
    if first == second:
        return weight_match
    elif first == '-' or second == '-':
        return weight_gap
    else:
        return weight_mismatch


# Step 3: Creating similarity matrix

for j in range(0, len1 + 1):
    score[0][j] = - j
for i in range(0, len2 + 1):
    score[i][0] = - i
for j in range(1, len1 + 1):
    for i in range(1, len2 + 1):
        # Calculate the score by checking the top, left, and diagonal cells
        match = score[i - 1][j - 1] + match_score(line1[j - 1], line2[i - 1])
        delete = score[i - 1][j] + weight_gap
        insert = score[i][j - 1] + weight_gap
        # Record the maximum score from the three possible scores calculated above
        score[i][j] = max(match, delete, insert)

# Step 4: Backtracking alignment

# Setting variables to store alignment
align1 = ""
align2 = ""

# Start from bottom right cell of matrix
j = len1
i = len2

while i > 0 and j > 0:
    # (in that case we'll touch top or left edge of the matrix)
    score_current = score[i][j]
    score_diagonal = score[i - 1][j - 1]
    score_up = score[i][j - 1]
    score_left = score[i - 1][j]

    # Check to figure out which cell the current score was calculated from,
    # then update i and j to correspond to that cell.
    if score_current == score_diagonal + match_score(line1[j - 1], line2[i - 1]):
        align1 += line1[j - 1]
        align2 += line2[i - 1]
        i -= 1
        j -= 1
    elif score_current == score_up + weight_gap:
        align1 += line1[j - 1]
        align2 += '-'
        j -= 1
    elif score_current == score_left + weight_gap:
        align1 += '-'
        align2 += line2[i - 1]
        i -= 1

# Then we finish tracing up to the top left cell
while j > 0:
    align1 += line1[j - 1]
    align2 += '-'
    j -= 1
while i > 0:
    align1 += '-'
    align2 += line2[i - 1]
    i -= 1

# Our alignments were constructed from end to start of actual lines, so we reverse them to get actual answer
align1 = align1[::-1]
align2 = align2[::-1]

print(align1 + "\n" + align2)
input('Press ENTER to exit')