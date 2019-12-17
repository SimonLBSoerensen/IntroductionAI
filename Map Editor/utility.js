function strContainsAny(str, chars) {
    for (let i = 0; i < str.length; i++) {
        const ch = chars[i];
        if (str.includes(ch)) return true;
    }
    return false;
}

function strContainsAll(str, chars) { 
    for (let i = 0; i < str.length; i++) {
        const ch = chars[i];
        if (!str.includes(ch)) return false;
    }
    return true;
}