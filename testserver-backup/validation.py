input_text = 'abaabaabaczczczaaabcabcabc'

source = 'k*3p*3aal*3,k=aba,p=cz,l=abce'

r = source.split(',')
s1 = r[0]

print s1

ln = r.__len__()

for i in range(1,ln):
    ts = r[i]
    ss = ts.split('=')
    pt = s1.rfind(ss[0])
    s1 = s1.replace(ss[0], int(s1[pt+2])*ss[0])
    s1 = s1.replace(ss[0],ss[1])

pt1 = s1.rfind('*'); s1 = s1.replace(s1[pt1+1],'')
pt1 = s1.rfind('*'); s1 = s1.replace(s1[pt1],'')

 
if s1 == input_text:
    print 'success'
else:
    print 'failure'