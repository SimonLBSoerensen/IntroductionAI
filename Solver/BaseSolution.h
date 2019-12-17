#pragma once

#include "Defs.h"
#include "Map.h"

#include <vector>
#include <unordered_map>
#include <unordered_set>

class BaseSolution
{
public:
	virtual ~BaseSolution() = default;
	virtual std::vector<Map::State> solve(Map map, Map::State state) = 0;
};

