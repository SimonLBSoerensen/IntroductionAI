#include "Stopwatch.h"

#define log1000(x) std::log2(x)/std::log2(1000)

// This code has been developed during the 4th. semester by Oliver Vea as a part of an assignment.
// NOT DEVELOPED DURING THIS PROJECT. 

Stopwatch::Stopwatch()
{
}


Stopwatch::~Stopwatch()
{
}

void Stopwatch::addWatch(std::string watchName)
{
	watchNames.push_back(watchName);
	times.push_back(std::pair<ns, ns>());
}

void Stopwatch::start(std::string watchName)
{
	int index = getIndex(watchName);
	if (index == -1) {
		index = watchNames.size();
		addWatch(watchName);
	}
	times[index].first = std::chrono::steady_clock::now().time_since_epoch();

}

void Stopwatch::stop(std::string watchName)
{
	int index = getIndex(watchName);
	if (index != -1) {
		times[index].second = std::chrono::steady_clock::now().time_since_epoch();
	}
}

double Stopwatch::getTime(std::string watchName, Unit unit)
{
	int index = getIndex(watchName);
	if (index != -1) {
		double time = (times[index].second - times[index].first).count();
		time /= pow(1000, (double)unit);
		return time;
	}
}

std::string Stopwatch::getString(std::string watchName, int decimals)
{
	std::string units[] = { "ns","us","ms","s", "ks", "Ms" };

	int index = getIndex(watchName);
	if (index != -1) {
		std::string sTime;
		double time = getTime(watchName, Nanosecond);
		size_t unitVal = log1000(time);
		time = time / pow(10, 3 * unitVal);

		std::ostringstream out;
		out << std::setprecision(decimals) << time;
		sTime = out.str();
		return sTime + units[unitVal];
	}
	return "Watch " + watchName + " not found.";
}

void Stopwatch::print(std::string watchName)
{
	std::cout << getString(watchName) << std::endl;
}

int Stopwatch::getIndex(std::string watchName)
{
	for (int i = 0; i < watchNames.size(); i++) if (watchNames[i] == watchName) return i;
	return -1;
}
