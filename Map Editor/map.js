class TileMap {
    constructor(width, height, gridsize, layerAmount, defaultTile, errortile, context, tilelist) {
        this.map = new Array(layerAmount);
        for (let i = 0; i < layerAmount; i++) {
            let row = new Array(width);
            for (let j = 0; j < width; j++) {
                let col = new Array(height);
                if (i == 0) col.fill(defaultTile);
                row[j] = col;
            }
            this.map[i] = row;
        }
        
        this.width = width;
        this.height = height;
        this.gridsize = gridsize;
        this.layerAmount = layerAmount;
        this.defaultTile = defaultTile;
        this.errortile = errortile;
        this.context = context;
        this.tilelist = tilelist;

        var TO_RADIANS = Math.PI/180; 
    }

    getTileFromList(shorthand) {
        for (const tile of this.tilelist) {
            if (shorthand == tile.shorthand) {
                console.log(tile);
                return tile;
            }
        }
        return this.errortile;
    }

    getTile(x, y, layer) {
        //console.log(layer, this.map)
        return this.map[layer][x][y];
    }

    getSurroundings(x, y) {
        // Make empty surroundings array.
        let surroundings = new Array(3);
        for (let i = 0; i < 3; i++) {
            let row = new Array(3);
            row.fill(undefined);
            surroundings[i] = row;
        }

        // Copy surroundings.
        for (let i = 0; i < 3; i++) {
            let tempx = (i - 1 + x);
            if (tempx >= 0 && tempx < this.width) {
                for (let j = 0; j < 3; j++) {
                    let tempy = (j - 1 + y);
                    if (tempy >= 0 && tempy < this.height) {
                        surroundings[i][j] = this.map[0][tempx][tempy].name;
                    }
                }
            }
        }

        return surroundings;
    }

    getSurroundingString(x, y) {
        let surroundings = this.getSurroundings(x, y);
        let str = "";

        let pos = [[1,0,2], [0,1,4],[2,1,6], [1,2,8]]

        for (const [px, py, v] of pos) {
            if (surroundings[px][py] == surroundings[1][1]) str += v.toString();
        }

        if (!(debug == undefined) && debug.includes('TileMap')) console.log("x, y", x, y, "Surrounding Tiles:", surroundings);

        return str;
    }
    
    drawImage(sx, sy, dx, dy) {
        this.context.drawImage(sprite, sx * gridsize, sy * gridsize, gridsize, gridsize, dx * gridsize, dy * gridsize, gridsize, gridsize);
        if (!(debug == undefined) && debug.includes('drawImage')) console.log("sx, sy, dx, dy, gridsize", sx, sy, dx, dy, gridsize);
    }

    updateTile(x, y) {
        for (let nlayer = 0; nlayer < this.layerAmount; nlayer++) {
            let tile = this.map[nlayer][x][y];
            if (tile !== undefined) {
                let sx, sy;
                if (tile.isDynamic()) {
                    let surroundingString = this.getSurroundingString(x,y);
                    [sx, sy] = tile.getSpritePos(surroundingString);
                }
                else {
                    [sx, sy] = tile.getSprite();
                }
                this.drawImage(sx, sy, x, y);
                //console.log("Updated tile at (x,y): ", x, y)
            }
        }
    }
    
    updateTiles(tile) {
        //console.log(tile.layer);
        for (let i = 0; i < this.width; i++) {
            for (let j = 0; j < this.height; j++) {
                if (this.getTile(i,j,0).name == tile.name) this.updateTile(i, j);
            }
        }
    }

    place(x, y, tile) {
        //console.log(tile);
        this.map[tile.layer][x][y] = tile;
        if (tile.name == 'robot') this.playerPosition = {x, y};
        for (let i = x - 1; i < x + 2; i++) {
            for (let j = y - 1; j < y + 2; j++) {
                if (i >= 0 && j >= 0 && i < this.width && j < this.height) {
                    this.updateTile(i, j);
                }
            }
        }
    }

    remove(x, y, tile) {
        this.map[tile.layer][x][y] = undefined;
        if (tile.name == 'robot') this.playerPosition = {x, y};
        for (let i = x - 1; i < x + 2; i++) {
            for (let j = y - 1; j < y + 2; j++) {
                if (i >= 0 && j >= 0 && i < this.width && j < this.height) {
                    this.updateTile(i, j);
                }
            }
        }
    }

    move(direction) {
        let dx = 0, dy = 0;
        if (direction == 'N') dy = -1;
        if (direction == 'S') dy =  1;
        if (direction == 'W') dx = -1;
        if (direction == 'E') dx =  1;

        let x = this.playerPosition.x + dx, y = this.playerPosition.y + dy;

        if (x < this.width && x >= 0 && y < this.height && y >= 0) {
            let tiles = []
            for (let l = 0; l < 3; l++)  {
                console.log(this.map[l][x][y])
                if (this.map[l][x][y] != undefined) tiles.push(this.map[l][x][y].name);
            }
    
            if (!tiles.includes('wall')) {
                if (tiles.includes('can')) {
                    let nextTiles = []
                    for (let l = 0; l < 3; l++)  if (this.map[l][x + dx][y + dy] != undefined) nextTiles.push(this.map[l][x + dx][y + dy].name);
    
                    if (!nextTiles.includes('wall') && !nextTiles.includes('can')) {
                        // MOVE STUFF
                        let playerTile = this.getTileFromList('P');
                        let canTile = this.getTileFromList('O');
                        this.remove(x - dx, y - dy, playerTile);
                        this.remove(x, y, canTile);
                        this.place(x, y, playerTile);
                        this.place(x + dx, y + dy, canTile);
                        this.playerPosition = {x, y};
                    }
                } else {
                    // MOVE BOT
                    let playerTile = this.getTileFromList('P');
                    this.place(x, y, playerTile);
                    this.remove(x - dx, y - dy, playerTile);
                    this.playerPosition = {x, y};
                }
            }

        }
        
    }

    getString() {
        let str = '{ "table": [';
        for (let i = 0; i < this.width; i++) {
            str += '[';
            for (let j = 0; j < this.height; j++) {
                str += '"';
                let l = this.layerAmount;
                while (this.map[--l][i][j] == undefined);
                str += this.map[l][i][j].shorthand;
                str += '"';
                if (j + 1 < this.height) str += ', ';
            }
            str += ']';
            if (i + 1 < this.width) str += ',\n';
        }
        str += ']}';
        return str;
    }

    fromString(s) {
        let arr = JSON.parse(s)['table'];
        console.log(arr, arr.length)
        for (let x = 0; x < arr.length; x++) {
            const row = arr[x];
            for (let y = 0; y < row.length; y++) {
                const t = row[y];
                let tile = this.getTileFromList(t);
                console.log(x, y, t, tile, this.tilelist)
                this.place(x, y, tile);
            }  
        }
    }

}