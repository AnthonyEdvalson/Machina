#include <iostream>
#include "Event.h"

int value = 0;

void subscriber(int val)
{
    value = val;
}

int main()
{
    Event<int>* e = new Event<int>();
    e->Subscribe(&subscriber);

    e->Invoke(42);
    std::cout << ((value == 42) ? "OK\n" : "FAIL\n");
    
    e->Unsubscribe(&subscriber);

    value = 0;
    e->Invoke(42);
    std::cout << ((value == 0) ? "OK\n" : "FAIL\n");

    return 0;
}
