#pragma once
#include <unordered_map>

template <typename A, typename B>
class Dictionary
{
public:
	Dictionary() {}
	~Dictionary() {}

	void add(A a, B b)
	{
		a_[b] = a;
		b_[a] = b;
	}

	A a(B val) { return a_[val]; }
	B b(A val) { return b_[val]; }

	std::unordered_map<B, A> getA() { return a_; }
	std::unordered_map<A, B> getB() { return b_; }

private:
	std::unordered_map<B, A> a_;
	std::unordered_map<A, B> b_;
};

