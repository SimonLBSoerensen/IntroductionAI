#include "Dictionary.h"


template<typename A, typename B>
Dictionary<A, B>::Dictionary()
{
}

template<typename A, typename B>
Dictionary<A, B>::~Dictionary()
{
}

template<typename A, typename B>
void Dictionary<A, B>::add(A a, B b)
{
	a_[b] = b;
	b_[a] = b;
}

template<typename A, typename B>
A Dictionary<A, B>::a(B val)
{
	return a_[val];
}

template<typename A, typename B>
B Dictionary<A, B>::b(A val)
{
	return b_[val];
}
