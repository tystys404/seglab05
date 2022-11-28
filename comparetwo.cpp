#include<iostream>
#include<vector>
#include<string>
#include<map>
#include <fstream>
#include<sstream>
#include <iostream>
#include<random>
#include<stdio.h>
#include<string.h>
using namespace std;
string readFileIntoString(string filename)
{
    ifstream ifile(filename);
    ostringstream buf;
    char ch;
    while(buf&&ifile.get(ch))
    buf.put(ch);
    return buf.str();
}
vector<string> read_names(string pos)
{
    string data;
    data=readFileIntoString(pos);
    vector<string>names;
    names.push_back("");
    int flag=1;
    int j=0;
    for(int i=0;i<data.size();i++)
    {
        // if(data[i]=='\n') cout<<endl;
        // cout<<data[i];
        if(data[i]=='\n')
        {
            flag=1;
            names.push_back("");
            j++;
        }
        else if(data[i]=='.')
        {
            flag=0;
        }
        else if(flag==1)
        {
            names[j].push_back(data[i]);
        }
    }
    for(int k=0;k<names.size();k++)
        {
            for(int l=0;l<names[k].size();l++)
            {
                cout<<names[k][l];
            }
            cout<<endl;
        }
    return names;
}
void executeCMD(const char *cmd, char *result)
{
    char buf_ps[1024];
    char ps[1024]={0};
    FILE *ptr;
    strcpy(ps, cmd);
    if((ptr=popen(ps, "r"))!=NULL)
    {
        while(fgets(buf_ps, 1024, ptr)!=NULL)
        {
//	       可以通过这行来获取shell命令行中的每一行的输出
//	   	   printf("%s", buf_ps);
           strcat(result, buf_ps);
           if(strlen(result)>1024)
               break;
        }
        pclose(ptr);
        ptr = NULL;
    }
    else
    {
        printf("popen %s error\n", ps);
    }
}
int main(int argc,char* argv[])
{
    string pos1,pos2,pos;
    vector<string>tmp;
    char data[100];
    ifstream infile;
    infile.open("in.txt",ios::in);
    while(infile.getline(data,100))
    {
        string cur=data;
        tmp.push_back(cur);
    }
    pos=tmp[0];
    pos1=tmp[1];
    pos2=tmp[2];
    int flag=1;
    for(int k=0;k<50;k++)
    {
        string cmmd1="./randominput.out "+pos+" >randomin.txt";
        // cout<<cmmd1<<endl;
        char res1[1024]={};
        const char* cmd1=cmmd1.c_str();
        executeCMD(cmd1,res1);
        string cmmd2=pos1+" <randomin.txt";
        // cout<<cmmd2<<endl;
        char res2[1024]={};
        const char* cmd2=cmmd2.c_str();
        executeCMD(cmd2,res2);
        string cmmd3=pos2+" <randomin.txt";
        // cout<<cmmd3<<endl;
        char res3[1024]={};
        const char* cmd3=cmmd3.c_str();
        executeCMD(cmd3,res3);
        string ans1=string(res2);
        string ans2=string(res3);
        // cout<<ans1<<" "<<ans2;
        if(ans1!=ans2)
        {
            cout<<"no"<<endl;
            flag=0;
            break;
        }
    }
    if(flag==1) cout<<"yes";
    return 0;
}