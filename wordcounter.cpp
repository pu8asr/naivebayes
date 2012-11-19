/**
 * Given a directory, outputs the frequency of each unique word in all files
 * in the directory. Assumes each file has 1 line, the length of which < 1M.
 */

#include<map>
#include<set>
#include<cstdio>
#include<dirent.h>
#include<iostream>
#include<errno.h>
using namespace std;

const int MAX_FILE_CHARS = 1000001;
char line[MAX_FILE_CHARS];

typedef pair<string, int> pci;
struct cmpFunc2 {
  bool operator()(const pair<string, int>&a, const pair<string, int>&b) const {
    return (a.second > b.second ||
            a.second == b.second && a.first < b.first);
  }
};
map<string, int> freq;

int main(int argc, char** argv) {
  // Open directory
  string inputDir = argv[1];
  if(*inputDir.end() != '/')
    inputDir += '/';
  DIR* dir = opendir(inputDir.c_str());
  dirent* entry;

  while(entry = readdir(dir)) {
    if(strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
      continue;

    // Open file
    string fullPath = inputDir + entry->d_name;
    FILE* f = fopen(fullPath.c_str(), "r");
    if(f == NULL) {
      cerr << "Error opening file " << fullPath << ", Error: "
           << strerror(errno) << endl;
      exit(1);
    }
    if(atoi(entry->d_name) % 1000 == 0) {
      cerr << "Processing file " << entry->d_name << endl;
    }
    
    // Read line. The way the crawler is written, there is only 1 line per file
    fgets(line, 1000000000, f);
    int len = strlen(line);
    if(line[len-1] == '\n')
      line[len-1] = '\0';

    // Tokenize
    char* pch;
    pch = strtok(line, " ");
    map<string, int>::iterator it;
    while(pch != NULL) {
      string pch_s = pch;
      it = freq.find(pch_s);
      if(it == freq.end()) {
        freq.insert(make_pair(pch_s, 1));
      }
      else {
        it->second++; 
      }
      pch = strtok (NULL, " ");
    }

    // Close file
    fclose(f);
  }

  // Sort in decreasing order of frequency and print
  set<pair<string, int>, cmpFunc2> S;
  for(map<string, int>::iterator it = freq.begin(); it != freq.end(); it++) {
    S.insert(make_pair(it->first, it->second));
  }
  for(set<pair<string, int>, cmpFunc2>::iterator it = S.begin(); it != 
        S.end(); it++) {
    printf("%s %d\n", it->first.c_str(), it->second);
  }

  return 0;
 }
