color=['#000','#795548','#f44336','#ff9800','#ffeb3b','#51e756','#2196F3','#be3dd4','#757575','#fdf5e6','#9e7806','#b1b1b1']
band=[0,1,2,3,4,5,6,7,8,9,0,0]
toleranceLabel=['0','±1%','±2%','&nbsp;','&nbsp;','±0.5%','±0.25%','±0.10%','±0.05%','&nbsp;','±5%','±10%']
toleranceVal=[0,0.01,0.02,0,0,0.005,0.0025,0.001,0.0005,0,0.05,0.1]
multiplierLabel=['1Ω','10Ω','100Ω','1KΩ','10KΩ','100KΩ','1MΩ','10MΩ','&nbsp;','&nbsp;','0.1Ω','0.01Ω']
multiplierVal=[1e0,1e1,1e2,1e3,1e4,1e5,1e6,1e7,0,0,1e-1,1e-2];

y=0
for x in color:
    print("<tr>")
    for z in range(1,5):
        if z==1 or z==2:
            print("<td id=\"c"+str(z)+"r"+str(color.index(x))+"\" class=\"w3-col s3 m3 l3 w3-center res-btn\" style=\"border:1px solid black;background-color:"+x+"\" onclick=\"myvalue(this,"+str(z)+","+str(color.index(x))+")\">"+str(band[y])+"</td>");
        if z==3:
            print("<td id=\"c"+str(z)+"r"+str(color.index(x))+"\" class=\"w3-col s3 m3 l3 w3-center res-btn\" style=\"border:1px solid black;background-color:"+x+"\" onclick=\"myvalue(this,"+str(z)+","+str(multiplierVal[y])+")\">"+str(multiplierLabel[y])+"</td>");
        if z==4:
          print("<td id=\"c"+str(z)+"r"+str(color.index(x))+"\" class=\"w3-col s3 m3 l3 w3-center res-btn\" style=\"border:1px solid black;background-color:"+x+"\" onclick=\"myvalue(this,"+str(z)+","+str(toleranceVal[y])+")\">"+str(toleranceLabel[y])+"</td>");
    y+=1
    print("</tr>")
