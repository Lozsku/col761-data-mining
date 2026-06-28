#include<bits/stdc++.h>
#include<chrono>
using namespace std;
using namespace std::chrono;
#define int long long
map<int,vector<int>> decompressor;
map<vector<int>, int> compressor;
int curmax;
struct Node{
	Node* parent;
	vector<Node*> children;
	int data = 0;
	int frequency = 0;
	Node* next;

	Node(int data, int frequency, Node* parent){
		this->data = data;
		this->frequency = frequency;
		this->parent = parent;
	}
};

void modifyTree(Node* root, vector<pair<int, int>> &transaction, int pos, map<int, Node*> &headerTable){
	if(pos == transaction.size()){
		return;
	}
	for(int i = 0; i < root->children.size(); i++){
		if(root->children[i]->data == transaction[pos].first){
			root->children[i]->frequency += transaction[pos].second;
			modifyTree(root->children[i], transaction, pos + 1, headerTable);
			return;
		}
	}
	
	for(int i = pos; i < transaction.size(); i++){
		Node* temp = new Node(transaction[i].first, transaction[i].second, root);
		root->children.push_back(temp);
		root = temp;
		temp->next = headerTable[transaction[i].first];
		headerTable[transaction[i].first] = temp;
	}
	return;
}

void bfs(Node* root){
	queue<Node*> q;
	q.push(root);
	while(!q.empty()){
		Node* temp = q.front();
		q.pop();
		cout << temp->data << ": " << temp->frequency << endl;
		for(int i = 0; i < temp->children.size(); i++){
			q.push(temp->children[i]);
		}
	}
}

void printHeaderTable(map<int, Node*> &headerTable){
	for(auto x: headerTable){
		Node* temp = x.second;
		while(temp != NULL){
			cout << temp->data << " " << temp->frequency << "; ";
			temp = temp->next;
		}
		cout << endl;
	}
}

Node* createTree(string file, map<int, int> &freq, map<int, Node*> &headerTable){
	Node* root = new Node(-1, 0, NULL);

	// Read each transaction
	fstream inp2(file);
	string s;
	while (getline (inp2, s)){
		stringstream ss(s);
		string temp;
		vector<pair<int, int>> v;
		while(ss >> temp){
			if(freq.count(stoi(temp))){
				v.push_back({-1*freq[stoi(temp)], stoi(temp)});
			}
		}
		sort(v.begin(), v.end());
		vector<pair<int, int>> transaction;
		for(int i = 0; i < v.size(); i++){
			transaction.push_back({v[i].second, 1});
		}
		modifyTree(root, transaction, 0, headerTable);
	}
	inp2.close();
	// bfs(root);
	// printHeaderTable(headerTable);
	return root;
}

Node* createCondTree(vector<vector<pair<int, int>>> &paths, map<int, int> &freq, map<int, Node*> &headerTable){
	Node* root = new Node(-1, 0, NULL);

	// Read each transaction
	for(int i = 0; i < paths.size(); i++){
		vector<pair<int, pair<int, int>>> v;
		for(int j = 0; j < paths[i].size(); j++){
			if(freq.count(paths[i][j].first)){
				v.push_back({-1*freq[paths[i][j].first], paths[i][j]});
			}
		}
		sort(v.begin(), v.end());
		vector<pair<int, int>> transaction;
		for(int i = 0; i < v.size(); i++){
			transaction.push_back({v[i].second.first, v[i].second.second});
		}
		modifyTree(root, transaction, 0, headerTable);
	}
	return root;
}

vector<pair<int, int>> getPath(Node* node, int freq){
	vector<pair<int, int>> path;
	node = node->parent;
	while(node->parent != NULL){
		path.push_back({node->data, freq});
		node = node->parent;
	}
	reverse(path.begin(), path.end());
	return path;
}

void mineTree(int data, int threshold, int num_transactions, set<int> condset, map<int, Node*> &headerTable, vector<set<int>> &ans){
	vector<vector<pair<int, int>>> paths;
	Node* node = headerTable[data];
	while(node != NULL){
		paths.push_back(getPath(node, node->frequency));
		node = node->next;
	}

	map<int, int> condCount;
	map<int, Node*> condHeaderTable;
	set<int> distinctItems;
	vector<pair<int, int>> v;
	for(int i = 0; i < paths.size(); i++){
		for(int j = 0; j < paths[i].size(); j++){
			condCount[paths[i][j].first] += paths[i][j].second;
			distinctItems.insert(paths[i][j].first);
		}
	}

	for(auto itr = distinctItems.begin(); itr != distinctItems.end(); itr++){
		if(condCount[*itr] < threshold){
			condCount.erase(*itr);
		}
		else{
			v.push_back({condCount[*itr], *itr});
			condset.insert(*itr);
			ans.push_back(condset);
			condset.erase(*itr);
		}
	}

	if(v.size() == 0){
		return;
	}

	createCondTree(paths, condCount, condHeaderTable);
	sort(v.begin(), v.end());
	for(int i = 0; i < v.size(); i++){
		condset.insert(v[i].second);
		mineTree(v[i].second, threshold, num_transactions, condset, condHeaderTable, ans);
		condset.erase(v[i].second);
	}
}

