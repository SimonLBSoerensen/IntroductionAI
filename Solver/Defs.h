#pragma once
#include "Stopwatch.h"

#include <string>
#include <vector>

#define THREAD_COUNT 4

#define MAX_STATES 10000000

#define DEFAULT_MAP_DELIMITER_START '['
#define DEFAULT_MAP_DELIMITER_END ']'
#define DEFAULT_MAP_CELL_DELIMITER '"'
#define DEFAULT_MAP_CONTAINER_DELIMITER_START '{'
#define DEFAULT_MAP_CONTAINER_DELIMITER_END '}'

/* -- TYPEDEFS -- */
typedef unsigned short int pos_t;
typedef int dir_t;
typedef double heu_t;
typedef std::string hash_t;
typedef char tile_t;

namespace costs {
	const heu_t halfturn = 1.1;
	const heu_t fullturn = 1.84;
	const heu_t forward = 1.31;
}

const std::string mapPath = "maps/map_3.json";