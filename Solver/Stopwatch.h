#pragma once

#include <string>
#include <vector>
#include <chrono>
#include <iostream>
#include <sstream>
#include <iomanip>

// Chrono wrapper-ish class as it made a mess in the source file.

class Stopwatch
{
public:
	typedef std::chrono::nanoseconds ns;

	enum Unit {Nanosecond, Microsecond, Millisecond, Second, Kilosecond, Megasecond, Terasecond};

	Stopwatch();
	~Stopwatch();

	void addWatch(std::string watchName = ""); // Adds a new watch with the specified name.
	void start(std::string watchName = ""); // Starts measuring time.
	void stop(std::string watchName = ""); // Stops measuring time since start.
	double getTime(std::string watchName = "", Unit unit = Millisecond); // Get time as value in the specified temporal unit.
	std::string getString(std::string watchName = "", int decimals = 3); // Get time as string. Unit is calculated internally.
	void print(std::string watchName = "");

private:
	int getIndex(std::string watchName);

	// This could have been a binary tree.
	std::vector<std::string> watchNames;
	std::vector<std::pair<ns, ns>> times;
};

