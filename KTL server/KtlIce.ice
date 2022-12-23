//
// Copyright (c) ZeroC, Inc. All rights reserved.
//

#pragma once

module Demo
{
    class Keyword
    {
        string name;
        string type;
        string value;
    }
    
    sequence<Keyword> KeywordSequence;    
    sequence<string> KeyNameSequence;
    

    interface Hello
    {
        void initialkeywords(KeywordSequence keywords);
        KeyNameSequence keylist();
        void modifiedkeyword(Keyword key);
        void shutdown();
    }
}
