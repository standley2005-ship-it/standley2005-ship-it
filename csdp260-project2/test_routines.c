/* Windows x64 harness: call the actual NASM arithmetic routines directly.
   These are real functional tests, separate from GUI validation. */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

extern long long calc_add(long long a,long long b);
extern long long calc_subtract(long long a,long long b);
extern long long calc_multiply(long long a,long long b);
extern long long calc_divide(long long a,long long b);

struct testcase {const char *name;long long a,b,expected;long long (*fn)(long long,long long);};
int main(void) {
 const struct testcase cases[]={
  {"Addition 10+5",10,5,15,calc_add},
  {"Addition 25+15",25,15,40,calc_add},
  {"Subtraction 20-8",20,8,12,calc_subtract},
  {"Subtraction 10-25",10,25,-15,calc_subtract},
  {"Multiply 6*4",6,4,24,calc_multiply},
  {"Multiply 12*5",12,5,60,calc_multiply},
  {"Divide 20/4 (scaled x10000)",20,4,50000,calc_divide},
  {"Divide 15/2 (scaled x10000)",15,2,75000,calc_divide},
  {"Divide 1/3 (scaled x10000)",1,3,3333,calc_divide},
  {"Divide -1/2 (scaled x10000)",-1,2,-5000,calc_divide},
  {"Multiply lower 32-bit boundary",-2147483648LL,-2147483648LL,4611686018427387904LL,calc_multiply},
  {"Add negatives",-10,5,-5,calc_add},
  {"Add 32-bit boundary",2147483647LL,2147483647LL,4294967294LL,calc_add}
 };
 FILE *f=fopen("evidence\\assembly_arithmetic_verified.csv","w");
 if(!f){perror("results");return 1;}
 fprintf(f,"Case,Input1,Input2,Expected,Observed,Pass\n");
 int errors=0;
 for(size_t i=0;i<sizeof(cases)/sizeof(cases[0]);i++){
  long long actual=cases[i].fn(cases[i].a,cases[i].b);
  int ok=(actual==cases[i].expected);
  printf("%s: %lld vs %lld -> %s\n",cases[i].name,actual,cases[i].expected,ok?"PASS":"FAIL");
  fprintf(f,"\"%s\",%lld,%lld,%lld,%lld,%s\n",cases[i].name,cases[i].a,cases[i].b,cases[i].expected,actual,ok?"PASS":"FAIL");
  if(!ok) errors++;
 }
 fclose(f);
 printf("NASM ROUTINES: %zu cases, %d failures\n",sizeof(cases)/sizeof(cases[0]),errors);
 return errors?1:0;
}
