#include "IDepthFirst.h"

size_t getMemoryUse() {
	PROCESS_MEMORY_COUNTERS_EX pmc;
	GetProcessMemoryInfo(GetCurrentProcess(), (PROCESS_MEMORY_COUNTERS*)&pmc, sizeof(pmc));
	return pmc.PrivateUsage;
}

void writeToFile(std::string message, std::string filename) {

	std::fstream file;
	file.open(filename, std::fstream::app);
	file << message << std::endl;
	file.close();
}

std::vector<Map::State> IDepthFirst::solve(Map map, Map::State state, Map::eHeuristic heuristic, size_t threads, std::string logPath = "")
{
	Stopwatch sw;
	sw.start("totalTime");
	std::mutex a, b;
	std::unordered_map<hash_t, std::pair<heu_t, hash_t>> pastBest;
	std::priority_queue<Map::State, std::vector<Map::State>, Map::StateComparison> openSet;

	std::vector<std::mutex> vmStopThread(threads);
	std::vector<int> vbStopThread(threads);
	for (int i = 0; i < threads; i++) vbStopThread[i] = 0;
	std::vector<std::mutex> vmThreadPaused(threads);
	std::vector<int> vbThreadPaused(threads);
	for (int i = 0; i < threads; i++) vbStopThread[i] = 0;
	std::vector<std::future<Map::State>> results(threads);

	openSet.push(state);

	for (int i = 0; i < threads; i++) {
		std::mutex &mStopThread = vmStopThread[i], &mThreadPaused = vmThreadPaused[i];
		int& bStopThread = vbStopThread[i];
		int& bThreadPaused = vbThreadPaused[i];
		results[i] = std::async(std::launch::async, [map, &a, &b, &mStopThread, &bStopThread, &mThreadPaused, &bThreadPaused, &pastBest, &openSet, heuristic] { return task(map, a, b, mStopThread, bStopThread, mThreadPaused, bThreadPaused, pastBest, openSet, heuristic); });
	}

	bool gotSolution = false, outOfStates = false;
	while (!gotSolution && !outOfStates && pastBest.size() < MAX_STATES) {
		for (int i = 0; i < threads; i++) gotSolution |= results[i]._Is_ready();
		int pausedThreads = 0;
		for (int i = 0; i < threads; i++) {
			vmThreadPaused[i].lock();
			pausedThreads += vbThreadPaused[i];
			vmThreadPaused[i].unlock();
		}
		outOfStates |= pausedThreads == threads;
		std::this_thread::sleep_for(std::chrono::milliseconds(20));
	}

	for (int i = 0; i < threads; i++) {
		vmStopThread[i].lock();
		vbStopThread[i] = true;
		vmStopThread[i].unlock();
	}

	if (outOfStates && logPath != "" && map.getName() != "") {
		sw.stop("totalTime");
		size_t memUsed = getMemoryUse();
		writeToFile(map.getName() + ", " + "-1" + ", " + std::to_string(pastBest.size()) + ", " + std::to_string(openSet.size()) + ", " + std::to_string(sw.getTime("totalTime")) + ", " + std::to_string(memUsed), logPath);
		return {};
	}

	Map::State bestState;

	std::vector<Map::State> r(threads);
	std::vector<bool> hW(threads);

	for (int i = 0; i < threads; i++) {
		r[i] = results[i].get();
		hW[i] = map.hasWon(r[i]);
	}
	for (int i = 0; i < threads; i++) { if (bestState == Map::State() || (!(r[i] == Map::State()) && r[i].getHeuristic() < bestState.getHeuristic())) bestState = r[i]; }

	std::vector<Map::State> solution;

	while (!(bestState == Map::State() || bestState == state)) {
		solution.push_back(bestState);
		hash_t bestHash = bestState.getHash();
		auto pastBestPair = pastBest[bestHash];
		hash_t parentHash = pastBestPair.second;
		bestState = Map::State::fromHash(parentHash);

		if (solution.size() > 20000) {
			sw.stop("totalTime");
			size_t memUsed = getMemoryUse();
			writeToFile(map.getName() + ", " + "-2" + ", " + std::to_string(pastBest.size()) + ", " + std::to_string(openSet.size()) + ", " + std::to_string(sw.getTime("totalTime")) + ", " + std::to_string(memUsed), logPath);
			return {};
		}
	}

	std::reverse(solution.begin(), solution.end());

	sw.stop("totalTime");
	std::cout << "Found solution with " << solution.size() << " steps after searching " << pastBest.size() << " states. Time to calculate: " << sw.getString("totalTime") << std::endl;

	if (logPath != "" && map.getName() != "") {
		sw.stop("totalTime");
		size_t memUsed = getMemoryUse();
		writeToFile(map.getName() + ", " + std::to_string(solution.size()) + ", " + std::to_string(pastBest.size()) + ", " + std::to_string(openSet.size()) + ", " + std::to_string(sw.getTime("totalTime")) + ", " + std::to_string(memUsed), logPath);
	}

	return solution;
}

Map::State IDepthFirst::task(const Map& map, std::mutex& a, std::mutex& b, std::mutex& mStopThread, int& bStopThread, std::mutex& mThreadPaused, int& bThreadPaused, std::unordered_map<hash_t, std::pair<heu_t, hash_t>>& pastBest, std::priority_queue<Map::State, std::vector<Map::State>, Map::StateComparison>& openSet, Map::eHeuristic heuristic)
{
	Map::State currentState;
	int i = 0;
	do {
		mStopThread.lock();
		a.lock();
		while (openSet.size() == 0 && !bStopThread) {
			a.unlock();
			mStopThread.unlock();
			mThreadPaused.lock();
			bThreadPaused = 1;
			mThreadPaused.unlock();
			std::this_thread::sleep_for(std::chrono::milliseconds(20));
			mStopThread.lock();
			a.lock();
		}
		mStopThread.unlock();
		mThreadPaused.lock();
		bThreadPaused = 0;
		mThreadPaused.unlock();

		if (bStopThread) {
			a.unlock();
			return Map::State();
		}

		currentState = openSet.top();
		openSet.pop();
		a.unlock();

		std::vector<Map::State> newStates = map.getChildStates(currentState, heuristic);

		for (Map::State newState : newStates) {
			hash_t hash = newState.getHash();

			b.lock();
			const std::pair<heu_t, hash_t> past = pastBest[hash];
			b.unlock();

			if (past.first == 0 || (past.first > newState.getHeuristic())) {
				a.lock();
				openSet.push(newState);
				a.unlock();
				const hash_t currentHash = currentState.getHash();
				b.lock();
				pastBest[hash] = { newState.getHeuristic(), currentHash };
				b.unlock();
			}
		}
		i++;
	} while (!map.hasWon(currentState));
	return currentState;
}
