#pragma once
#include "Defs.h"
#include "Dictionary.h"

#include <vector>
#include <unordered_map>
#include <queue>
#include <iostream>

class Map
{
public:
	enum eTileType { eNull, eFree, eWall, eTarget, ePlayer, eBox, eBoxOnTarget, eNobox };
	enum eHeuristic { eHeuNone, eHeuSparse };

	struct State {
		pos_t playerPos = 0; // Player position
		dir_t playerDir = 1; // Player direction
		std::vector<pos_t> boxPositions = {}; // The position of boxes.

		heu_t currentExpense = 0, futureExpense = 0; // Estimate of current and sfuture expense.

		const heu_t getHeuristic() const; // Returns currentExpense + futureExpense.

		const hash_t getHash() const; // Returns a hashed version of the state. Note this hash lacks heuristic information.
		static State fromHash(hash_t val); // Makes a state from a hashed shate. Note that the state will lack heuristic information.

		static bool comparison(const State& a, const State& b); // Comparison between states.

		const bool operator==(const State& s) const; // Comparison between states.
		const bool containsBox(pos_t position) const; // Query if a box is at a given position.

		const State move(dir_t direction) const; // Returns the state if the current state was to move in the direction.
	}; 

	static Dictionary<tile_t, Map::eTileType> dic;

	struct StateComparison {
		bool operator()(const State& a, const State& b) {
			return Map::State::comparison(a, b);
		}
	};

	Map(const std::vector<eTileType>& map, const std::string& mapName, const std::vector<pos_t>& targetPositions, const pos_t& width, const pos_t& height, const State& initialState);
	~Map();

	const bool hasWon(const State& state) const;

	static pos_t getFirstPosInConnectedArea(const pos_t& position, const State& state, std::vector<eTileType> map, const pos_t& width);
	static std::vector<pos_t> getConnectedArea(const pos_t& position, const State& state, std::vector<eTileType> map, const pos_t& width);

	pos_t getFirstPosInConnectedArea(const pos_t& position, const State& state);
	std::vector<pos_t> getConnectedArea(const pos_t& position, const State& state);

	const pos_t getDistance(pos_t a, pos_t b) const;
	const bool containsTarget(pos_t p) const;

	const std::vector<Map::State> getChildStates(const State& parentState, const eHeuristic& futureExpenseHeuristic) const;
	const pos_t getMaxPos() const;
	const State getInitialState() const;

	static const bool isValid(const pos_t& pos, const std::vector<eTileType>& map);
	const bool isValid(const pos_t& pos) const;

	static const bool isFree(const pos_t& pos, const std::vector<eTileType>& map);
	const bool isFree(const pos_t& pos) const;

	const pos_t getWidth() const;
	
	const std::string getName() const;
	const std::vector<dir_t> getDirections() const;

	std::vector<std::string> getStringOfCommands(size_t length, State initialState);

	static Map loadMap(const std::vector<std::vector<tile_t>>& map, const std::string& mapName);
	static void printMap(const Map& map, const State& state, std::ostream &);
	static std::vector<pos_t> getNeighbors(const pos_t& position, const std::vector<eTileType>& map, const pos_t& width, const std::vector<eTileType>& tiles);
	static bool contains(const eTileType& tile, const std::vector<eTileType>& tiles);

protected:
	const std::string mapName;
	const std::vector<dir_t> directions;
	const pos_t width, height;
	const std::vector<pos_t> targetPositions;
	const std::vector<eTileType> map;
	const Map::State initialState;
};