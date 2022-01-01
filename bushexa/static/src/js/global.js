String.prototype.capitalize = function() {
    if (this.length === 0) {
        return this;
    }
    if (this.length === 1) {
        return this.charAt(0).toUpperCase();
    }
    return this.charAt(0).toUpperCase() + this.slice(1);
}