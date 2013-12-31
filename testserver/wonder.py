
i,j=0,0
inp="LROE WLNFUDEF I!"

puzzle = [ [inp[x*4+y] for y in range(4)] for x in range(4)]


def get_position(s):
    ret =  ord(s[0]) - ord('a'), int(s[1]) - 1
    if 0 <= ret[0] <= 3 and 0 <= ret[1] <= 3:
        return ret
    else:
        raise Exception("Invalid board position")

exp_out="WONDERFUL LIFE! "
directory='/home/svpmtrust/output.txt'
fi=open(directory,'r')
for line in fi:
    line = line.strip()
    f_pos,t_pos = line.split('-')
    
    f_pos_r, f_pos_c = get_position(f_pos)
    t_pos_r, t_pos_c = get_position(t_pos)

    if (f_pos_r == t_pos_r and abs(f_pos_c - t_pos_c) == 1 or
        f_pos_c == t_pos_c and abs(f_pos_r - t_pos_r) == 1):
        # Move seems to be valid
        if puzzle[t_pos_r][t_pos_c] != ' ':
            raise Exception("Invalid Move - Target is not a space")
    else:
        raise Exception("Invalid Move - Too big move, almost a jump")

    puzzle[t_pos_r][t_pos_c] = puzzle[f_pos_r][f_pos_c]
    puzzle[f_pos_r][f_pos_c] = ' '

final_string = "".join("".join(p) for p in puzzle)

print final_string
if exp_out == final_string:
    print "Excellent"
else:
    print "too bad"
