#include<cstdio>
using namespace std;
short a[6200][2900];
float ans[6200][6200];
int main(int num,char** arg)
{
	freopen(("%s",arg[num-2]),"r",stdin);
	for(int i=0;i<6194;i++)
		for(int j=0;j<2848;j++)
			scanf("%d",&a[i][j]);
	for(int i=0;i<10;i++)
	{
		for(int j=i+1;j<10;j++)
		{
		    int x=0,y=0;
		    float c=0.0;
            while(x<2848&&y<2848)
            {
            	if(a[i][x]==a[j][y])
            	{
            		c++;
            		x++;
            		y++;
            	}
            	else if(a[i][x]<a[j][y])
            	{
            		x++;
            	}
            	else y++;
            }
            ans[i][j]=ans[j][i]=c/(2848*2-c);
		}
		printf("complete %.4f\n",100*i/6194);
	}
	freopen(("%s",arg[num-1]),"w",stdout);
	for(int i=0;i<10;i++)
	{
		for(int j=0;j<10;j++)
		{
           if(i==j)printf("1 ");
           else printf("%f ",ans[i][j]);
		}
		printf("\n");
	}
}