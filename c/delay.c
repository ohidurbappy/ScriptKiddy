#include<stdio.h>
#include<time.h>

void delay(unsigned int mseconds)
{
clock_t goal = mseconds + clock();
while (goal > clock());
}

int main()
{
int i;
char str[]="Welcome to my Program";
for(i=0;i<sizeof(str);i++)
{
printf("%c",str[i]);
delay(500);
}
return 0;
}
