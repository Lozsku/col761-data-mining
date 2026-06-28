#include<bits/stdc++.h>
using namespace std;
void check(string s1,string s2){
    fstream inp1(s1);
    ofstream output;
    output.open(s2);
    string k;
    while(getline(inp1,k)){
        // cout<<k<<endl;
        if(s1.empty()){
			break;
		}
		stringstream ss(k);
		string temp;
        vector<int> v;
        while(ss>>temp){
            v.push_back(stoi(temp));
        }

        sort(v.begin(),v.end());
        for(auto itm:v){
            output<<itm<< " ";
        }
        output<<"\n";
    }
    output.close();
    inp1.close();
}
int main(){
    string s1,s2;
    cin>>s1>>s2;
    check(s1,"out1.dat");
    check(s2,"out2.dat");
    return 0;
}
