#include <vector>
#include <algorithm>

#pragma once

template <class T> class Event {
using F = void (*)(T);
public:
    Event<T>();
    void Invoke(T arg);
    void Subscribe(F farg);
    void Unsubscribe(F farg);
private:
    std::vector<F> subs;
};



template <class T>
Event<T>::Event()
{
    subs = std::vector<void (*)(T)>();
}

    
template <class T>
void Event<T>::Invoke(T arg)
{
    for (int i = 0; i < subs.size(); ++i)
        subs[i](arg);
}


template <class T>
void Event<T>::Subscribe(void (*farg)(T))
{
    subs.push_back(farg);
}


template <class T>
void Event<T>::Unsubscribe(void (*farg)(T))
{
    subs.erase(
        std::remove_if(subs.begin(), subs.end(),
            [&farg](const T& f) { return f == farg; }),
        subs.end()
    );
}




