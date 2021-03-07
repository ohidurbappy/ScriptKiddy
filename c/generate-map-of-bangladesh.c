#include <stdio.h>
int
main ()
{
  char str[] =
    "ED..GDAD..DLEB..COCC..CV..FS..HQ..JN..MP..Go..Cr..Cq..Cp..Fk..Jf..J`..I`..H`ID..J^HE..K^FG..N[ABCG..L`CG..MTBT..MUCS..NTDBCBAJ..NUBBHI..OTMI..OROI..OGDCSI..PE[I..RC[I..rBDB..rB..sB..tB";
  int c, i;
  for (i = 0; i < strlen (str); i++)
    {
      c = str[i] - 64;
      if (str[i] == 46)
	{
	  putchar (10);
	  ++i;
	}
      else if (i % 2 == 0)
	{
	  while (c != 0)
	    {
	      putchar (32);
	      c--;
	    }
	}
      else
	{
	  while (c != 0)
	    {
	      putchar (124);
	      c--;
	    }
	}
    }
}
