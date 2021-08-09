x=1000

for y in range(1,500):
	if x%2==1:
		x=3*x+1
	else:
		x=x/2
	print(x)