// bool fun1(int i1, int i2){
// 	if(freq[i1] > freq[i2])
// 	{
// 		return 1;
// 	}
// 	else if(freq[i1] == freq[i2])
// 	{
// 		return i1 < i2;
// 	}
// 	return 0;
// }

void create_compressor(vector<vector<int>> &freq_sets){
	//cout << "Start: " << curmax << endl;
	//cout << freq_sets.size() << endl;
	for(auto it:freq_sets){
		compressor[it] = curmax+1;
		++curmax;
	}
	//cout << "Final: " << curmax << endl;
}

double compress_file(string file, string outfile, map<int, int> &freq){
	ofstream output;
	output.open(outfile);
	fstream inp2(file);
	string s1;
        int l1 = 0;
        int l2 = 0;
	int cnt1 = 0;
	int cnt2 = 0;
	while (getline (inp2, s1)){
		if(s1.empty()){
			break;
		}
                l1++;
		stringstream ss(s1);
		string temp;
		vector<int> curr;
		vector<int> prev;
		vector<pair<int, int>> transaction;
		while(ss >> temp){
			transaction.push_back({-1*freq[stoi(temp)], stoi(temp)});
			cnt1++;
		}
		sort(transaction.begin(), transaction.end());
		for(int i = 0; i < transaction.size(); i++)
		{
			int item = transaction[i].second;
			curr.push_back(item);
			if(compressor.find(curr)!=compressor.end())
			{
				prev = curr;
			}
			else
			{
				if(prev.size() > 1)
				{	
					// cout << prev.size() << endl;
					cnt2++;
					output << compressor[prev] << " ";
					decompressor[compressor[prev]] = prev;
				}
				else if(prev.size() == 1)
				{
					cnt2++;
					output << prev[0] << " ";
				}
				prev.clear();
				prev.push_back(item);
				curr = prev;
			}
		}
		if(prev.size() != 0)
		{
			if(compressor.find(prev) != compressor.end() && prev.size() != 1)
			{
				cnt2++;
				output << compressor[prev] << "\n";
				decompressor[compressor[prev]] = prev;
			}
			else
			{
				for(auto ele: prev)
				{
					cnt2++;
					output << ele << " ";
				}
				output << "\n";
			}
                        l2++;
		}
	}
	output << "\n";
	// cout << "############\n";
	for(auto it: decompressor)
	{
		//cout << (it.second).size() << endl;
		output << it.first << " ";
		cnt2++;
		for(auto ele: it.second)
		{
			cnt2++;
			output << ele << " ";
		}
		output << "\n";
	}
	while (getline (inp2, s1)){
		stringstream ss(s1);
		string temp;
		while(ss >> temp){
			cnt1++;
		}
	}
        //cout << "Lines in file 1 " << l1 << endl;
        //cout << "Lines in file 2 " << l2 << endl; 
	inp2.close();
	output.close();
	cout << "Integers in original and compressed files: " << cnt1 << ", " << cnt2 << endl;
	//cout << (double) (cnt1 - cnt2) / (double) cnt1 << endl;
	double compression = (double) (cnt1 - cnt2) / (double) cnt1;
	return compression;
}

void plot(map<int,int> &freq){
	map<int,int> freq_count;
	for(auto itm: freq){
		int a,b;
		a = itm.first;
		b = itm.second;
		++freq_count[b];
	}

	ofstream output;
	output.open("data.csv");
	for(auto itm: freq_count){
		int a,b;
		a = itm.first;
		b = itm.second;
		output<<a<<","<<b<<"\n";
	}
	output.close();
}

double mean(std::vector<int>& data) {
    if (data.empty()) {
        std::cerr << "Error: Empty vector provided." << std::endl;
        return 0.0;
    }
    
    double sum = 0.0;
    for (double num : data) {
        sum += num;
    }
    
    return sum / data.size();
}

double stddev(std::vector<int>& data) {
    if (data.empty()) {
        std::cerr << "Error: Empty vector provided." << std::endl;
        return 0.0;
    }
    
    double m = mean(data);
    double sumSquaredDiffs = 0.0;
    
    for (double num : data) {
        double diff = num - m;
        sumSquaredDiffs += diff * diff;
    }
    
    double variance = sumSquaredDiffs / data.size();
    return std::sqrt(variance);
}

int find_threshold(map<int, int> &freq, double percentile){
	vector<int> frequencies;
	for(auto itm: freq){
		frequencies.push_back(itm.second);
	}
	double p = percentile;
	//cout << mean(frequencies) << " " << stddev(frequencies) << endl;
// 	double pos = mean(frequencies) + p*stddev(frequencies);
//	if(pos < 0){
//		return mean(frequencies);
//	}
//	return abs(pos);
//	return frequencies[(int)pos]; 
	sort(frequencies.begin(), frequencies.end());
//	int pos = min(percentile*frequencies.size(), (double)frequencies.size()-1);
//	int p = percentile;
//	int pos=frequencies.size()*percentile;
	int pos;
	if(frequencies.size() < (int)(p*1000.0)){
		pos = frequencies.size()*(0.7/p);
	}
	else{
		pos = frequencies.size() -(int) (p*300.0);
	}
	//cout << "Pos: " << (int) (p*300.0) << " " << pos << endl;
//	plot(freq);
//	exit(1);
	return frequencies[pos];
//	plot(freq);
}

