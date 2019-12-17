class Tile {
    constructor(name, shorthand, layer, offsetX, offsetY) {
        this.name = name;
        this.shorthand = shorthand;
        this.layer = layer;
        this.offsetX = offsetX;
        this.offsetY = offsetY;
    }

    isDynamic() {
        return false;
    }

    getName() {
        return this.name;
    }

    getSprite() {
        return [this.offsetX, this.offsetY];
    }
}


class DynamicTile {
    constructor(name, shorthand, layer, offsetX, offsetY) {
        this.name = name;
        this.shorthand = shorthand;
        this.layer = layer;
        this.offsetX = offsetX;
        this.offsetY = offsetY;
    }

    isDynamic() {
        return true;
    }

    getName() {
        return this.name;
    }

    getSpritePos(surroundingString) {
        let res = [0, 0];

        if (surroundingString == '2') res = [3,1];
        if (surroundingString == '4') res = [2,0];
        if (surroundingString == '24') res = [2,3];
        if (surroundingString == '6') res = [1,0];
        if (surroundingString == '26') res = [0,3];
        if (surroundingString == '46') res = [3,4];
        if (surroundingString == '246') res = [1,3];
        if (surroundingString == '8') res = [3,0];
        if (surroundingString == '28') res = [2,4];
        if (surroundingString == '48') res = [2,1];
        if (surroundingString == '248') res = [2,2];
        if (surroundingString == '68') res = [0,1];
        if (surroundingString == '268') res = [0,2];
        if (surroundingString == '468') res = [1,1];
        if (surroundingString == '2468') res = [1,2];


        if (!(debug == undefined) && debug.includes('DynamicTile')) console.log('DynamicTile with input ' + surroundingString, 'returned:',[res[0] + this.offsetX, res[1] + this.offsetY]);
        return [res[0] + this.offsetX, res[1] + this.offsetY];
    }

    getSprite() {
        return [this.offsetX, this.offsetY];
    }
}