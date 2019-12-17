#pragma once

#include "Defs.h"

#include <string>
#include <vector>
#include <fstream>

namespace json {
	std::string getContents(std::string s, char start, char end) {
		if (s == "") return "";
		int counter = 0;
		size_t i = 0, i_start, i_end;
		while (s[i] != start && i < s.length()) i++;
		i_start = i + 1;
		while ((s[i] != end || counter != 0) && counter >= 0 && i < s.length()) {
			if (s[i] == start) counter++;
			if (s[i] == end) counter--;
			i++;
		}
		i_end = i - 1;
		if (counter != 0) return "";
		return s.substr(i_start, i_end - i_start);
	}

	std::string getContents(std::string s, char delim) {
		if (s == "") return "";
		size_t i = 0, i_start, i_end;
		while (s[i] != delim) i++;
		i_start = ++i;
		while (s[i] != delim) i++;
		i_end = i;
		return s.substr(i_start, i_end - i_start);
	}

	std::vector<std::string> getMultipleCells(std::string s, char start, char end) {
		std::vector<std::string> result;

		std::string temp = "";
		int level = 0;
		for (int i = 0; i < s.size(); i++) {
			if (s[i] == start) {
				level++;
				if (level == 1) temp = "";
			}
			if (s[i] == end) {
				level--;
				if (level == 0) result.push_back(temp);
			}
			if ((s[i] == start && level != 1) || (s[i] == end && level != 0) || (s[i] != start && s[i] != end && level > 0)) temp += s[i];
		}
		return result;
	}

	std::vector<std::string> getMultipleCells(std::string s, char delim) {
		std::vector<std::string> result;

		std::string temp = "";
		bool inCell = false;
		for (int i = 0; i < s.size(); i++) {
			if (s[i] == delim) {
				if (inCell) result.push_back(temp);
				else temp = "";
				inCell = !inCell;
			}
			else if (inCell) temp += s[i];
		}
		return result;
	}

	std::vector<std::string> readJSONList(std::string s) {
		std::string contents = getContents(s, DEFAULT_MAP_CONTAINER_DELIMITER_START, DEFAULT_MAP_CONTAINER_DELIMITER_END);
		std::string categoryName = getContents(s, DEFAULT_MAP_CELL_DELIMITER);
		std::string arrayString = getContents(s, DEFAULT_MAP_DELIMITER_START, DEFAULT_MAP_DELIMITER_END);
		return getMultipleCells(arrayString, DEFAULT_MAP_CELL_DELIMITER);
	}

	std::vector<std::vector<std::string>> readJSONMap(std::string s) {
		std::string contents = getContents(s, DEFAULT_MAP_CONTAINER_DELIMITER_START, DEFAULT_MAP_CONTAINER_DELIMITER_END);
		std::string categoryName = getContents(s, DEFAULT_MAP_CELL_DELIMITER);
		std::string mapString = getContents(s, DEFAULT_MAP_DELIMITER_START, DEFAULT_MAP_DELIMITER_END);
		std::vector<std::string> mapContents = getMultipleCells(mapString, DEFAULT_MAP_DELIMITER_START, DEFAULT_MAP_DELIMITER_END);
		std::vector<std::vector<std::string>> result;
		for (std::string arr : mapContents) {
			std::vector<std::string> arrContents = getMultipleCells(arr, DEFAULT_MAP_CELL_DELIMITER);
			result.push_back(arrContents);
		}
		return result;
	}

	std::vector<std::vector<std::string>> readJSONMapFromFile(std::string path) {
		std::vector<std::vector<std::string>> result;

		std::ifstream file;
		file.open(path, std::ios::in);
		std::string s = "";

		while (file.is_open() && !file.eof()) {
			char c;
			file.read(&c, 1);
			s += c;
		}
		result = readJSONMap(s);

		return result;
	}

	std::vector<std::vector<tile_t>> reduceToChars(std::vector<std::vector<std::string>> vec) {
		std::vector<std::vector<tile_t>> result;

		for (const std::vector<std::string>& vecRow : vec) {
			std::vector<tile_t> row;
			for (const std::string& s : vecRow) row.push_back(s[0]);
			result.push_back(row);
		}

		return result;
	}
}