int fptree(string file, vector<set<int>> &ans, string outfile, double percentile){
	int num_transactions = 0;

	// Store frequency of itemsets
	//cout << "Start curmax: " << curmax << endl;
	map<int, int> freq;
	map<int, int> freq1;
	set<int> distinctItems;
	map<int, Node*> headerTable;
	vector<pair<int, int>> v;
	fstream inp1(file);
	string s;
	while (getline (inp1, s)){
		stringstream ss(s);
		string temp;
		num_transactions++;
		while(ss >> temp){
			freq[stoi(temp)]++;
			if(stoi(temp)>=curmax){
				curmax = stoi(temp);
			}
			headerTable[stoi(temp)] = NULL;
			distinctItems.insert(stoi(temp));
		}
	}
	inp1.close();
	int threshold = find_threshold(freq, percentile);
	//cout << "Thresholds: " << threshold << endl;
	for(auto itr = distinctItems.begin(); itr != distinctItems.end(); itr++){
		if(freq[*itr]>= threshold){
			freq1[*itr] = freq[*itr];
			set<int> S;
			S.insert(*itr);	
			ans.push_back(S);
			v.push_back({freq[*itr], *itr});
		}
	}
	sort(v.begin(), v.end());
	//cout << "Reading done" << endl;
	createTree(file, freq1, headerTable);
	//cout << "Creation done" << endl;
	for(int i = 0; i < v.size(); i++){
		set<int> S;
		S.insert(v[i].second);
		mineTree(v[i].second, threshold, num_transactions, S, headerTable, ans);
	}
	//cout << "Mining done" << endl;

	// cout << ans.size() << endl;
	vector<vector<int>> freq_sets;
	for(auto S: ans){
		vector<pair<int, int>> temp;
		for(auto ele: S){
			temp.push_back({-1*freq1[ele], ele});
		}
		sort(temp.begin(), temp.end());
		vector<int> temp_list;
		for(int i = 0; i < temp.size(); i++){
			temp_list.push_back(temp[i].second);
		}
		freq_sets.push_back(temp_list);
	}

	// cout << freq_sets.size() << endl;
	create_compressor(freq_sets);
	// cout << compressor.size() << endl;
	double compression = compress_file(file, outfile, freq1);
	cout << "Compression: " << compression*100 << endl;
	if(compression < 0.001){
		return 1;
	}
	return 0;
}

vector<string> customSort2(vector<set<int>> &V){
	vector<string> ans;
	for (auto itm: V){
		vector<int> temp;
		for(auto ele: itm){
			temp.push_back(ele);
		}
		sort(temp.begin(),temp.end());
		string s;
		for(int i = 0; i < temp.size(); i++){
			s += temp[i] + " ";
		}
		ans.push_back(s);
	}
	return ans;
}

vector<string> customSort(vector<set<int>> &V){
	vector<string> ans;
	for(auto S: V){
		vector<string> temp;
		for(auto ele: S){
			temp.push_back(to_string(ele));
		}
		sort(temp.begin(), temp.end());
		string s;
		for(int i = 0; i < temp.size(); i++){
			s += temp[i] + " ";
		}
		ans.push_back(s);
	}	
	sort(ans.begin(), ans.end());
	return ans;
}

void copy_file(string infile, string outfile){
    fstream inp(infile);
    ofstream output;
    output.open(outfile);
    string s;
//    cout << infile << endl;
    while(getline(inp,s)){
        stringstream ss(s);
        string temp;
        while(ss>>temp){
            output<<temp << " ";
        }
        output<<"\n";
    }
    inp.close();
    output.close();
    
}

signed main(int32_t argc, char* argv[]){
	string dataset = argv[1];
	string outName = argv[2];
	int n = 15;
	vector<string> outfile_names = {"compressed1.dat", "compressed2.dat"};
	auto start = high_resolution_clock::now();
	curmax = 0;
	double per = 1;
	for(int i = 0; i < n; i++){
		string outfile = outfile_names[i%2];
		vector<set<int>> V;
		int stop = fptree(dataset, V, outfile, per);
		dataset = outfile;
		per += 0.1;
		if(stop){
			per = per*1.5;
		}
		auto cur_time = high_resolution_clock::now();
		auto duration = duration_cast<std::chrono::minutes>(cur_time - start);
		if(duration.count() <  58){
			//cout << "Writing to file" << endl;
            		copy_file(outfile, outName);
        	}
	}
	auto end = high_resolution_clock::now();
	cout << "Time spent: " << duration_cast<milliseconds>(end - start).count() << endl;
	// getback_file(outName,"finalout.dat");
	// vector<string> ans = customSort(V);

	// ofstream output;
	// output.open(outName+".dat");

	// for(int i = 0; i < ans.size(); i++){
	// 	output << ans[i] << "\n";
	// }
	// output.close();
	return 0;
}
