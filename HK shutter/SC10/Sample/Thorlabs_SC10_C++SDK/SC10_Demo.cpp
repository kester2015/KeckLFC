#include <SDKDDKVer.h>
#include <windows.h>
#include <vector>
#include <string>
#include "sc10_cmd_library.h"
#include <tchar.h>

using namespace std;

#define BUFFER_SIZE 256

bool ready_to_exit(){
	char e;
	while(1){
		printf("Press e to exit...");
		e=getchar();
		if(e=='e')
			return true;
	}
}

void Split(string& s,char delim,vector<string>* ret)  
{  
	size_t last = 0;  
	size_t index=s.find_first_of(delim,last);  
	while (index!=string::npos)  
	{  
		ret->push_back(s.substr(last,index-last));  
		last=index+1;  
		index=s.find_first_of(delim,last);  
	}  
	if (index-last>0)  
	{  
		ret->push_back(s.substr(last,index-last));  
	}  
} 

int _tmain(int argc, _TCHAR* argv[])
{
	char devices[256];
	int result = List(devices, 256);
	if(result<=0){
		printf("List devices failed\n");
		if(ready_to_exit())
			return 0;
	}
	string s = devices;
	
	vector<string> deviceVector;
	Split(s,',',&deviceVector);
	
	char id[100];
	strcpy_s(id,deviceVector[0].c_str());

	int handle = Open(id,9600,20);

	if(handle<0){
		printf("Open devices failed\n");
		if(ready_to_exit())
			return 0;
	}

	result = GetId(handle, id);
	printf("\nDevice ID: %s", id);
	
	SetMode(handle,4);  // Set to repeat mode
	SetOpenTime(handle, 2000); // Set open time to 2000ms
	SetCloseTime(handle, 5000); // Set close time to 5000ms
	SetTriggerMode(handle, 0); // Set to internal trigger
	SetRepeatCount(handle, 10); // Set repeat time
	ToggleEnable(handle); // Enable	

	if(ready_to_exit()){		
		Close(handle);
		return 0;
	}
	return 0;
}